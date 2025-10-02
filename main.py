# main.py (rich-enhanced, logic preserved)
# Importing required modules
import os
import time
import humanize
from datetime import datetime, timedelta
from sql import *
import random
import pwinput

projectname = 'Zoop'

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt

    console = Console()
    RICH = True
except Exception:
    Console = None
    Table = None
    Panel = None
    Prompt = None
    console = None
    RICH = False


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def cprint(text='', end='\n'):
    if RICH:
        console.print(text, end=end)
    else:
        print(text, end=end)


def input_prompt(prompt=''):
    if RICH:
        return console.input(prompt)
    else:
        return input(prompt)


def prompt_choice(prompt, choices=None, default=None):
    if choices and RICH:
        return Prompt.ask(prompt, choices=choices, default=default)
    else:
        return input_prompt(f"{prompt} ")


def print_table(title, headers, rows):
    if RICH:
        table = Table(title=title)
        for h in headers:
            table.add_column(h, overflow="fold")
        for row in rows:
            # convert every cell to string
            table.add_row(*[str(x) for x in row])
        console.print(table)
    else:
        # simple fallback table
        cprint(f"--- {title} ---")
        cprint(" | ".join(headers))
        cprint("-" * 40)
        for row in rows:
            cprint(" | ".join([str(x) for x in row]))
        cprint("")


def print_panel(title, content):
    if RICH:
        console.print(Panel(content, title=title, expand=False))
    else:
        cprint(f"{title}\n{content}\n")


# Login screen function
def loginscreen():
    global new
    global _check
    global data
    global loginDetails

    clear()
    cprint(f"[bold cyan]Welcome to {projectname}[/bold cyan]\nYour favourite dishes and delicacies delivered to your doorsteps!" if RICH else f"Welcome to {projectname}\nYour favourite dishes and delicacies delivered to your doorsteps!")
    loginDetails = input_prompt('Sign in or sign up with email\nEmail address: ')
    clear()
    _check = check(loginDetails)

    if _check[0]:
        while True:
            password = pwinput.pwinput(prompt=f'Welcome back {_check[1]}\nPlease enter your password to login: ')
            if login(loginDetails, password):
                cprint('\n[green]Login successful[/green]' if RICH else '\nLogin successful')
                new = False
                break
            else:
                clear()
                cprint('[red]Login unsuccessful, please try again[/red]' if RICH else 'Login unsuccessful, please try again')

    else:
        clear()
        cprint('Hello new user, please sign up')
        name = input_prompt('What is your name: ')
        password = pwinput.pwinput(prompt='Enter a safe and secure password: ')
        register(loginDetails, password, name)
        clear()
        cprint('[green]Registration successful!\nAuto-Login successful[/green]' if RICH else 'Registration successful!\nAuto-Login successful')
        new = True

    clear()
    cprint('Hold on while we fetch your details...')
    _check = check(loginDetails)
    data = retrieve(loginDetails)
    cprint('All done!')
    clear()


# -------------------------
# Payment function
# -------------------------
def cardPayment_cart(cart, deliveryTime, total_price):
    cprint('All sensitive information is stored securely and encrypted')
    text = ''
    while True:
        card = input_prompt(f'{text}Please enter your Card Number: ')
        if len(card) != 16:
            text = 'Invalid Card Number, please try again '
        else:
            text = ''
            break
    while True:
        cvv = input_prompt(f'{text}Please enter your CVV: ')
        if len(cvv) not in (3, 4):
            text = 'Invalid CVV, please try again '
        else:
            text = ''
            break
    while True:
        expiry = input_prompt(f'{text}Please enter your Expiry Date in the format MM/YY: ')
        try:
            cmonth, cyear = expiry.split('/')
            month, year = datetime.now().strftime('%m/%y').split('/')
            if not (int(cyear) >= int(year) and int(cmonth) >= int(month) and int(cyear) < int(year) + 10 and int(cmonth) <= 12):
                text = 'Invalid Expiry Date, please try again '
            else:
                text = ''
                break
        except Exception:
            text = 'Invalid Expiry Date, please try again '

    cardtype = 'Visa' if str(card)[0] == '4' else 'MasterCard'
    save = prompt_choice('Would you like to save your card details for future orders?\n1.Yes\n2.No\nEnter your choice:', choices=['1', '2'], default='1')
    clear()
    if save == '1':
        addPayment(loginDetails, card, cvv, expiry, cardtype)

    cprint("Thank you for your order:")
    for dish, qty, price in cart:
        cprint(f"   {dish} x {qty} = {price} AED")
    cprint(f"Total: {total_price} AED\nPayment has been made on your {cardtype} ending with {str(card)[12:]}")

    orders = viewOrders(loginDetails)
    if orders[0]:
        order_number = len(eval(orders[1][0])) + 1
    else:
        order_number = 1

    cprint(f"Order Number: {order_number}\nEstimated time of delivery: {deliveryTime // 60} minutes")



# Program start
loginscreen()

