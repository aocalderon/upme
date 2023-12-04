library(tidyverse)

ids1 <- read_tsv("missing_bands_v1.tsv", col_names = F) 
ids2 <- read_tsv("missing_bands_solved_v4.tsv", col_names = F) 

setdiff(ids1, ids2) |> write_tsv("missing_bands_v4.tsv", col_names = F)
