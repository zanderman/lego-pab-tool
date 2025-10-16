"""Tool for coalescing the Lego parts from multiple CSV files into a single CSV for uploading to Lego's Pick a Brick service.

Dumps to standard output in CSV format.

Usage:
>>> $ python part_list_combiner.py > combined.csv
"""
from pathlib import Path
import sys
import csv

# Collection of part CSV files to be combined.
root = Path("./example-part-lists/")
d = {
    "pab-pirate-0.csv": 1,
    "pab-pirate-1.csv": 4,
    #
    "pab-falcon-knight-0.csv": 5,
    "pab-falcon-knight-1.csv": 5,
    "pab-falcon-knight-2.csv": 5,
    "pab-falcon-knight-3.csv": 5,
    "pab-falcon-knight-horse.csv": 5,
    "pab-forestmen-0.csv": 5,
    "pab-forestmen-1.csv": 5,
    "pab-forestmen-2.csv": 5,
    "pab-forestmen-3.csv": 5,
    "pab-lion-knight-0.csv": 5,
    "pab-lion-knight-1.csv": 5,
    "pab-lion-knight-2.csv": 5,
    "pab-lion-knight-3.csv": 5,
    "pab-lion-knight-4.csv": 5,
    "pab-lion-knight-horse.csv": 5,
    "pab-townsfolk-0.csv": 5,
    "pab-townsfolk-1.csv": 5,
    "pab-wolfpack-0.csv": 5,
    "pab-wolfpack-1.csv": 5,
    "pab-wolfpack-2.csv": 5,
    "pab-wolfpack-3.csv": 5,
}

# Process individual CSV files.
inventory = {}
necessary_fields = ['elementId','quantity']
for fname, quantityMultiplier in d.items():
    with open(root/fname) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',') # Treat first row as header and process into dictionary.
        fieldnames = reader.fieldnames
        for row in reader:
            # Only collect the necessary fields from the current row.
            row = {field: row[field] for field in necessary_fields}
            
            # Create an image field.
            row['image'] = f"https://www.lego.com/cdn/product-assets/element.img.photoreal.192x192/{row['elementId']}.jpg"
            
            # Create new entry for current part if none exists.
            if row['elementId'] not in inventory:
                inventory[row['elementId']] = row
                inventory[row['elementId']]['quantity'] = int(inventory[row['elementId']]['quantity']) * quantityMultiplier
            # Increment existing part count by the total number of parts listed.
            else:
                inventory[row['elementId']]['quantity'] += int(row['quantity']) * quantityMultiplier

# Dump total inventory to CSV.
fieldnames = ['elementId','quantity','image']
writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(inventory.values())