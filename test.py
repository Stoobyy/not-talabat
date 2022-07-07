# Importing Modules
import mysql.connector as sql
import os
import time
import requests
from cryptography.fernet import Fernet

# Variables to be stored on seperate secure database
key = 'D9QRguYyat5TWlIyfg9AFWizc91muAGD-UlpWHxT0Y8='

# Creating required objects
db = sql.connect(
    host = 'localhost',
    username = 'root',
    password = 'stooby',
    database = 'nottalabat'
)
cursor = db.cursor()
f=Fernet(key)

def login(username, password):
    encpassword = list(cursor.execute(f'select password from userdata where username = {username}'))[0]
    output = f.decrypt(encpassword.encode())
    if password == output:
        return True

print('**********************************\n           Not Trivago\n**********************************\n')
print('Welcome to Not Trivago\nAre you a')
logintype = int(input('1.'))