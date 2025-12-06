import unittest
import datetime

from assignment2.sales_analysis import (
    total_revenue,
    revenue_by_store,
    revenue_by_time_of_day,
    popular_items_by_time_of_day,
    member_vs_non_member_revenue,
    average_member_visits_per_week,
)


class SalesAnalysisTests(unittest.TestCase):
    def setUp(self):
        # Small in-memory dataset to test all functions.
        # Dates chosen so weeks differ for average_member_visits_per_week.
        self.sample_sales = [
            {
                "order_id": "1",
                "date": datetime.date(2025, 11, 3),   # week 45
                "time_of_day": "morning",
                "store": "Sunnyvale",
                "item_name": "Latte",
                "quantity": 2,
                "price": 4.5,
                "is_member": True,
                "member_id": "M1",
            },
            {
                "order_id": "2",
                "date": datetime.date(2025, 11, 3),   # same day as above
                "time_of_day": "afternoon",
                "store": "Sunnyvale",
                "item_name": "Muffin",
                "quantity": 1,
                "price": 3.0,
                "is_member": False,
                "member_id": None,
            },
            {
                "order_id": "3",
                "date": datetime.date(2025, 11, 10),  # week 46
                "time_of_day": "morning",
                "store": "Mountainview",
                "item_name": "Latte",
                "quantity": 1,
                "price": 4.5,
                "is_member": True,
                "member_id": "M1",
            },
            {
                "order_id": "4",
                "date": datetime.date(2025, 11, 10),  # week 46
                "time_of_day": "night",
                "store": "Palo Alto",
                "item_name": "Tea",
                "quantity": 3,
                "price": 2.0,
                "is_member": True,
                "member_id": "M2",
            },
            {
                "order_id": "5",
                "date": datetime.date(2025, 11, 17),  # week 47
                "time_of_day": "morning",
                "store": "Sunnyvale",
                "item_name": "Latte",
                "quantity": 1,
                "price": 4.5,
                "is_member": True,
                "member_id": "M1",
            },
            {
                "order_id": "6",
                "date": datetime.date(2025, 11, 17),  # week 47
                "time_of_day": "night",
                "store": "Sunnyvale",
                "item_name": "Latte",
                "quantity": 1,
                "price": 4.5,
                "is_member": False,
                "member_id": None,
            },
        ]
        # Handy: total revenue we expect from these rows:
        # Row1: 2 * 4.5 = 9.0
        # Row2: 1 * 3.0 = 3.0
        # Row3: 1 * 4.5 = 4.5
        # Row4: 3 * 2.0 = 6.0
        # Row5: 1 * 4.5 = 4.5
        # Row6: 1 * 4.5 = 4.5
        # Total = 31.5

    def test_total_revenue(self):
        self.assertEqual(total_revenue(self.sample_sales), 31.5)

    def test_revenue_by_store(self):
        result = revenue_by_store(self.sample_sales)
        # Sunnyvale: rows 1,2,5,6 → 9 + 3 + 4.5 + 4.5 = 21.0
        # Mountainview: row 3 → 4.5
        # Palo Alto: row 4 → 6.0
        self.assertEqual(result["Sunnyvale"], 21.0)
        self.assertEqual(result["Mountainview"], 4.5)
        self.assertEqual(result["Palo Alto"], 6.0)

    def test_revenue_by_time_of_day(self):
        result = revenue_by_time_of_day(self.sample_sales)
        # morning: rows 1,3,5 → 9 + 4.5 + 4.5 = 18.0
        # afternoon: row 2 → 3.0
        # night: rows 4,6 → 6 + 4.5 = 10.5
        self.assertEqual(result["morning"], 18.0)
        self.assertEqual(result["afternoon"], 3.0)
        self.assertEqual(result["night"], 10.5)

    def test_popular_items_by_time_of_day(self):
        result = popular_items_by_time_of_day(self.sample_sales, top_n=3)
        # morning:
        #   Latte: row1 (2) + row3 (1) + row5 (1) = 4
        morning_items = dict(result["morning"])
        self.assertEqual(morning_items["Latte"], 4)

        # afternoon:
        afternoon_items = dict(result["afternoon"])
        self.assertEqual(afternoon_items["Muffin"], 1)

        # night:
        night_items = dict(result["night"])
        # Tea: 3 (row 4), Latte: 1 (row 6)
        self.assertEqual(night_items["Tea"], 3)
        self.assertEqual(night_items["Latte"], 1)

    def test_member_vs_non_member_revenue(self):
        result = member_vs_non_member_revenue(self.sample_sales)
        # members: rows 1,3,4,5 → 9 + 4.5 + 6 + 4.5 = 24.0
        # non-members: rows 2,6 → 3 + 4.5 = 7.5
        self.assertEqual(result["member"], 24.0)
        self.assertEqual(result["non_member"], 7.5)

    def test_average_member_visits_per_week(self):
        # Member M1: rows 1 (week45), 3 (week46), 5 (week47)
        #   → 3 orders in 3 weeks → 1.0 visits/week
        # Member M2: row 4 (week46)
        #   → 1 order in 1 week → 1.0 visits/week
        # Average across members = (1.0 + 1.0) / 2 = 1.0
        avg = average_member_visits_per_week(self.sample_sales)
        self.assertAlmostEqual(avg, 1.0)


if __name__ == "__main__":
    unittest.main()
