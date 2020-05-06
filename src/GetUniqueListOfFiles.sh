#!/bin/bash

for db in Lightroom*.lrcat
do
	python3.8 lr_reader.py --verbose "${db}"
done | sed 's/F:\/Pictures\///g' | sed 's/F:\///g' | sort -u | tee image-files.txt
