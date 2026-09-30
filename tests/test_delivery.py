import unittest
from src.Delivery import calculate_delivery_cost

class TestDelivery(unittest.TestCase):

    def test_normal_delivery(self):
        cost, date = calculate_delivery_cost(2.0, 100, "обычный")
        self.assertEqual(cost, 700)
        self.assertEqual(date, "2026-09-04")

    def test_fragile_delivery(self):
        cost, date = calculate_delivery_cost(2.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_delivery(self):
        cost, date = calculate_delivery_cost(2.0, 100, "опасный")
        self.assertEqual(cost, 1700)

    def test_weight_5kg(self):
        cost1, date1 = calculate_delivery_cost(4.9, 100, "обычный")
        cost2, date2 = calculate_delivery_cost(5.0, 100, "обычный")
        cost3, date3 = calculate_delivery_cost(5.1, 100, "обычный")

        self.assertEqual(cost2, cost3)
        self.assertNotEqual(cost1, cost2)

    def test_express_price(self):
        cost1, date1 = calculate_delivery_cost(10.0, 1000, "обычный", is_express=False)
        cost2, date2 = calculate_delivery_cost(10.0, 1000, "обычный", is_express=True)

        self.assertGreater(cost2, cost1)

    def test_express_days(self):
        cost, date = calculate_delivery_cost(5.0, 100, "обычный", is_express=True)
        self.assertNotEqual(date, "2026-09-03")

    def test_weight_too_small(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_too_big(self):
        cost, date = calculate_delivery_cost(55.0, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_wrong_type(self):
        cost, date = calculate_delivery_cost(5.0, 100, "животное")
        self.assertEqual(cost, -1)

    def test_max_distance(self):
        cost, date = calculate_delivery_cost(5.0, 5000, "обычный")
        self.assertGreater(cost, 0)
        self.assertEqual(date, "2026-09-13")

if __name__ == '__main__':
    unittest.main()