cart = []
while True:
    clear()
    cprint(f'Welcome{" back " if not new else " "}to {projectname}, {_check[1]}! What would you like to do today?')
    cprint('1.Place an order\n2.View your orders\n3.View or change your account details\n4.Logout\n5.Exit')
    choice = input_prompt('Enter your choice: ')

    if choice == '1':
        clear()
        cprint('Please wait while we retrieve nearby restaurants...')
        clear()
        restaurants = getRestaurants()
        cprint('All done! Here are the nearby restaurants\n')

        rows = []
        for restaurant in restaurants:
            details = eval(restaurant[2])
            rows.append((restaurant[0], details.get("Location", ""), details.get("Cuisine", ""), details.get("Rating", ""), details.get("Phone", ""), details.get("Website", "")))
        print_table("Nearby Restaurants", ["Name", "Location", "Cuisine", "Rating", "Phone", "Website"], rows)

        choice = input_prompt('Which restaurant would like you to order from: ')
        cprint('\n')
        clear()

        for restaurant in restaurants:
            if restaurant[0] == choice:
                menu = eval(restaurant[1])
                while True:
                    clear()
                    cprint(f"Menu - {restaurant[0]}:\n")
                    menu_rows = [(dish, f"{menu[dish]} AED") for dish in menu]
                    print_table(f"Menu - {restaurant[0]}", ["Dish", "Price"], menu_rows)

                    choice = input_prompt('\nWhich dish would you like to order (or type "checkout" to finish): ')

                    if choice.lower() == "checkout":
                        if not cart:
                            cprint("Cart is empty, nothing to checkout.")
                            input_prompt("Press enter to continue...")
                            break

                        clear()
                        cprint("Your Cart:")
                        cart_rows = [(dish, qty, f"{price} AED") for dish, qty, price in cart]
                        print_table("Cart Summary", ["Dish", "Qty", "Price"], cart_rows)
                        total_price = sum([item[2] for item in cart])
                        cprint(f"Total: {total_price} AED")

                        payment = prompt_choice('\nHow would you like to pay?\n1.Cash on Delivery\n2.Pay Online\nEnter your choice:', choices=['1', '2'], default='1')
                        deliveryTime = random.randint(20, 50) * 60
                        unix = (datetime.now() + timedelta(seconds=deliveryTime)).timestamp()

                        if payment == '1':
                            cprint(f"\nThank you! Payment on delivery.\nOrder placed for {len(cart)} items. Total = {total_price} AED")
                        elif payment == '2':
                            if retrievePayment(loginDetails)[0]:
                                cont = prompt_choice('Would you like to use your saved card details?\n1.Yes\n2.No\nEnter your choice:', choices=['1', '2'], default='1')
                                if cont == '1':
                                    carddetails = eval(retrievePayment(loginDetails)[1][0])
                                    cprint(f'Thank you for your order. Payment has been made on your {carddetails["cardtype"]} ending with {str(carddetails["card"])[12:]}')
                                else:
                                    cardPayment_cart(cart, deliveryTime, total_price)
                            else:
                                cardPayment_cart(cart, deliveryTime, total_price)

                        placeOrder(loginDetails, restaurant[0], cart, unix, total_price)
                        data = retrieve(loginDetails)[1]
                        cart = [] 
                        break

                    elif choice in menu:
                        try:
                            quantity = int(input_prompt('\nHow many would you like to order: '))
                        except Exception:
                            cprint("Invalid quantity")
                            input_prompt("Press enter to continue...")
                            continue
                        price = quantity * menu[choice]
                        cart.append((choice, quantity, price))
                        cprint(f"{choice} x {quantity} added to cart ({price} AED)")
                        input_prompt("Press enter to continue...")
                    else:
                        cprint("Dish not available")
                        input_prompt("Press enter to continue...")

        input_prompt('Press enter to continue...  ')

    elif choice == '2':
        clear()
        cprint('\n')
        orders = viewOrders(loginDetails)

        if orders[0]:
            cprint('Your orders:')
            orders = orders[1]
            for order in orders:
                order = eval(order)
                for i in range(0, len(order)):
                    j = str(i)
                    restaurant = order[j][0]
                    items = order[j][1]
                    unix_time = order[j][2]
                    total_price = order[j][3]

                    cprint(f'Order Number {i+1}\nRestaurant: {restaurant}')
                    for dish, qty, price in items:
                        cprint(f'   {dish} x {qty} = {price} AED')

                    deliveryStatus = 'Delivered' if unix_time < datetime.now().timestamp() else 'Delivering in'
                    cprint(f'Total Price: {total_price} AED\n{deliveryStatus} {humanize.naturaltime(datetime.fromtimestamp(unix_time))} ({datetime.fromtimestamp(unix_time).strftime("%D %H:%M:%S")})\n')
                    cprint('\n')
        else:
            cprint('No orders yet, place an order to get started')
        input_prompt('Press enter to continue... ')

    elif choice == '3':
        clear()
        cprint('\n')
        userDetails = retrieveDetails(loginDetails)
        __check = retrieve(loginDetails)
        if __check[2] != '{}':
            card = eval(__check[2])
            cardDetails = f'{card["cardtype"]} ending with {card["card"][12:]} expiring on {card["expiry"]}'
        else:
            cardDetails = None

        details_content = f"Name: {userDetails[2]}\nEmail: {userDetails[1]}\nCard: {cardDetails if cardDetails else 'None'}"
        print_panel("Account Details", details_content)

        choice = prompt_choice('Would you like to change your password?\n1.Yes\n2.No\nEnter your choice:', choices=['1', '2'], default='2')

        if choice == '1':
            clear()
            oldpassword = pwinput.pwinput(prompt='Enter Old Password: ')
            if login(loginDetails, oldpassword):
                password = pwinput.pwinput(prompt='Enter New Password: ')
                confirm = pwinput.pwinput(prompt='Confirm New Password: ')

                if password == confirm:
                    changePassword(loginDetails, password)
                    cprint('Password changed successfully')
                else:
                    cprint('Passwords do not match')
            else:
                cprint('Incorrect password')
            input_prompt('Press enter to continue...')

    elif choice == '4':
        cprint('\n')
        cprint('Logging out...')
        time.sleep(2)
        cprint('Logged out successfully')

        loginscreen()

    elif choice == '5':
        cprint('\n')
        cprint(f'Thank you for using {projectname}\nHave a nice day!')
        time.sleep(4)
        exit()

    else:
        cprint('Invalid choice, please try again')
