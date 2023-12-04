library(tidyverse)

fields <- c("A1","A2","A3","A4","A5","A6","Band")
read_tsv("missing_bands_v4.tsv", col_names = c("id")) |>
  separate(id, into = fields, sep = "_") |>
  mutate(id = paste0(A1,"_",A2,"_",A3,"_",A4,"_",A5,"_",A6)) |>
  select(id, Band) |>
  group_by(id) |> summarise(Band = str_c(Band, collapse = ",")) |>
  write_tsv("missing_bands.tsv", col_names = F)

