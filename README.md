[![License](https://img.shields.io/badge/license-%20CC--BY-blue.svg)](LICENSE)


## Data for Hill Mari language constructicon


### Generation of YAML files

First the Google spreadsheet is saved as Excel sheet.
Then the Excel sheet is opened and saved in CSV format.

Then, YAML files are auto-generated from `database.csv` using:
```bash
$ rm -f data/*yml  # this is to make sure that deleted records get removed also in this repository
$ python convert-db.py database.csv
```


### Combined data file

The individual YAML files are combined into one data on the "generated" branch.
The motivation to combine them is to speed up the web page load which is
significantly faster when one big file is fetched compared to fetching hundreds
of small files.

This is done automatically upon each push or pull request towards the `main`
branch using [this workflow](.github/workflows/combine.yml):

```bash
$ python combine-data.py data > data-combined.yml
```


### Splitting the combined data file

You can also do the opposite of the above and split the combined data file
like this (this will write the data files to the folder `data`, you can change
the name/location):

```bash
$ python split-data.py data-combined.yml data
```
