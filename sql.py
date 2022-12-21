from cryptography.fernet import Fernet
import mysql.connector as sql
import random
import os
import json

with open('sqlDetails.json') as f:
    config = json.load(f)

db = sql.connect(
    host = config['host'],
    username = config['username'],
    password = config['password'],
)

key = 'D9QRguYyat5TWlIyfg9AFWizc91muAGD-UlpWHxT0Y8=' #Store in secure place

cursor = db.cursor()
f=Fernet(key)
db.autocommit = True

def login(username, password):
    cursor.execute(f'select password from userdata where username = \'{username}\'')
    encpassword = cursor.fetchall()[0][0]
    output = f.decrypt(encpassword.encode())
    if password == output.decode():
        return True

def register(username, password, name):
    password = f.encrypt(password.encode())
    cursor.execute(f'insert into userdata values (\'{password.decode()}\', \'{username}\', \'{name}\')')
    cursor.execute(f'insert into data values ("{username}", "{dict()}", "{dict()}")')
    return True

def check(username):
    cursor.execute(f'select * from userdata where username = \'{username}\'')
    output = cursor.fetchall()
    if output != []:
        output = output[0]
        return True, output[2]
    else:
        return False, None

def retrieve(username):
    cursor.execute(f'select * from data where username = \'{username}\'')
    output = cursor.fetchall()
    return output[0]

def getRestaurants():
    cursor.execute('select * from restaurants')
    output = cursor.fetchall()
    return output

def placeOrder(username, restaurant, dish, quantity, unix, price):
    cursor.execute(f'select orders from data where username = \'{username}\'')
    output = cursor.fetchall()
    if output == [('{}',)]:
        output = {}
    else:
        output = eval(output[0][0])
    output.update({f'{len(output)}':[restaurant, dish, quantity, unix, price]})
    cursor.execute(f'update data set orders = "{output}" where username = \'{username}\'')
    cursor.execute(f'select * from data where username = \'{username}\'')
    output = cursor.fetchall()
    return True, output[0]

def viewOrders(username):
    cursor.execute(f'select orders from data where username = \'{username}\'')
    output = cursor.fetchall()
    if output == [('{}',)]:
        return False, None
    else:
        return True, output[0]

def logout(username):
    cursor.execute(f'update data set orders = "{dict()}" where username = \'{username}\'')
    return True


def changePassword(username, password):
    password = f.encrypt(password.encode())
    cursor.execute(f'update userdata set password = "{password.decode()}" where username = \'{username}\'')
    return True

def addPayment(username, card, cvv, expiry,cardtype):
    cursor.execute(f'select payment from data where username = \'{username}\'')
    output = cursor.fetchall()
    if output == [('{}',)]:
        output = {}
    else:
        output = eval(output[0][0])
    output = {'card':card, 'cvv':cvv, 'expiry':expiry, 'cardtype':cardtype}
    cursor.execute(f'update data set payment = "{output}" where username = \'{username}\'')
    return True

def retrieveDetails(username):
    cursor.execute(f'select * from userdata where username = \'{username}\'')
    output = cursor.fetchall()
    return output[0]

def retrievePayment(username):
    cursor.execute(f'select payment from data where username = \'{username}\'')
    output = cursor.fetchall()
    if output == [('{}',)]:
        return False, None
    else:
        return True, output[0]
