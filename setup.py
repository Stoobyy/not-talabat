import os
import sys
import subprocess
import mysql.connector as sql
import json

with open('sqlDetails.json', 'w') as f:
    host = input('Enter the host address: ')
    username = input('Enter the username: ')
    password = input('Enter the password: ')
    json.dump({'host': host, 'username': username, 'password': password}, f)

db = sql.connect(
    host = host,
    username = username,
    password = password
)

cursor = db.cursor()
db.autocommit = True

print('Installing required dependencies and packages...')
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'humanize', '--quiet'], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pwinput', '--quiet'], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography', '--quiet'], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'rich', '--quiet'], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
print('Dependencies and packages installed successfully!')
print()

print('Creating database and inserting test values...')

# -----------------------
# Restaurant Menus & Details
# -----------------------

# 1. Grana Pizzeria By Abramatt (Pizza / Italian)
food_grana = {
    "Mineral Water": 20.00,
    "Garlic Bread": 120.00,
    "Bruschetta": 150.00,
    "Mozzarella Sticks": 180.00,
    "Margherita Pizza": 350.00,
    "Smoked Chicken Pesto Pizza": 450.00,
    "Tiramisu": 220.00
}
details_grana = {
    "Location": "Panampilly Nagar, Kochi",
    "Phone": "+91 484 1234567",
    "Website": "www.granapizzeria.com",
    "Opening Hours": "11:00 - 23:00",
    "Cuisine": "Italian / Pizza",
    "Rating": "4.6"
}

# 2. Mash Restocafe (Café)
food_mash = {
    "Mineral Water": 20.00,
    "Cold Coffee": 150.00,
    "French Fries": 120.00,
    "Fish Fingers": 220.00,
    "Soup of the Day": 150.00,
    "Burger": 280.00,
    "Pasta Alfredo": 300.00
}
details_mash = {
    "Location": "Panampilly Nagar, Kochi",
    "Phone": "+91 484 2233445",
    "Website": "www.mashrestocafe.com",
    "Opening Hours": "10:00 - 23:00",
    "Cuisine": "Café / Continental",
    "Rating": "4.5"
}

# 3. P60 (Pizza / Café)
food_p60 = {
    "Mineral Water": 20.00,
    "Passion Lemonade": 100.00,
    "Garlic Bread": 120.00,
    "Soup of the Day": 150.00,
    "Italian Pizza": 400.00,
    "Lasagna": 350.00,
    "Tiramisu": 200.00
}
details_p60 = {
    "Location": "Panampilly Nagar, Kochi",
    "Phone": "+91 484 3344556",
    "Website": "www.p60cafe.com",
    "Opening Hours": "12:00 - 23:00",
    "Cuisine": "Pizza / Italian / Café",
    "Rating": "4.4"
}

# 4. Happy Cup (Casual Café / Street Food)
food_happy = {
    "Mineral Water": 20.00,
    "Soft Drink": 40.00,
    "Samosa": 50.00,
    "Chaat": 100.00,
    "Kebab": 180.00,
    "Butter Chicken with Naan": 300.00,
    "Chole Bhature": 150.00
}
details_happy = {
    "Location": "Panampilly Nagar, Kochi",
    "Phone": "+91 484 4455667",
    "Website": "www.happycupcafe.com",
    "Opening Hours": "09:00 - 22:00",
    "Cuisine": "Café / Indian Street Food",
    "Rating": "4.3"
}

# 5. Gokul Oottupura (South Indian Veg)
food_gokul = {
    "Mineral Water": 20.00,
    "Idli": 40.00,
    "Dosa": 60.00,
    "Vada": 50.00,
    "Meals (Veg Thali)": 120.00,
    "Uttapam": 80.00,
    "Filter Coffee": 40.00
}
details_gokul = {
    "Location": "Panampilly Nagar, Kochi",
    "Phone": "+91 484 5566778",
    "Website": "www.gokuloottupura.com",
    "Opening Hours": "07:00 - 22:00",
    "Cuisine": "South Indian (Vegetarian)",
    "Rating": "4.4"
}

# 6. 1947 Indian Restaurant (North Indian)
food_1947 = {
    "Mineral Water": 20.00,
    "Paneer Tikka": 220.00,
    "Chicken Tandoori": 280.00,
    "Dal Makhani": 180.00,
    "Butter Naan": 40.00,
    "Chicken Biryani": 260.00,
    "Gulab Jamun": 90.00
}
details_1947 = {
    "Location": "Panampilly Nagar, Kochi",
    "Phone": "+91 484 6677889",
    "Website": "www.1947restaurant.com",
    "Opening Hours": "12:00 - 23:00",
    "Cuisine": "North Indian",
    "Rating": "4.5"
}

# 7. Zaatar Restaurant (Arabic / Middle Eastern)
food_zaatar = {
    "Mineral Water": 20.00,
    "Hummus with Pita": 150.00,
    "Falafel": 180.00,
    "Shawarma Roll": 200.00,
    "Chicken Mandi": 350.00,
    "Mixed Grill Platter": 480.00,
    "Baklava": 200.00
}
details_zaatar = {
    "Location": "Panampilly Nagar, Kochi",
    "Phone": "+91 484 7788990",
    "Website": "www.zaatarcafe.com",
    "Opening Hours": "11:00 - 23:00",
    "Cuisine": "Arabic / Middle Eastern",
    "Rating": "4.6"
}

# -----------------------
# Database Setup
# -----------------------
cursor.execute('drop database if exists zoop')
cursor.execute('create database zoop')
cursor.execute('use zoop')
cursor.execute('drop table if exists userdata')
cursor.execute('drop table if exists data')
cursor.execute('drop table if exists restaurants')
cursor.execute('create table userdata (password varchar(100), username varchar(100), name varchar(100))')
cursor.execute('create table data (username varchar(100), orders varchar(16000), payment text(1000));')
cursor.execute('create table restaurants (name varchar(100), menu varchar(10000), details varchar(1000))')

# Insert all 7 restaurants
cursor.execute(f'insert into restaurants values("Grana Pizzeria", "{str(food_grana)}", "{str(details_grana)}")')
cursor.execute(f'insert into restaurants values("Mash Restocafe", "{str(food_mash)}", "{str(details_mash)}")')
cursor.execute(f'insert into restaurants values("P60", "{str(food_p60)}", "{str(details_p60)}")')
cursor.execute(f'insert into restaurants values("Happy Cup", "{str(food_happy)}", "{str(details_happy)}")')
cursor.execute(f'insert into restaurants values("Gokul Oottupura", "{str(food_gokul)}", "{str(details_gokul)}")')
cursor.execute(f'insert into restaurants values("1947 Restaurant", "{str(food_1947)}", "{str(details_1947)}")')
cursor.execute(f'insert into restaurants values("Zaatar Restaurant", "{str(food_zaatar)}", "{str(details_zaatar)}")')

print('Database created successfully with 7 restaurants!')
