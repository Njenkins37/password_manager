from tkinter import *
from tkinter import messagebox
import json
import random


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def gen_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))
    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    pass_entry.insert(0, password)


# ---------------------------- SEARCH PASSWORD -----------------------------#
def search_db():
    thing_to_search = web_entry.get().lower()
    try:
        with open('data.json', mode='r') as file:
            data = json.load(file)
            focus = data[thing_to_search]
            messagebox.showinfo(title='Password Found', message=f"Your email/username is {focus['email']}.\n"
                                f"Your password is {focus['password']}")
    except FileNotFoundError:
        messagebox.showerror(title='File Not Found', message='The file you requested to be searched was not found.')
    except KeyError:
        messagebox.showerror(title='Website Not Found', message='The website or location you have requested does not '
                                                                'exist in our database. You can try again without the '
                                                                '.com suffix')


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pass():
    website = web_entry.get()
    user_name = email_entry.get()
    pass_word = pass_entry.get()
    new_data = {
        website: {
            'email': user_name,
            'password': pass_word
        }
    }

    if len(website) == 0 or len(pass_word) == 0:
        messagebox.showerror(title="Missing website or password", message="You did not enter a website or a password. "
                                                                          "Please try again")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f'These are your details: \nWebsite: {website}\nEmail/Username: {user_name}\n'
                                               f'Password: {pass_word}\n'
                                               f'Do you want to save?')
        if is_ok:
            try:
                with open('data.json', mode='r') as file:
                    data = json.load(file)
                    data.update(new_data)
                with open('data.json', mode='w') as file:
                    json.dump(data, file, indent=4)
            except FileNotFoundError:
                with open('data.json', mode='w') as file:
                    json.dump(new_data, file, indent=4)

            web_entry.delete(0, END)
            pass_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# Label Creation
web = Label(text='Website:')
username = Label(text='Email/Username:')
password = Label(text='Password:')

# Button Creation
gen_pass = Button(text='Generate Password', command=gen_password)
add = Button(text='Add', width=36, command=save_pass)
search = Button(text='Search', width=13, command=search_db)

# Entry Creations
web_entry = Entry(width=20)
web_entry.focus()
email_entry = Entry(width=38)
pass_entry = Entry(width=21)

# Layouts
web.grid(row=1, column=0)
username.grid(row=2, column=0)
password.grid(row=3, column=0)

web_entry.grid(row=1, column=1, columnspan=1)
email_entry.grid(row=2, column=1, columnspan=2)
pass_entry.grid(row=3, column=1)

gen_pass.grid(row=3, column=2)
add.grid(row=4, column=1, columnspan=2)
search.grid(row=1, column=2)

window.mainloop()
