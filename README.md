# lego-pab-tool

Make Lego Pick a Brick (<https://www.lego.com/en-us/pick-and-build/pick-a-brick>) orders easier by curating parts lists with this collection of tools.

## `part_list_combiner`

Tool for coalescing the Lego parts from multiple CSV files into a single CSV for uploading to Lego's Pick a Brick service.

Dumps to standard output in CSV format.

Usage:

```bash
$ python part_list_combiner.py > combined.csv
```

This tool is useful for creating individual part list files for specific builds -- minifigures being a primary example. Say you want to build specific minifigures via Pick a Brick. Normally you would have to find all the parts, pick them on Pick a Brick, and then they all go into one large cart that can be hard to keep track of. Using the `part_list_combiner` tool you can create separate CSV files for every minifigure you want to build. As an added bonus, this also serves as a way to store and reuse your builds for the future. Another example is for modular city builders using the MILS system. You can create a parts list for MILS plates with varying top-plate colors and then create a combined CSV with multiple MILS plates for a single order.