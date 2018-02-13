#!/bin/bash

# Decompress each .zip file in pwd into its own directory
# (i.e. a.zip -> a, b.zip -> b, etc.):

for zipfile in *.zip; do
    zipdir="${zipfile%.zip}"
    mkdir "$zipdir"
    unzip -d "$zipdir" "$zipfile"
done
