#!/bin/bash

for z in `ls *.zip`
do
    # https://stackoverflow.com/questions/965053/extract-filename-and-extension-in-bash
    filename=$(basename -- "$z")
    extension="${filename##*.}"
    filename="${filename%.*}"
    mkdir -p $filename
    mv $z $filename/$z
    pushd $filename
    unzip $z
    popd
done