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



def calc_discount_percentage(data):
    stats = {}  

    for row in data:
        try:
            region = row["Region"]
            qty = int(row["Quantity"])
            

            discount = float(row["Discount"])
        except (KeyError, ValueError):
            continue

        if region not in stats:
            stats[region] = {
                "total_orders": 0,
                "discounted_orders": 0,
                "total_quantity": 0,
                "discounted_quantity": 0,
            }

        stats[region]["total_orders"] += 1
        stats[region]["total_quantity"] += qty

        if discount > 0:
            stats[region]["discounted_orders"] += 1
            stats[region]["discounted_quantity"] += qty

    result = {}
    for region, s in stats.items():
        by_orders = (s["discounted_orders"] / s["total_orders"]) if s["total_orders"] > 0 else 0.0
        by_quantity = (s["discounted_quantity"] / s["total_quantity"]) if s["total_quantity"] > 0 else 0.0
        result[region] = {
            "by_orders": by_orders,
            "by_quantity": by_quantity,
            "total_orders": s["total_orders"],
            "discounted_orders": s["discounted_orders"],
            "total_quantity": s["total_quantity"],
            "discounted_quantity": s["discounted_quantity"],
        }

    return result



if __name__ == "__main__":
    data = load_csv("SampleSuperstore.csv")

    avg_margin = calc_avg_profit_margin(data)
    for k, v in avg_margin.items():
        print(f"{k}: {v:.4f}")
        
    disc = calc_discount_percentage(data)
    for region, d in disc.items():
        print(
            f"{region}: discount_rate_by_orders={d['by_orders']*100:.2f}%  "
            f"discount_rate_by_quantity={d['by_quantity']*100:.2f}%  "
            f"(orders {d['discounted_orders']}/{d['total_orders']}, "
            f"quantity {d['discounted_quantity']}/{d['total_quantity']})"
        )
