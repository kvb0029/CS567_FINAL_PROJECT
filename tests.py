import unittest
from datetime import datetime, timedelta
from CAS import CarAuctionSystem
class TestCarAuctionSystem(unittest.TestCase):

    def setUp(self):
        """Set up a CarAuctionSystem instance before each test."""
        self.system = CarAuctionSystem()
        self.system.register_user("test_user", "password123")
        self.system.login_user("test_user", "password123")

    def test_register_user(self):
        self.system.register_user("new_user", "new_password")
        self.assertIn("new_user", self.system.users)
        self.assertEqual(self.system.users["new_user"].password, "new_password")

    def test_login_user(self):
        self.system.logout()
        self.system.login_user("test_user", "password123")
        self.assertEqual(self.system.logged_in_user.username, "test_user")

    def test_list_car(self):
        future_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.system.list_car("Car1", "A fast car", 5000, future_time)
        self.assertEqual(len(self.system.cars), 1)
        self.assertEqual(self.system.cars[0].name, "Car1")

    def test_display_active_auctions(self):
        future_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.system.list_car("Car1", "A fast car", 5000, future_time)
        self.system.display_active_auctions()  # Ensure it runs without errors

    def test_place_bid(self):
        future_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.system.list_car("Car1", "A fast car", 5000, future_time)
        self.system.logout()
        self.system.register_user("bidder_user", "bidder_password")
        self.system.login_user("bidder_user", "bidder_password")
        self.system.place_bid("Car1", 6000)
        self.assertEqual(self.system.cars[0].highest_bid.amount, 6000)
        self.assertEqual(self.system.cars[0].highest_bid.user.username, "bidder_user")

    def test_close_expired_auctions(self):
        past_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.system.list_car("Car1", "A fast car", 5000, past_time)  # List a car with an expired time
        self.system.close_expired_auctions()  # Run the method to close expired auctions
        self.assertEqual(len(self.system.cars), 1)  # Ensure the car is still in the list
        self.assertEqual(self.system.cars[0].winner, None)  # Check that no bids were placed

    def test_cancel_listing(self):
        future_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.system.list_car("Car1", "A fast car", 5000, future_time)
        self.system.cancel_listing("Car1")
        self.assertEqual(len(self.system.cars), 0)

    def test_view_my_listings(self):
        future_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.system.list_car("Car1", "A fast car", 5000, future_time)
        self.system.view_my_listings()  # Ensure it runs without errors

    def test_extend_auction(self):
        future_time = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        self.system.list_car("Car1", "A fast car", 5000, future_time)
        self.system.extend_auction("Car1", 30)
        extended_time = self.system.cars[0].end_time
        self.assertGreater(extended_time, datetime.now() + timedelta(minutes=10))

    def test_generate_report(self):
        self.system.generate_report()  # Ensure it runs without errors

if __name__ == "__main__":
    unittest.main()
