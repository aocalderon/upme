#!/bin/bash

THE_FILE=$1
THE_FOLDER=$2
THE_WORKERS=$3

ls -1 $THE_FOLDER > temp
cut -f1 -d'.' temp > just_found.tsv

echo "Bands already done:"
cat just_found.tsv

python missing_ids_setter.py -m $THE_FILE -f just_found.tsv -o still_missing.tsv

echo "Bands still missing:"
cat still_missing.tsv

cat still_missing.tsv | parallel -j $THE_WORKERS -k --colsep '\t' python downloader.py -i {1} -b {2} -w 1 -o $THE_FOLDER
