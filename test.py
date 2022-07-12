import tkinter
import customtkinter  # <- import the CustomTkinter module

root_tk = tkinter.Tk()  # create the Tk window like you normally do
root_tk.geometry("480x640")
root_tk.title("easy")

def button_function():
    print('helo')

button = customtkinter.CTkButton(master=root_tk,
                                 fg_color=("black", "lightgray"),  # <- tuple color for light and dark theme
                                 text="CTkButton",
                                 command=button_function)
button.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)

root_tk.mainloop()