"""Tool for coalescing the Lego parts from multiple CSV files into a single CSV for uploading to Lego's Pick a Brick service.

Input is a JSON file with the format:

```json
{
    "path/to/csv": <quantity>,
}
```

Dumps to standard output in CSV format by default, or use `-o` for dumping to a file.

Usage:
>>> $ python part_list_combiner.py example-orders/example-order.json > combined.csv
"""
from pathlib import Path
import sys
import csv
import json


def process_order_file_to_partlists(filepath: Path) -> dict:
    # Read order.
    with open(filepath, 'r') as jsonfile:
        d = json.load(jsonfile)
    return d

def process_partlists_to_inventory(d: dict) -> dict:
    # Process individual CSV files.
    inventory = {}
    necessary_fields = ['elementId','quantity']
    for fpath, quantityMultiplier in d.items():
        with open(fpath) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',') # Treat first row as header and process into dictionary.
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
    return inventory

def dump_inventory_to_csv(inventory: dict, f):
    # Dump total inventory to CSV.
    fieldnames = ['elementId','quantity','image']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(inventory.values())

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filepath", type=Path, help="Path to input JSON file.")
    parser.add_argument("-o", "--outfile", type=Path, help="Path to input output CSV file.", default=None, required=False)
    args = parser.parse_args()
    filepath = Path(args.filepath)
    outfile = args.outfile
    
    # Process the order file into a dictionary of part lists.
    d = process_order_file_to_partlists(filepath)
    
    # Process the partlists into a consolidated inventory.
    inventory = process_partlists_to_inventory(d)
    
    # Dump the inventory to CSV format.
    if outfile is None:
        dump_inventory_to_csv(inventory, f=sys.stdout)
    else:
        with open(outfile, 'w+') as f:
            dump_inventory_to_csv(inventory, f=f)