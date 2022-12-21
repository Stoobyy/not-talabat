#Importing required modules
import os
import time
import requests
import humanize
from datetime import datetime, timedelta
from sql import *
import random
import pwinput

projectname = 'Zoop'

#Login screen function
def loginscreen():
    global new
    global _check
    global data
    global loginDetails

    os.system('cls')
    print(f'Welcome to {projectname}\nYour favourite dishes and delicacies delivered to your doorsteps!')
    loginDetails = input('Sign in or sign up with email\nEmail address: ')
    os.system('cls')
    _check = check(loginDetails)

    if _check[0]:
        while True:
            password = pwinput.pwinput(prompt=f'Welcome back {_check[1]}\nPlease enter your password to login: ')
            if login(loginDetails, password):
                print('\nLogin successful')
                new = False
                break
            else:
                os.system('cls')
                print('Login unsuccessful, please try again')
                
    else:
        os.system('cls')
        print('Hello new user, please sign up')
        name = input('What is your name: ')
        password = pwinput.pwinput(prompt='Enter a safe and secure password: ')
        register(loginDetails, password, name)
        os.system('cls')
        print('Registration successful!\nAuto-Login successful')
        new = True

    os.system('cls')
    print('Hold on while we fetch your details...')
    _check = check(loginDetails)
    data = retrieve(loginDetails)
    print('All done!')
    os.system('cls')

def cardPayment(choice, quantity, deliveryTime, menu):
    print('All sensitive information is stored securely and encrypted')
    text = ''
    while True:
        card = input(f'{text}Please enter your Card Number: ')
        if len(card) != 16:
            text = 'Invalid Card Number, please try again '
        else:
            text = ''
            break
    while True:
        cvv = input(f'{text}Please enter your CVV: ')
        if len(cvv) not in (3, 4):
            text = 'Invalid CVV, please try again '
        else:
            text = ''
            break
    while True:
        expiry = input(f'{text}Please enter your Expiry Date in the format MM/YY: ')
        cmonth, cyear = expiry.split('/')
        month, year = datetime.now().strftime('%m/%y').split('/')
        if not (int(cyear) >= int(year) and int(cmonth) >= int(month) and int(cyear)<int(year)+10 and int(cmonth) <= 12):
            text = 'Invalid Expiry Date, please try again '
        else:
            text = ''
            break
    cardtype = 'Visa' if str(card)[0] == 4 else 'MasterCard'
    save = input('Would you like to save your card details for future orders?\n1.Yes\n2.No\nEnter your choice: ')
    os.system('cls')
    if save == '1':
        addPayment(loginDetails, card, cvv, expiry, cardtype)
    print(f'Thank you for your order of {choice} x {quantity}. Payment has been made on your {cardtype} ending with {str(card)[12:]}\nOrder Number: {len(eval(data[1]))+1}\nPrice: {int(quantity)*menu[choice]} AED\nEstimated time of delivery: {deliveryTime//60} minutes')

#Initialising login screen
loginscreen()

