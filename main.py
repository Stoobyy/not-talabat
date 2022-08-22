import os
import time
import requests
import humanize
from datetime import datetime, timedelta
from sql import *
import random

projectname = 'Not Talabat'

print(f'Welcome to {projectname}\nYour favourite dishes and delicacies delivered to your doorsteps!')
loginDetails = input('Sign in or sign up with email\nEmail address: ')
_check = check(loginDetails)
if _check[0]:
    while True:
        password = input(f'Welcome back {_check[1]}\nPlease enter your password to login: ')
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
print('All done!')

print(f'Welcome back to {projectname} {_check[1]}, what would you like to do today?')
print('1.Place an order\n2.View your orders\n3.View or change your account details\n4.Logout')
choice = input('Enter your choice: ')
if choice == '1':
    print('Please wait while we retrieve nearby restaurants...')
    
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
                deliveryTime = random.randint(20,50)*60
                unix = (datetime.now()+ timedelta(seconds=deliveryTime)).timestamp()
                if payment == '1':
                    print('\n')
                    print(f'Thank you for your order of {choice} x {quantity}. Payment will be made upon delivery\nOrder Number: {len(eval(data[1]))+1}\nEstimated time of delivery: {deliveryTime} minutes')
                elif payment == '2':
                    print('\n')
                    card = input('All sensitive information is stored securely.\nPlease enter your Card Number: ')
                    cvv = input('Please enter your CVV: ')
                    expiry = input('Please enter your Expiry Date in the format MM/YY: ')
                    cardtype = 'Visa' if str(card)[0] == 4 else 'MasterCard'
                    print('\n')
                    addPayment(loginDetails, card, cvv, expiry, cardtype)
                    print(f'Thank you for your order of {choice} x {quantity}. Payment has been made on your {cardtype} ending with {str(card)[12:]}\nOrder Number: {len(eval(data[1]))+1}\nEstimated time of delivery: {deliveryTime//60} minutes')
                placeOrder(loginDetails, restaurant[0], choice, quantity, unix)
                data = retrieve(loginDetails)[1]
            else:
                print('Dish not available')
elif choice == '2':
    print('\n')
    print('Your orders:')
    orders = viewOrders(loginDetails)[1]
    for order in orders:
        order = eval(order)
        for i in range(1,len(order)+1):
            j = str(i)
            deliveryStatus = 'Delivered' if order[j][3] < datetime.now().timestamp() else 'Delivering in'
            print(f'Order Number {i+1}\nRestaurant: {order[j][0]}\nDish: {order[j][1]}\nQuantity: {order[j][2]}\n{deliveryStatus} {humanize.naturaltime(datetime.fromtimestamp(order[j][3]))}')
            print('\n')

elif choice == '3':
    print('\n')
    userDetails = retrieveDetails(loginDetails)
    _check = retrieve(loginDetails)
    if _check[2] != '{}':
        card = eval(_check[2])
        cardDetails = f'{card["cardtype"]} ending with {card["card"][12:]} expiring on {card["expiry"]}'
    else:
        cardDetails = None
    print(f'Your account details:\nName: {userDetails[2]}\nEmail: {userDetails[1]}\nCard: {cardDetails}')
    print('\n')
    choice = input('Would you like to change your password?\n1.Yes\n2.No\nEnter your choice: ')
    if choice == '1':
        password = input('Enter your new password: ')
        changePassword(loginDetails, password)
        print('Password changed successfully')

elif choice == '4':
    print('\n')
    print('Logging out...')
    time.sleep(2)
    print('Logged out successfully')
    exit()

else:
    print('Invalid choice')
    exit()
