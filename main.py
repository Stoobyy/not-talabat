import mysql.connector as sql
import os
import time
import requests
import tkinter
import customtkinter 
from sql import *

db = sql.connect(
    host = 'localhost',
    username = 'root',
    password = 'stooby',
    database = 'notTalabat'
)
projectname = 'Not Talabat'

print(f'Welcome to {projectname}\nYour favourite dishes and delicacies delivered to your doorsteps!')
loginDetails = input('Sign in or sign up with email\nEmail address: ')
check = check(loginDetails)
if check[0]:
    while True:
        password = input(f'Welcome back {check[1]}\nPlease enter your password to login: ')
        if login(loginDetails, password):
            print('Login successful')
            break
        else:
            print('Login unsuccessful, please try again')
else:
    print('Hello new user, please sign up')
    name = input('Whats your name: ')
    password = input('Enter a safe and secure password: ')
    register(loginDetails, password, name)
    print('Registration successful!\nAuto-Login successful')

print('Hold on while we fetch your details...')
time.sleep(2)
userdata = retrieve(loginDetails)
print('All done!')

print(f'Welcome back to {projectname} {userdata[1]}, what would you like to do today?')
print('1.Place an order\n2.View your orders\n3.View or change your account details\n4.Logout')
choice = input('Enter your choice: ')
if choice == '1':
    print('Please wait while we retrieve nearby restaurants...')
    time.sleep(2)
    
