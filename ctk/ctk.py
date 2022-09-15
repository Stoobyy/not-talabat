import tkinter
import customtkinter
import os
import time
import requests
import humanize
from datetime import datetime, timedelta
from ctk.ctkFunctions import *
import random

projectname = 'Not Talabat'

def register(username, password, name):
    password = f.encrypt(password.encode())
    cursor.execute(f'insert into userdata values (\'{password.decode()}\', \'{username}\', \'{name}\')')
    cursor.execute(f'insert into data values ("{username}", "{dict()}", "{dict()}")')
    db.commit()
    name_label.grid_remove()
    name_entry.grid_remove()
    password_label.grid_remove()
    password_entry.grid_remove()
    continue_button.grid_remove()
    new_label = customtkinter.CTkLabel(frame, text='Account Created\nPlease Login', text_font= ('Verdana', '8', 'bold'))
    new_label.grid(row=2, column=0, sticky="news", columnspan=2, pady=40)
    username_label.grid(row=3, column=0, sticky="news", pady=10)
        


def check(username):
    cursor.execute(f'select * from userdata where username = \'{username}\'')
    output = cursor.fetchall()
    print(output)
    username_label.grid_remove()
    username_entry.grid_remove()
    continue_button.grid_remove()
    if output != []:
        output = output[0][2]
        name_label = customtkinter.CTkLabel(frame, text=f'Welcome back {output}!', text_font=('Verdana', '10'))
        name_label.grid(row=2, column=0, columnspan=2, sticky="news", pady=10)
        password_label.grid(row=3, column=0, sticky="news", pady=10)
        password_entry.grid(row=3, column=1, sticky="news", pady=20)
        login_button.grid(row=4, column=0, columnspan=2, pady=20)
    else:
        new_label = customtkinter.CTkLabel(frame, text='Hello There!\n Please fill in the below details\nto create your account', text_font= ('Verdana', '8', 'bold'))
        new_label.grid(row=2, column=0, sticky="news", columnspan=2, pady=10)
        name_label = customtkinter.CTkLabel(frame, text='Name')
        name_label.grid(row=3, column=0, sticky="news", pady=10)
        name_entry = customtkinter.CTkEntry(frame)
        name_entry.grid(row=3, column=1, sticky="news", pady=20)
        password_label.grid(row=4, column=0, sticky="news", pady=10)
        password_entry.grid(row=4, column=1, sticky="news", pady=10)
        continue_button.grid(row=5, column=0, columnspan=2, pady=20)


def completelogin(username, password):
    cursor.execute(f'select password from userdata where username = \'{username}\'')
    encpassword = cursor.fetchall()[0][0]
    output = f.decrypt(encpassword.encode())
    if password == output.decode():
        password_entry.grid_remove()
        login_button.grid_remove()
        password_label.grid_remove()
        login_message = customtkinter.CTkLabel(frame, text="Login Successful\nLoading Userdata Please Wait...", text_font=("Helvetica", '10'))
        login_message.grid(row=2, column=0, sticky="news", pady=40)
    else:
        failed_label = customtkinter.CTkLabel(frame, text='Login Failed', text_font= ('Verdana', '5', 'bold'))
        failed_label.grid(row=4, column=0, columnspan=2, sticky="news", pady=40)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("480x480")
app.title(projectname + ' | Food Delivery')
app.resizable(False, False)
frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=20, padx=50)

login_label = customtkinter.CTkLabel(frame, text='\nZoop', text_font= ('Verdana', '20', 'bold'))
user_label = customtkinter.CTkLabel(frame, text='Food Delivery', text_font= ('Verdana', '18', 'bold'))
username_label = customtkinter.CTkLabel(frame, text="Username")
username_entry = customtkinter.CTkEntry(frame)
password_entry = customtkinter.CTkEntry(frame, show="*")
password_label = customtkinter.CTkLabel(frame, text="Password")
continue_button = customtkinter.CTkButton(frame, text="Continue", command= lambda: check(username_entry.get()))
login_button = customtkinter.CTkButton(frame, text="Continue", command= lambda: completelogin(username_entry.get(), password_entry.get()))

login_label.grid(row=0, column=0, columnspan=2, sticky="news")
user_label.grid(row=1, column=0, columnspan=2, sticky="news", pady=10)
username_label.grid(row=2, column=0, pady = 20)
username_entry.grid(row=2, column=1, pady=20)
continue_button.grid(row=3, column=0, columnspan=2, pady=20)

frame.pack()

app.mainloop()



