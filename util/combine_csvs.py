#!/usr/bin/env python3
"""Combine a directory of CSVs into one CSV. """

import sys
import csv
from os import listdir
from os.path import isfile, join

# Parameters from the command line.
directory_in = sys.argv[1]
file_out = sys.argv[2]


def read_csv(in_file_name):
    """ Read the origin file. """

    rows = []
    with open(in_file_name, newline='', encoding="utf-8") as csvfileIn:
        reader = csv.DictReader(csvfileIn)

        for row in reader:
            shouldSkip = False

            if shouldSkip:
                print ("Skipping row that is missing data.")
                continue

            rows.append(row)

            # print(row['default_latitude-deg'], row['default_longitude-deg'])
            # keep = {'long': row['default_longitude-deg'], 'lat': row['default_latitude-deg']}

    return rows

def write_csv(out_file_name, rows):
    """ Write the destination file. """

    if len(rows) < 2:
        print("No rows for " + out_file_name + ". Skipping.")
        return

    with open(out_file_name, 'w', newline='', encoding="utf-8") as csv_file_out:
        writer = csv.DictWriter(csv_file_out, fieldnames=rows[1].keys())
        writer.writeheader()

        for row in rows:
            writer.writerow(row)

only_files = [f for f in listdir(directory_in) if isfile(join(directory_in, f))]

root_rows = []

print ("Read " + directory_in + ': ', end='')
for file_name_in in only_files:
    file_in = directory_in + '/' + file_name_in
    file_rows = read_csv(file_in)
    print('.', end='', flush=True)

    for file_row in file_rows:
        root_rows.append(file_row)
print()

print("Write " + file_out)
write_csv(file_out, root_rows)
