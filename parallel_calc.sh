#!/bin/bash

parallel -j $1 -k ./calc.sh :::: test.tsv ::: 02 03 04 05 06 07 08 11 12