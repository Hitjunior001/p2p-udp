import csv

with open('input.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(','.join(row))