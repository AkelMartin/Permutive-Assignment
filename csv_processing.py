import csv

def read_csv(file_path):
    """
    Reads a CSV file and returns a list of dictionaries.
    Assumes that the CSV file has a header row.
    """
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
