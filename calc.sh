#!/bin/bash

#S2A_MSIL2A_20230127T150721_R082_T19NBG_20230128T231543
BANDS_PATH="/home/acald013/opt/upme/bands"
OUTPUT_PATH="/home/acald013/tmp"
SID=$1
NUM_THREADS=2
BAND_NUMBER=$2

gdal_calc.py --overwrite --calc "(A==4)*B" --format GTiff --type Float32 --NoDataValue 0.0 --quiet --debug \
    -A ${BANDS_PATH}/${SID}_SCL.tif --A_band 1 \
    -B ${BANDS_PATH}/${SID}_B${BAND_NUMBER}.tif --B_band 1 \
    --co "NUM_THREADS=${NUM_THREADS}" --co="COMPRESS=DEFLATE" \
    --outfile ${OUTPUT_PATH}/PRIME${BAND_NUMBER}.tif
gdalwarp -t_srs EPSG:9377 -overwrite ${OUTPUT_PATH}/PRIME${BAND_NUMBER}.tif ${OUTPUT_PATH}/B${BAND_NUMBER}.tif \
    -co NUM_THREADS=${NUM_THREADS} -co COMPRESS=DEFLATE \
