#!/bin/bash

cat $1 | parallel --colsep '\t' python download_id_by_bands.py -i {1} -b {2} -w $2
