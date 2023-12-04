library(tidyverse)

ids1 <- read_tsv("missing_bands_v1.tsv", col_names = F) 
ids2 <- read_tsv("missing_bands_solved_v3.tsv", col_names = F) 

setdiff(ids1, ids2) |> write_tsv("missing_bands_v3.tsv", col_names = F)
