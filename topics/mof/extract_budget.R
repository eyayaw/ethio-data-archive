library(data.table)
use("readxl", "read_excel")

xls_files = c(
  "2000" = "federal_governemnt_budget_proclamation_2000.xls",
  "2001" = "federal_governemnt_budget_proclamation_2001.xls",
  "2002" = "federal_governemnt_budget_proclamation_2002.xls",
  "2003" = "federal_governemnt_budget_proclamation_2003.xls",
  "2004" = "federal_governemnt_budget_proclamation_2004.xls",
  "2005" = "federal_governemnt_budget_proclamation_2005.xls",
  # 2006 missing --- see below,
  "2007" = "federal_governemnt_budget_proclamation_2007.xls",
  "2008" = "federal_governemnt_budget_proclamation_2008.xls",
  # 2009 missing -- see blow
  # 2010 missing -- see blow
  "2011" = "federal_governemnt_budget_proclamation_2011.xlsx",
  "2012" = "2012_ec_budget_year_goe_federal_budget_proclamation_part_two.xlsx",
  "2013" = "2013_ec_budget_year_goe_federal_budget_proclamation_part_two.xlsx",
  "2014" = "2014_ec_budget_year_goe_federal_budget_proclamation_part_twoh.xlsx",
  "2015" = "2015_ec_budget_year_goe_federal_budget_proclamation_part_two.xlsx",
  "2016" = "2016_ec_budget_year_goe_federal_budget_proclamation_part_two.xlsx",
  "2017" = "executive_budget_proposal_efy_2017_-202425__budget_year_goe_federal_budget_proclamation-proposal.xlsx",
  "2018" = "2018_e_c_budget_year_goe_federal_budget_proclamation_part_two.xlsx"
)

budgets = lapply(
  xls_files,
  \(f) {
    read_excel(
      file.path("docs/budget/", f),
      sheet = "Kelel Degoma Summary",
      col_names = FALSE,
      skip = 5
    )
  }
)

budgets = budgets |>
  # remove empty cols
  lapply(\(x) x[, !apply(x, 2, \(col) all(is.na(col)))]) |>
  # skip the amharic cols
  lapply(\(x) x[, -c(1:4)]) |>
  lapply(\(x) setNames(x, c("region", "value"))) |>
  rbindlist(use.names = TRUE, idcol = "year") |>
  na.omit()

# write regional budgets to csvs
for (y in unique(get("year", budgets))) {
  fwrite(
    budgets[year == y, !"year"],
    file.path("data/budget-regional/raw", sprintf("budget_%sEC.csv", y))
  )
}
