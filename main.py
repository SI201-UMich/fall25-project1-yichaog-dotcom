import csv

def load_csv(file):
    """
    Read the CSV file into a list of dictionaries.
    Parameters:
        CSV file.
    Returns:
        list[dict]: dataset containing each row as a dictionary
    """
    dataset = []
    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dataset.append(row)
    return dataset


if __name__ == "__main__":
    data = load_csv("SampleSuperstore.csv")
    print(f"Total rows: {len(data)}")
    print("Example row:", data[0])








def calc_avg_profit_margin(data):
    """
    Calculate average profit margin per category.
    Parameters:
        Data from CSV.
    Returns:
        dict: {Category: average profit margin}
    """
    category_margin = {}   
    category_count = {}    

    for row in data:
        try:
            category = row["Category"]
            sales = float(row["Sales"])
            profit = float(row["Profit"])

            if sales > 0:
                margin = profit / sales
                category_margin[category] = category_margin.get(category, 0) + margin
                category_count[category] = category_count.get(category, 0) + 1
        except (ValueError, KeyError):
            continue  
    avg_margin = {}
    for category in category_margin:
        avg_margin[category] = category_margin[category] / category_count[category]

    return avg_margin

if __name__ == "__main__":
    data = load_csv("SampleSuperstore.csv")
    results = calc_avg_profit_margin(data)
    for k, v in results.items():
        print(f"{k}: {v:.4f}")







