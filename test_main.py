import unittest
from main import calc_avg_profit_margin, calc_discount_percentage


def rows_for_avg():
    return [
        {"Category": "Furniture", "Sales": "100", "Profit": "20"},
        {"Category": "Furniture", "Sales": "200", "Profit": "40"}, 
        {"Category": "Technology", "Sales": "50",  "Profit": "5"},  
    ]

def rows_for_avg_with_issues():
    return [
        {"Category": "Office Supplies", "Sales": "0",    "Profit": "10"},  
        {"Category": "Office Supplies", "Sales": "100",  "Profit": "25"},   
        {"Category": "Office Supplies", "Sales": "abc",  "Profit": "9"},    
        {"Category": "Office Supplies", "Sales": "200",  "Profit": "50"},   
    ]

def rows_for_discount_general_one_region():
    return [
        {"Region": "East", "Quantity": "2", "Discount": "0.1"},
        {"Region": "East", "Quantity": "3", "Discount": "0"},
    ] 

def rows_for_discount_two_regions_with_noise():
    return [
        {"Region": "East", "Quantity": "1", "Discount": "0.2"},
        {"Region": "East", "Quantity": "4", "Discount": "0"},
        {"Region": "East", "Quantity": "5", "Discount": "0.05"},
        {"Region": "West", "Quantity": "3", "Discount": "0"},
        {"Region": "West", "Quantity": "2", "Discount": "0.0"},
        {"Region": "West", "Quantity": "not_a_number", "Discount": "0.5"}, 
    ]

class TestCalcAvgProfitMargin(unittest.TestCase):
    def test_general_two_categories(self):
        data = rows_for_avg()
        res = calc_avg_profit_margin(data)
        self.assertIn("Furniture", res)
        self.assertIn("Technology", res)
        self.assertAlmostEqual(res["Furniture"], 0.2, places=6)
        self.assertAlmostEqual(res["Technology"], 0.1, places=6)

    def test_general_with_zero_sales_skipped(self):
        data = rows_for_avg_with_issues()
        res = calc_avg_profit_margin(data)
        self.assertIn("Office Supplies", res)
        self.assertAlmostEqual(res["Office Supplies"], 0.25, places=6)

    def test_edge_empty_input(self):
        res = calc_avg_profit_margin([])
        self.assertEqual(res, {})

    def test_edge_bad_values_all_skipped(self):
        bad = [
            {"Category": "A", "Sales": "x", "Profit": "1"},
            {"Category": "A", "Sales": "1", "Profit": "y"},
            {"Category": "A", "Sales": "0", "Profit": "0"},
        ]
        res = calc_avg_profit_margin(bad)
        self.assertEqual(res, {})


class TestCalcDiscountPercentage(unittest.TestCase):
    def test_general_one_region_ratios(self):
        data = rows_for_discount_general_one_region()
        res = calc_discount_percentage(data)
        self.assertIn("East", res)
        self.assertAlmostEqual(res["East"]["by_orders"], 0.5, places=6)
        self.assertAlmostEqual(res["East"]["by_quantity"], 0.4, places=6)
        self.assertEqual(res["East"]["total_orders"], 2)
        self.assertEqual(res["East"]["discounted_orders"], 1)
        self.assertEqual(res["East"]["total_quantity"], 5)
        self.assertEqual(res["East"]["discounted_quantity"], 2)

    def test_general_two_regions_with_noise(self):
        data = rows_for_discount_two_regions_with_noise()
        res = calc_discount_percentage(data)
        self.assertIn("East", res)
        self.assertAlmostEqual(res["East"]["by_orders"], 2/3, places=6)
        self.assertAlmostEqual(res["East"]["by_quantity"], 6/10, places=6)
        self.assertIn("West", res)
        self.assertAlmostEqual(res["West"]["by_orders"], 0.0, places=6)
        self.assertAlmostEqual(res["West"]["by_quantity"], 0.0, places=6)
        self.assertEqual(res["West"]["total_orders"], 2)
        self.assertEqual(res["West"]["discounted_orders"], 0)

    def test_edge_all_zero_discounts(self):
        data = [
            {"Region": "South", "Quantity": "1", "Discount": "0"},
            {"Region": "South", "Quantity": "2", "Discount": "0.0"},
        ]
        res = calc_discount_percentage(data)
        self.assertAlmostEqual(res["South"]["by_orders"], 0.0, places=6)
        self.assertAlmostEqual(res["South"]["by_quantity"], 0.0, places=6)

    def test_edge_bad_rows_skipped(self):
        data = [
            {"Region": "West", "Quantity": "x", "Discount": "0.2"},  
            {"Region": "West", "Quantity": "5", "Discount": "0.5"},  
        ]
        res = calc_discount_percentage(data)
        self.assertAlmostEqual(res["West"]["by_orders"], 1.0, places=6)
        self.assertAlmostEqual(res["West"]["by_quantity"], 1.0, places=6)
        self.assertEqual(res["West"]["total_orders"], 1)
        self.assertEqual(res["West"]["discounted_orders"], 1)
        self.assertEqual(res["West"]["total_quantity"], 5)
        self.assertEqual(res["West"]["discounted_quantity"], 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
