# lego-pab-tool

Make Lego Pick a Brick orders easier by curating parts lists with this collection of tools.

## `part_list_combiner`

Tool for coalescing the Lego parts from multiple CSV files into a single CSV for uploading to Lego's Pick a Brick service.

Dumps to standard output in CSV format.

Usage:

```bash
$ python part_list_combiner.py > combined.csv
```