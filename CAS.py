import datetime


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.listed_cars = []
        self.bids = []


class Car:
    def __init__(self, name, description, min_price, end_time, seller):
        self.name = name
        self.description = description
        self.min_price = min_price
        self.end_time = end_time
        self.seller = seller
        self.bids = []
        self.highest_bid = None
        self.winner = None


class Bid:
    def __init__(self, user, amount):
        self.user = user
        self.amount = amount


class CarAuctionSystem:
    def __init__(self):
        self.users = {}
        self.logged_in_user = None
        self.cars = []

    def register_user(self, username, password):
        if username in self.users:
            print("Username already exists. Please choose a different username.")
            return
        self.users[username] = User(username, password)
        print("User registered successfully!")

    def login_user(self, username, password):
        if username not in self.users:
            print("Username not found. Please register first.")
            return
        if self.users[username].password != password:
            print("Incorrect password.")
            return
        self.logged_in_user = self.users[username]
        print(f"Welcome, {username}! You are now logged in.")

    def logout(self):
        if not self.logged_in_user:
            print("You are not logged in.")
            return
        print(f"Goodbye, {self.logged_in_user.username}! You have been logged out.")
        self.logged_in_user = None

    def list_car(self, name, description, min_price, end_time):
        if not self.logged_in_user:
            print("You must log in to list a car.")
            return
        try:
            end_time_obj = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            if end_time_obj <= datetime.datetime.now():
                print("End time must be in the future.")
                return
        except ValueError:
            print("Invalid end time format. Use YYYY-MM-DD HH:MM:SS.")
            return

        car = Car(name, description, min_price, end_time_obj, self.logged_in_user)
        self.cars.append(car)
        self.logged_in_user.listed_cars.append(car)
        print(f"Car '{name}' has been listed successfully!")

    def display_active_auctions(self):
        print("\n=== Active Car Auctions ===")
        now = datetime.datetime.now()
        active = False
        for car in self.cars:
            if car.end_time > now:
                active = True
                print(f"Car: {car.name}, Description: {car.description}, Minimum Price: {car.min_price}, "
                      f"Ends: {car.end_time}, Highest Bid: {car.highest_bid.amount if car.highest_bid else 'None'}")
        if not active:
            print("No active auctions at the moment.")
        print()

    def place_bid(self, car_name, amount):
        if not self.logged_in_user:
            print("You must log in to place a bid.")
            return
        now = datetime.datetime.now()
        for car in self.cars:
            if car.name == car_name:
                if now >= car.end_time:
                    print("This auction has already ended.")
                    return
                if amount < car.min_price:
                    print("Your bid must be at least the minimum price.")
                    return
                if car.highest_bid and amount <= car.highest_bid.amount:
                    print("Your bid must be higher than the current highest bid.")
                    return
                bid = Bid(self.logged_in_user, amount)
                car.bids.append(bid)
                car.highest_bid = bid
                self.logged_in_user.bids.append(bid)
                print(f"Your bid of {amount} has been placed on '{car_name}'.")
                return
        print("Car not found.")

    def close_expired_auctions(self):
        now = datetime.datetime.now()
        for car in self.cars:
            if car.end_time <= now and not car.winner:
                if car.highest_bid:
                    car.winner = car.highest_bid.user
                    print(f"Auction closed for '{car.name}'. Winner: {car.winner.username} with bid: {car.highest_bid.amount}")
                else:
                    print(f"Auction closed for '{car.name}'. No bids were placed.")

    def display_winners(self):
        print("\n=== Auction Winners ===")
        winners_found = False
        for car in self.cars:
            if car.winner:
                winners_found = True
                print(f"Car: {car.name}, Winner: {car.winner.username}, Winning Bid: {car.highest_bid.amount}")
        if not winners_found:
            print("No auctions have winners yet.")
        print()

def search_cars(self, keyword):
    print(f"\n=== Search Results for '{keyword}' ===")
    results_found = False
    for car in self.cars:
        if keyword.lower() in car.name.lower() or keyword.lower() in car.description.lower():
            results_found = True
            print(f"Car: {car.name}, Description: {car.description}, Minimum Price: {car.min_price}")
    if not results_found:
        print("No cars found matching your search criteria.")
    print()

def cancel_listing(self, car_name):
    if not self.logged_in_user:
        print("You must log in to cancel a listing.")
        return
    for car in self.cars:
        if car.name == car_name and car.seller == self.logged_in_user:
            if car.bids:
                print("You cannot cancel the listing because there are already bids.")
                return
            self.cars.remove(car)
            self.logged_in_user.listed_cars.remove(car)
            print(f"Listing for '{car_name}' has been successfully canceled.")
            return
    print("Car not found or you do not have permission to cancel this listing.")

def view_my_listings(self):
    if not self.logged_in_user:
        print("You must log in to view your listings.")
        return
    print(f"\n=== Listings by {self.logged_in_user.username} ===")
    if not self.logged_in_user.listed_cars:
        print("You have not listed any cars.")
        return
    for car in self.logged_in_user.listed_cars:
        print(f"Car: {car.name}, Description: {car.description}, Minimum Price: {car.min_price}, Ends: {car.end_time}")
    print()

