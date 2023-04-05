1. Download .zip files from Census containing all the tables for a given year. (This works best year-by-year.)
2. Place them in this directory.
3. Run `unzip-all.sh`. This will create directories, move the zips into them, and unzip them.
4. Run `create-dbs.sh`. This will go through each directory and load all the .txt files into .sqlite3 files.

This creates SQLite3 DB files that can be used for exploration.

The import process yields a lot of unescaped character errors, as well as some 

```
revisions22.txt:100: expected 19 columns but found 6 - filling the rest with NULL
```

type errors. (Or, a lot of them.) This further suggests there are significant problems in the Census data exports.