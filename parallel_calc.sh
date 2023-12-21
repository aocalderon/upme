#!/bin/bash

cat $1 | parallel -j $2 -k --colsep '\t' ./calc.sh {1} {2}
