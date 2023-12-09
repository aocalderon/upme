#!/bin/bash

cat $1 | parallel -j $2 -k --colsep '\t' gdaldem slope {1}.dem.tif {1}.slope.tif -of GTiff -b 1 -s 1.0 -p -co compress=lzw