while True:
    os.system('cls')
    print(f'Welcome{" back " if not new else " "}to {projectname}, {_check[1]}! What would you like to do today?')
    print('1.Place an order\n2.View your orders\n3.View or change your account details\n4.Logout\n5.Exit')
    choice = input('Enter your choice: ')

    if choice == '1':
        os.system('cls')
        print('Please wait while we retrieve nearby restaurants...')
        os.system('cls')
        restaurants = getRestaurants()
        print('All done! Here are the nearby restaurants\n')

        for restaurant in restaurants:
            details = eval(restaurant[2])
            menu = eval(restaurant[1])
            print(restaurant[0])
            print(f'Location: {details["Location"]}\nCuisine: {details["Cuisine"]}\nRating: {details["Rating"]}\nPhone: {details["Phone"]}\nWebsite: {details["Website"]}\n\n')
        
        choice = input('Which restaurant would like you to order from: ')
        print('\n')
        os.system('cls')

        for restaurant in restaurants:
            if restaurant[0] == choice:
                menu = eval(restaurant[1])
                print('Menu:')

                for dish in menu:
                    print(f'{dish}: {menu[dish]} AED')
                print('\n')
                choice = input('Which dish would you like to order: ')

                if choice in menu:
                    quantity = input('\nHow many would you like to order: ')
                    payment = input('\nHow would you like to pay?\n1.Cash on Delivery\n2.Pay Online\nEnter your choice: ')
                    deliveryTime = random.randint(20,50)*60
                    unix = (datetime.now()+ timedelta(seconds=deliveryTime)).timestamp()

                    if payment == '1':
                        print('\n')
                        os.system('cls')
                        print(f'Thank you for your order of {choice} x {quantity}. Payment will be made on delivery\nOrder Number: {len(eval(data[1]))+1}\nPrice: {int(quantity)*menu[choice]} AED\nEstimated time of delivery: {deliveryTime//60} minutes')
                    elif payment == '2':
                        print('\n')
                        os.system('cls')

                        if retrievePayment(loginDetails)[0]:
                            cont = input('Would you like to use your saved card details?\n1.Yes\n2.No\nEnter your choice: ')
                            if cont == '1':
                                carddetails = eval(retrievePayment(loginDetails)[1][0])
                                print(f'Thank you for your order of {choice} x {quantity}. Payment has been made on your {carddetails["cardtype"]} ending with {str(carddetails["card"])[12:]}\nOrder Number: {len(eval(data[1]))+1}\nPrice: {int(quantity)*menu[choice]} AED\nEstimated time of delivery: {deliveryTime//60} minutes')
                            elif cont == '2':
                                cardPayment(choice, quantity, deliveryTime, menu)
                        else:
                            cardPayment(choice, quantity, deliveryTime, menu)
                    price = int(quantity)*menu[choice]
                    placeOrder(loginDetails, restaurant[0], choice, quantity, unix, price)
                    data = retrieve(loginDetails)[1]
                else:
                    print('Dish not available')

        input('Press enter to continue...  ')

    elif choice == '2':
        os.system('cls')
        print('\n')
        orders = viewOrders(loginDetails)

        if orders[0]:
            print('Your orders:')
            orders = orders[1]

            for order in orders:
                order = eval(order)

                for i in range(0,len(order)):
                    j = str(i)
                    deliveryStatus = 'Delivered' if order[j][3] < datetime.now().timestamp() else 'Delivering in'
                    print(f'Order Number {i+1}\nRestaurant: {order[j][0]}\nDish: {order[j][1]}\nQuantity: {order[j][2]}\n{deliveryStatus} {humanize.naturaltime(datetime.fromtimestamp(order[j][3]))} ({datetime.fromtimestamp(order[j][3]).strftime("%D %H:%M:%S")})\nPrice: {order[j][4]} AED\n')
                    print('\n')
        else:
            print('No orders yet, place an order to get started')
        input('Press enter to continue... ')

    elif choice == '3':
        os.system('cls')
        print('\n')
        userDetails = retrieveDetails(loginDetails)
        __check = retrieve(loginDetails)
        if __check[2] != '{}':
            card = eval(__check[2])
            cardDetails = f'{card["cardtype"]} ending with {card["card"][12:]} expiring on {card["expiry"]}'
        
        else:
            cardDetails = None
        print(f'Your account details:\nName: {userDetails[2]}\nEmail: {userDetails[1]}\nCard: {cardDetails}')
        print('\n')
        choice = input('Would you like to change your password?\n1.Yes\n2.No\nEnter your choice: ')

        if choice == '1':
            os.system('cls')
            password = input('Enter your new password: ')
            changePassword(loginDetails, password)
            print('Password changed successfully')
            input('Press enter to continue... ')

    elif choice == '4':
        print('\n')
        print('Logging out...')
        time.sleep(2)
        print('Logged out successfully')

        loginscreen()

    elif choice == '5':
        print('\n')
        print(f'Thank you for using {projectname}\nHave a nice day!')
        time.sleep(4)
        exit()

    else:
        print('Invalid choice, please try again')