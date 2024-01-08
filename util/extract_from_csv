#!/usr/bin/env python3
""" Extract just the fields we need from the CSVs. """

import sys
import csv

name = sys.argv[1]
file_name = sys.argv[2]
destination = sys.argv[3]
destination_file = destination + "/" + name + ".csv"
# print(destination_file)

# From: https://docs.python.org/3/library/csv.html
with open(file_name, newline='', encoding="utf-8") as csv_file_in:
    fieldnames = ['long', 'lat']

    reader = csv.DictReader(csv_file_in)

    with open(destination_file, 'w', newline='', encoding="utf-8") as csv_file_out:
        writer = csv.DictWriter(csv_file_out, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            if row['default_longitude-deg'] == '':
                continue
            if row['default_latitude-deg'] == '':
                continue

            keep = {'long': row['default_longitude-deg'], 'lat': row['default_latitude-deg']}
            writer.writerow(keep)
            # print(row['default_latitude-deg'], row['default_longitude-deg'])
