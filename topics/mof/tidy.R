library(data.table)
source("utils.R")

data_dir = "data/budget-regional/raw/"
data_pat = "budget_(\\d{4})EC\\.csv"
eth_year_pat = "(?i)\\d+(?=EC)"



# budget files
files = list.files(
  "data/budget-regional/raw/", data_pat, recursive = FALSE, full.names = TRUE
)

budget = setNames(files, extract_year(basename(files), eth_year_pat)) |>
  lapply(fread) |>
  rbindlist(use.names = TRUE, idcol = "year")

# budgets for missing years (scraped)
files2 = list.files(file.path(data_dir, "alternatives/"), data_pat, full.names = TRUE)
names(files2) = extract_year(files2, eth_year_pat)

budget2 = lapply(files2, \(f) fread(f, quote = "\"")) |>
  rbindlist(idcol = "year", use.names = TRUE,  fill = TRUE)

# Combine
# If any duplicates, then will be dealt below
budget = rbindlist(list(mof=budget, other=budget2), idcol = "source", fill = TRUE, use.names = TRUE)
budget[, year:=as.integer(year)]

# Correct region names
budget[, region0 := region # the original for checkup
      ][, region := fix_region_names(region)]

# Check for duplicates
stopifnot(all(budget[, .N, .(region, year)]$N == 1))
# budget = budget[, .(value = first(value)), .(region, year)]

# TODO: Merge with regions.csv for full/amharic names


## Population data ----

# census data
pop_2007 = fread(
  "data/pop-and-hhs-eth_2007.csv", select = c("region", "Date", "Value")
)
# population projections
pop = fread("data/projected-pop.csv")

idvar = "region"
pop = reshape(
  pop, direction = "long", idvar = idvar, sep = "_",
  varying = setdiff(names(pop), idvar), timevar = "year"
)
setorderv(pop, "year")
pop[, region := fix_region_names(region)]

setnames(pop_2007, c("Value", "Date"), c("pop", "year"))
pop_2007 |>
  subset(
    grepl(
      "(Addis Ababa)|(Dire Dawa)|(-?Region(?![)]))|(Sidama.Zone)", region, perl = TRUE, ignore.case = TRUE)
  ) -> region_pop
region_pop[, `:=`(
  region = fix_region_names(region),
  year = paste0("2000", "/", year)
)]

region_pop = rbind(
  region_pop,
  pop[
    tolower(region) %notin% c("ethiopia", "special"),
    .(region, year, pop = total)
  ],
  use.names = TRUE
)
region_pop[,
  c('year', 'year_gc') := tstrsplit(year, split = "/", type.convert = as.integer)
]


# Add the latest population stats
budget = merge(
  budget, region_pop[year == max(year), .(region, pop_2013 = pop)],
  by = "region", all.x = TRUE
)


## CPI (adjusting for inflation) ----

cpi = fread("../cpi/data/cpi-ethiopia_base2016m12.csv")
cpi[, date_ec := to_eth_ym(date)]
# Construct yearly cpi from monthly values
cpi = cpi[, .(cpi = mean(value, na.rm = TRUE)), .(year = extract_year(date_ec, "^\\d{4}"))]

budget = merge(budget, cpi, "year", all.x = TRUE)
setcolorder(budget, c("region", "region0", "year", "value"))
setcolorder(budget, "source", after = last(names(budget)))

fwrite(budget, "data/budget-regional/processed/budget.csv")
