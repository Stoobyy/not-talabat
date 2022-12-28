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
print('Dependencies and packages installed successfully!')
print()

print('Creating database and inserting test values...')
foodmcd = {"Big Mac": 19.00, "Big Mac Meal": 32.00, "McChicken": 18.00, "McChicken Meal": 31.00, "Cheeseburger": 9.00, "Veggie Surprise": 13.00, "Happy Meal": 12.50, "Water": 1.00, "Cola": 1.50, "Fries": 3.00}
detailsmcd = {"Location": "Sharjah City Center", "Phone": "+971 6 567 9263", "Website": "www.mcdonalds.ae", "Opening Hours": "9:00 - 21:00", "Cuisine": "Fast Food", "Rating": "4.5"}
foodpizza = {"Margherita": 25.00, "Pepperoni": 30.00, "Hawaiian Pizza": 35.00, "Veggie Delight": 30.00, "Water": 1.00, "Cola": 1.50, "Fries": 3.00}
detailspizza = {"Location": "Mirdif City Center", "Phone": "+971 4 323 3421", "Website": "www.pizzahut.ae", "Opening Hours": "10:00 - 23:00", "Cuisine": "Fast Food", "Rating": "4.5"}
detailsgazebo = {"Location": "Sahara Center", "Phone": "+971 4 121 0021", "Website": "www.gazebo.ae", "Opening Hours": "10:00 - 23:00", "Cuisine": "Fast Food", "Rating": "4.5"}
foodgazebo = {"Murgh Tikka Biryani": 45.00, "Paneer Tikka Biryani": 43.00, "Pulao" : 35.00, "Roti": 6.00, "Murgh Masala": 30.00, "Paneer Masala": 28.00, "Dal Makhani": 25.00, "Water": 1.00, "Cola": 1.50, "Fries": 3.00}

cursor.execute('drop database if exists zoop')
cursor.execute('create database zoop')
cursor.execute('use zoop')
cursor.execute('drop table if exists userdata')
cursor.execute('drop table if exists data')
cursor.execute('drop table if exists restaurants')
cursor.execute('create table userdata (password varchar(100), username varchar(100), name varchar(100))')
cursor.execute('create table data (username varchar(100), orders varchar(16000), payment text(1000));')
cursor.execute('create table restaurants (name varchar(100), menu varchar(10000), details varchar(1000))')
cursor.execute(f'insert into restaurants values("McDonalds", "{str(foodmcd)}", "{str(detailsmcd)}")')
cursor.execute(f'insert into restaurants values("Pizza Hut", "{str(foodpizza)}", "{str(detailspizza)}")')
cursor.execute(f'insert into restaurants values("Gazebo", "{str(foodgazebo)}", "{str(detailsgazebo)}")')
print('Database created successfully!')