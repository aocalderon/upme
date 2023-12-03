#!/bin/bash

cat missing_bands_25.tsv | parallel --colsep '\t' echo "python download_id_by_bands.py -i {1} -b {2}"
