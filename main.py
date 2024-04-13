import pymongo
from datetime import datetime

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["water_management"]
collection = db["water_logs"]

def log_water_usage(amount):
    # Log water usage with timestamp
    log_entry = {"amount": amount, "timestamp": datetime.now()}
    collection.insert_one(log_entry)

def get_water_usage():
    # Get total water usage
    total_usage = sum([entry["amount"] for entry in collection.find()])
    return total_usage

def main():
    while True:
        print("1. Log water usage")
        print("2. View total water usage")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Enter the amount of water used (in liters): "))
            log_water_usage(amount)
            print("Water usage logged successfully.")
        elif choice == "2":
            total_usage = get_water_usage()
            print(f"Total water usage: {total_usage} liters")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
