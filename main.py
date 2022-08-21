import os
import time
import requests
from sql import *
import random

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
data = retrieve(loginDetails)
time.sleep(2)
print('All done!')

print(f'Welcome back to {projectname} {check[1]}, what would you like to do today?')
print('1.Place an order\n2.View your orders\n3.View or change your account details\n4.Logout')
choice = input('Enter your choice: ')
if choice == '1':
    print('Please wait while we retrieve nearby restaurants...')
    time.sleep(2)
    restaurants = getRestaurants()
    print('All done! Here are the nearby restaurants')
    for restaurant in restaurants:
        details = eval(restaurant[2])
        menu = eval(restaurant[1])
        print(restaurant[0])
        print(f'Location: {details["Location"]}\nCuisine: {details["Cuisine"]}\nRating: {details["Rating"]}\nPhone: {details["Phone"]}\nWebsite: {details["Website"]}')
    choice = input('Which restaurant would like you to order from: ')
    print('\n')
        
    for restaurant in restaurants:
        if restaurant[0] == choice:
            menu = eval(restaurant[1])
            print('Menu:')
            for dish in menu:
                print(f'{dish}: {menu[dish]}')
            print('\n')
            print('\n')
            choice = input('Which dish would you like to order: ')
            print('\n')
            if choice in menu:
                quantity = input('How many would you like to order: ')
                payment = input('How would you like to pay?\n1.Cash on Delivery\n2.Pay Online\nEnter your choice: ')
                if payment == '1':
                    print('\n')
                    print(f'Thank you for your order of {choice} x {quantity}. Payment will be made upon delivery\nOrder Number: {len(eval(data[1]))+1}\nEstimated time of delivery: {random.randint(20,50)} minutes')
                elif payment == '2':
                    print('\n')
                    card = input('All sensitive information is stored securely.\nPlease enter your Card Number: ')
                    cardtype = 'Visa' if str(card)[0] == 4 else 'MasterCard'
                    print(f'Thank you for your order of {choice} x {quantity}. Payment has been made on your {cardtype} ending with {str(card)[12:]}\nOrder Number: {len(eval(data[1]))+1}\nEstimated time of delivery: {random.randint(20,50)} minutes')
                placeOrder(loginDetails, restaurant[0], choice, quantity)
            else:
                print('Dish not available')


