#!/bin/bash

BANDS_PATH="/opt/upme/bands"
OUTPUT_PATH="/opt/upme/tsvs"
NUM_THREADS=1
SID=$1
BAND_NUMBER=$2

gdal_calc.py --overwrite --calc "(A==4)*B" --format GTiff --type Float32 --NoDataValue 0.0 --quiet --debug \
    -A ${BANDS_PATH}/${SID}_SCL.tif --A_band 1 \
    -B ${BANDS_PATH}/${SID}_B${BAND_NUMBER}.tif --B_band 1 \
    --co "NUM_THREADS=${NUM_THREADS}" --co="COMPRESS=DEFLATE" \
    --outfile ${OUTPUT_PATH}/${SID}_PRIME${BAND_NUMBER}.tif

gdalwarp -t_srs EPSG:9377 -co NUM_THREADS=${NUM_THREADS} -co COMPRESS=DEFLATE -overwrite \
 ${OUTPUT_PATH}/${SID}_PRIME${BAND_NUMBER}.tif ${OUTPUT_PATH}/${SID}_B${BAND_NUMBER}.tif 
    
python pixels2points.py --n 1024 ${OUTPUT_PATH}/${SID}_B${BAND_NUMBER}.tif ${OUTPUT_PATH}