#!/bin/bash

cat $1 | parallel -j $2 -k --colsep '\t' gdalwarp -t_srs EPSG:9377 -tr 10.0 10.0 -r near -of GTiff -co compress=lzw -ot Int16 {1}.dem.tif {1}.dem.warp.tif
