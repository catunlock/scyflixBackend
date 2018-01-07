#!/bin/bash
PAPERS="/home/sunlock/selected_papers/*"
OUTPUT_PATH="/home/sunlock/image_papers/"
for f in $PAPERS
do
    python extractFirstPage2.py $f $OUTPUT_PATH
done