def extend_auction(self, car_name, extra_minutes):
    if not self.logged_in_user:
        print("You must log in to extend an auction.")
        return
    for car in self.cars:
        if car.name == car_name and car.seller == self.logged_in_user:
            car.end_time += datetime.timedelta(minutes=extra_minutes)
            print(f"The auction for '{car_name}' has been extended by {extra_minutes} minutes.")
            return
    print("Car not found or you do not have permission to extend this auction.")

def leave_review(self, car_name, review):
    if not self.logged_in_user:
        print("You must log in to leave a review.")
        return
    for car in self.cars:
        if car.name == car_name and car.winner == self.logged_in_user:
            print(f"Review for {car.seller.username}: {review}")
            return
    print("You can only leave reviews for auctions you have won.")

def generate_report(self):
    print("\n=== Auction Report ===")
    total_sales = 0
    for car in self.cars:
        if car.highest_bid:
            total_sales += car.highest_bid.amount
            print(f"Car: {car.name}, Sold to: {car.winner.username}, Price: {car.highest_bid.amount}")
    print(f"Total Sales: {total_sales}")
    print()

def list_car_with_category(self, name, description, min_price, end_time, category):
    if not self.logged_in_user:
        print("You must log in to list a car.")
        return
    try:
        end_time_obj = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        if end_time_obj <= datetime.datetime.now():
            print("End time must be in the future.")
            return
    except ValueError:
        print("Invalid end time format. Use YYYY-MM-DD HH:MM:SS.")
        return

    car = Car(name, description, min_price, end_time_obj, self.logged_in_user)
    car.category = category
    self.cars.append(car)
    self.logged_in_user.listed_cars.append(car)
    print(f"Car '{name}' in category '{category}' has been listed successfully!")

def send_notification(self, user, message):
    print(f"Notification for {user.username}: {message}")

def block_user(self, username):
    if username in self.users:
        self.users.pop(username)
        print(f"User '{username}' has been blocked.")
    else:
        print("User not found.")

def set_buy_now_price(self, car_name, buy_now_price):
    if not self.logged_in_user:
        print("You must log in to set a buy-now price.")
        return
    for car in self.cars:
        if car.name == car_name and car.seller == self.logged_in_user:
            car.buy_now_price = buy_now_price
            print(f"Buy-now price of {buy_now_price} has been set for '{car_name}'.")
            return
    print("Car not found or you do not have permission to set a buy-now price.")

def process_payment(self, car_name):
    if not self.logged_in_user:
        print("You must log in to process a payment.")
        return
    for car in self.cars:
        if car.name == car_name and car.winner == self.logged_in_user:
            print(f"Payment of {car.highest_bid.amount} has been processed for '{car_name}'.")
            return
    print("Car not found or you are not the winner of this auction.")

def main():
    system = CarAuctionSystem()

    while True:
        print("\n=== Car Auction System ===")
        print("1. Register")
        print("2. Login")
        print("3. Logout")
        print("4. List a Car for Auction")
        print("5. Display Active Auctions")
        print("6. Place a Bid")
        print("7. Close Expired Auctions")
        print("8. Display Winners")
        print("9. Search for Cars")
        print("10. View My Listings")
        print("11. Cancel Listing")
        print("12. Leave a Review")
        print("13. Generate Report")
        print("14. Extend Auction Time")
        print("15. Set Buy Now Price")
        print("16. Process Payment")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            system.register_user(username, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            system.login_user(username, password)
        elif choice == "3":
            system.logout()
        elif choice == "4":
            name = input("Enter car name: ")
            description = input("Enter car description: ")
            min_price = float(input("Enter minimum price: "))
            end_time = input("Enter auction end time (YYYY-MM-DD HH:MM:SS): ")
            system.list_car(name, description, min_price, end_time)
        elif choice == "5":
            system.display_active_auctions()
        elif choice == "6":
            car_name = input("Enter car name to bid on: ")
            amount = float(input("Enter your bid amount: "))
            system.place_bid(car_name, amount)
        elif choice == "7":
            system.close_expired_auctions()
        elif choice == "8":
            system.display_winners()
        elif choice == "9":
            keyword = input("Enter search keyword: ")
            system.search_cars(keyword)
        elif choice == "10":
            system.view_my_listings()
        elif choice == "11":
            car_name = input("Enter car name to cancel listing: ")
            system.cancel_listing(car_name)
        elif choice == "12":
            car_name = input("Enter car name to leave review: ")
            review = input("Enter your review: ")
            system.leave_review(car_name, review)
        elif choice == "13":
            system.generate_report()
        elif choice == "14":
            car_name = input("Enter car name to extend auction: ")
            extra_minutes = int(input("Enter extra minutes to extend: "))
            system.extend_auction(car_name, extra_minutes)
        elif choice == "15":
            car_name = input("Enter car name to set buy now price: ")
            buy_now_price = float(input("Enter buy now price: "))
            system.set_buy_now_price(car_name, buy_now_price)
        elif choice == "16":
            car_name = input("Enter car name to process payment: ")
            system.process_payment(car_name)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
