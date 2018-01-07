#!/bin/bash
PAPERS="/home/sunlock/computer_science_magpie/*"
OUTPUT_PATH="/home/sunlock/image_papers/"
for f in $PAPERS
do
    python extractFirstPage.py $f $OUTPUT_PATH
done