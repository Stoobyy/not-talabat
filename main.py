# Importing Modules
import mysql.connector as sql
import os
import time
import requests
from cryptography.fernet import Fernet
import tkinter
import customtkinter 

# Variables to be stored on seperate secure database
key = 'D9QRguYyat5TWlIyfg9AFWizc91muAGD-UlpWHxT0Y8='
# Creating required objects
db = sql.connect(
    host = 'localhost',
    username = 'root',
    password = 'stooby',
    database = 'notTalabat'
)
cursor = db.cursor()
f=Fernet(key)
root_tk = tkinter.Tk()  # create the Tk window like you normally do
root_tk.geometry("480x640")
root_tk.title("Not Talabat | Easy food delivery")

def login(username, password):
    encpassword = list(cursor.execute(f'select password from userdata where username = {username}'))[0]
    output = f.decrypt(encpassword.encode())
    if password == output:
        return True

