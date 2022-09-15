import tkinter
import customtkinter
import os
import time
import requests
import humanize
from datetime import datetime, timedelta
from sql import *
import random
from ctk.ctk import *

key = 'D9QRguYyat5TWlIyfg9AFWizc91muAGD-UlpWHxT0Y8='

db = sql.connect(
    host = 'localhost',
    username = 'root',
    password = 'stooby',
    database = 'notTalabat'
)
cursor = db.cursor()
f=Fernet(key)

def login(username, password, frame):
    cursor.execute(f'select password from userdata where username = \'{username}\'')
    encpassword = cursor.fetchall()[0][0]
    output = f.decrypt(encpassword.encode())
    if password == output.decode():
        True
    else:
        failed_label = customtkinter.CTkLabel(frame, text='Login Failed', text_font= ('Verdana', '20', 'bold'))
        failed_label.grid(row=4, column=0, columnspan=2, sticky="news", pady=40)
