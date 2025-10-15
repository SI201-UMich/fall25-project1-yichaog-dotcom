import csv

def load_csv(file):
    """
    Read the CSV file into a list of dictionaries.
    Parameters:
        file (str): path to the CSV file
    Returns:
        list[dict]: dataset containing each row as a dictionary
    """
    dataset = []
    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dataset.append(row)
    return dataset

