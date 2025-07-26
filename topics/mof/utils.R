use("data.table", c("fcase", "%ilike%"))

fix_region_names = function(region) {
  fcase(
    region %ilike% "Orom(o|(iy|i)a)", "Oromia",
    region %ilike% "Somm?all?e?", "Somalia",
    region %ilike% "Beni?shangul|Gumuz", "Benshangul Gumuz",
    region %ilike% "Tigg?ray", "Tigray",
    region %ilike% "Amh?arr?a", "Amhara",
    region %ilike% "Addis\\s*Abb?(e|a)bb?(e|a)","Addis Ababa",
    region %ilike% "Dire\\s*D(a|e)wa", "Dire Dawa",
    region %ilike% "Aff?ar", "Afar",
    region %ilike% "Gambell?a", "Gambela",
    region %ilike% "Harr?arr?i", "Harari",
    region %ilike% "South(ern)?\\s*(Nations|Nationalities)", "SNNP",
    region %ilike% "Sidama", "SNNP (Sidama)",
    region %ilike% "South(ern)?\\s*West", "SNNP (SWEP)",
    region %ilike% "Central\\s*Ethiopia", "SNNP (CE)",
    region %ilike% "South(ern)?\\s*Ethiopia", "SNNP (SE)",
    rep(TRUE, length(region)), region
  )
}


extract_year = function(text, pattern) {
  year = regmatches(text, regexpr(pattern, text, perl = TRUE))
  as.integer(year)
}


to_eth_ym = function(ym) {
  if (!all(grepl("^\\d{4}M\\d{1,2}$", ym, ignore.case = TRUE))) {
    stop("ym should be formatted as yyyyMmm.", call. = FALSE)
  }

  year = as.integer(substr(ym, 1, 4))
  month = as.integer(substr(ym, 6, nchar(ym)))

  eth_year = integer(length(year))
  eth_mon = integer(length(month))
  for (i in seq_along(eth_year)) {
    if (month[i] >= 9L) {
      eth_mon[i] = month[i] - 8L
      eth_year[i] = year[i] - 7L
    } else {
      eth_mon[i] = month[i] + 4L
      eth_year[i] = year[i] - 8L
    }
  }
  ym = sprintf("%sM%02s", eth_year, eth_mon)
  return(ym)
}

## Ethiopain months
# 1.	Meskerem (September/October)
# 2.	Tekemt (October/November)
# 3.	Hedar (November/December)
# 4.	Tahesas (December/January)
# 5.	Tir (January/February)
# 6.	Yekatit (February/March)
# 7.	Megabit (March/April)
# 8.	Miyazya (April/May)
# 9.	Ginbot (May/June)
# 10.	Sene (June/July)
# 11.	Hamle (July/August)
# 12.	Nehase (August/September)
# 13.	Pagume (September)
