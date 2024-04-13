import pymongo
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time
import requests

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["water_management"]
users_collection = db["users"]
water_logs_collection = db["water_logs"]
water_quality_logs_collection = db["water_quality_logs"]
feedback_collection = db["feedback"]
energy_logs_collection = db["energy_logs"]

# User management
def create_user(username, password):
    user = {"username": username, "password": password, "water_usage": [], "language": "en", "units": "liters"}
    users_collection.insert_one(user)
    return user

def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and user["password"] == password:
        return user
    return None

# Water usage logging
def log_water_usage(user_id, amount):
    log_entry = {"user_id": user_id, "amount": amount, "timestamp": datetime.now()}
    water_logs_collection.insert_one(log_entry)
    users_collection.update_one({"_id": user_id}, {"$push": {"water_usage": log_entry}})

# Water usage analysis
def get_daily_water_usage(user_id):
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    logs = water_logs_collection.find({"user_id": user_id, "timestamp": {"$gte": yesterday, "$lt": today}})
    return sum(log["amount"] for log in logs)

def get_weekly_water_usage(user_id):
    today = datetime.now()
    last_week = today - timedelta(days=7)
    logs = water_logs_collection.find({"user_id": user_id, "timestamp": {"$gte": last_week, "$lt": today}})
    return sum(log["amount"] for log in logs)

def get_monthly_water_usage(user_id):
    today = datetime.now()
    last_month = today - timedelta(days=30)
    logs = water_logs_collection.find({"user_id": user_id, "timestamp": {"$gte": last_month, "$lt": today}})
    return sum(log["amount"] for log in logs)

def print_water_usage_stats(user):
    daily_usage = get_daily_water_usage(user["_id"])
    weekly_usage = get_weekly_water_usage(user["_id"])
    monthly_usage = get_monthly_water_usage(user["_id"])
    print(f"Daily water usage: {daily_usage} {user['units']}")
    print(f"Weekly water usage: {weekly_usage} {user['units']}")
    print(f"Monthly water usage: {monthly_usage} {user['units']}")

# Notification system
def check_water_usage_limit(user, limit):
    daily_usage = get_daily_water_usage(user["_id"])
    if daily_usage > limit:
        print(f"Warning: {user['username']} has exceeded the daily water usage limit of {limit} {user['units']}.")
        # Send notification to the user
        send_notification(user["username"], f"You have exceeded your daily water usage limit of {limit} {user['units']}.")

def send_notification(username, message):
    # Implement notification system, e.g., email, push notification, etc.
    print(f"Notification sent to {username}: {message}")

# Water conservation tips
def get_water_conservation_tips(user):
    tips = [
        "Take shorter showers",
        "Turn off the tap while brushing your teeth",
        "Use a water-efficient dishwasher",
        "Water your garden in the early morning or evening"
    ]
    return tips

# Mobile app integration
def log_water_usage_from_mobile(user_id, amount):
    log_water_usage(user_id, amount)
    print("Water usage logged successfully.")

# Water quality monitoring
def log_water_quality(user_id, quality_score):
    quality_log = {"user_id": user_id, "quality_score": quality_score, "timestamp": datetime.now()}
    water_quality_logs_collection.insert_one(quality_log)

# Data export and sharing
def export_water_usage_data(user_id, file_format="csv"):
    user = users_collection.find_one({"_id": user_id})
    if file_format == "csv":
        # Export data to a CSV file
        with open(f"{user['username']}_water_usage.csv", "w", newline="") as csvfile:
            for log in user["water_usage"]:
                csvfile.write(f"{log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')},{log['amount']},{user['units']}\n")
        print(f"Water usage data exported to {user['username']}_water_usage.csv")
    elif file_format == "json":
        # Export data to a JSON file
        import json
        with open(f"{user['username']}_water_usage.json", "w") as jsonfile:
            json.dump(user["water_usage"], jsonfile)
        print(f"Water usage data exported to {user['username']}_water_usage.json")
    else:
        print("Invalid file format.")

# Localization and units conversion
def set_user_preferences(user_id, language, units):
    users_collection.update_one({"_id": user_id}, {"$set": {"language": language, "units": units}})

# Automated water usage logging
def integrate_iot_device(user_id):
    # Connect to an IoT device and automatically log water usage
    device_id = "123456789"
    while True:
        usage = get_water_usage_from_iot_device(device_id)
        log_water_usage(user_id, usage)
        time.sleep(60)  # Check for water usage every minute

def get_water_usage_from_iot_device(device_id):
    # Implement logic to fetch water usage data from the IoT device
    return 10.0  # Dummy data, replace with actual device integration

# Weather integration
def get_weather_data(location):
    # Integrate with a weather API and fetch weather data for the given location
    api_key = "your_weather_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data

# Feedback and rating system
def submit_feedback(user_id, feedback, rating):
    feedback_data = {"user_id": user_id, "feedback": feedback, "rating": rating, "timestamp": datetime.now()}
    feedback_collection.insert_one(feedback_data)

# Energy usage tracking
def log_energy_usage(user_id, energy_usage):
    energy_log = {"user_id": user_id, "energy_usage": energy_usage, "timestamp": datetime.now()}
    energy_logs_collection.insert_one(energy_log)

# Example usage
create_user("user1", "password1")
user = authenticate_user("user1", "password1")
if user:
    log_water_usage(user["_id"], 50.0)
    print_water_usage_stats(user)
    check_water_usage_limit(user, 100)
    print("Water conservation tips:")
    for tip in get_water_conservation_tips(user):
        print(f"- {tip}")
    log_water_quality(user["_id"], 8.5)
    export_water_usage_data(user["_id"], "csv")
    set_user_preferences(user["_id"], "en", "liters")
    integrate_iot_device(user["_id"])
    weather_data = get_weather_data("New York")
    print(f"Current weather in New York: {weather_data['weather'][0]['description']}, {weather_data['main']['temp']}°C")
    submit_feedback(user["_id"], "Great app!", 4)
    log_energy_usage(user["_id"], 25.0)
else:
    print("Invalid username or password.")