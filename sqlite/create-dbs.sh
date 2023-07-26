#!/bin/bash

# 1. I download `gen20.txt` from Census.
# 1. I open `sqlite3`. 
# 1. I issue `.mode csv`
# 1. I issue `.separator |`
# 1. I create the table below.
# 1. I issue `.import gen20.txt general`

for d in `ls -d */`
do
    filename=$(basename -- "$d")
    dirname="${filename%.*}"
    echo ${dirname}
    pushd $dirname
        cat <<EOF > script.sql
.mode csv
.separator |
EOF
    dbfilename="${filename}.sqlite3"
    [ -e $dbfilename ] && rm $dbfilename
    touch $dbfilename
    for f in `ls *.txt`
    do
        txtfilename=$(basename -- "$f")
        txtextension="${txtfilename##*.}"
        txtfilename="${txtfilename%.*}"
    
        # https://unix.stackexchange.com/questions/245362/remove-numbers-strip-numeric-characters-from-the-string-variable
        tablename=$(printf '%s\n' "${txtfilename//[[:digit:]]/}")
        # echo $tablename
        cat <<EOF >> script.sql
.import $f $tablename
EOF
    # https://dba.stackexchange.com/questions/175986/scripting-sqlite-with-dot-commands
    done
    sqlite3 -batch $dbfilename < script.sql
    popd
done