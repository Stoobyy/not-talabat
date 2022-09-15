import os
import sys
import subprocess
import mysql.connector as sql

print('Installing required dependencies and packages...')
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'humanize', '--quiet'], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography', '--quiet'], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
print('Dependencies and packages installed successfully!')
print()
db = sql.connect(
    host = 'localhost',
    username = 'root',
    password = 'stooby',
)
cursor = db.cursor()
db.autocommit = True

print('Creating database and inserting test values...')
food = {"Big Mac": 19.00, "Big Mac Meal": 32.00, "McChicken": 18.00, "McChicken Meal": 31.00, "Cheeseburger": 9.00, "Veggie Surprise": 13.00, "Happy Meal": 12.50, "Water": 1.00, "Cola": 1.50, "Fries": 3.00}
details = {"Location": "Sharjah City Center", "Phone": "+971 4 4444 444", "Website": "www.restaurant.com", "Opening Hours": "9:00 - 21:00", "Cuisine": "Fast Food", "Rating": "4.5"}
cursor.execute('drop database if exists notTalabat')
cursor.execute('create database notTalabat')
cursor.execute('use notTalabat')
cursor.execute('drop table if exists userdata')
cursor.execute('drop table if exists data')
cursor.execute('drop table if exists restaurants')
cursor.execute('create table userdata (password varchar(100), username varchar(100), name varchar(100))')
cursor.execute('create table data (username varchar(100), orders varchar(16000), payment varchar(100));')
cursor.execute('create table restaurants (name varchar(100), menu varchar(10000), details varchar(1000))')
cursor.execute(f'insert into restaurants values("A", "{str(food)}", "{str(details)}")')
print('Database created successfully!')