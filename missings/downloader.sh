#!/bin/bash

cat $1 | parallel -j $2 -k --colsep '\t' python downloader.py -i {1} -b {2} -o downloads/
