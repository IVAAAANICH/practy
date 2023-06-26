import tkinter.messagebox as tkmb
import sqlite3
import configparser
import tkinter as tk
from tkinter import *
from tkinter import ttk

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

root = Tk()
root.title(config['Application']['Title'])
root.geometry(config['Application']['Geometry'])
root.resizable(width=config.getboolean('Application', 'ResizableWidth'), height=config.getboolean('Application', 'ResizableHeight'))

def open_registration_window():
    global second_window
    second_window = Toplevel(root)
    second_window.title(config['Windows']['RegistrationWindowTitle'])
    second_window.geometry(config['Windows']['RegistrationWindowGeometry'])
    
    global entry_username, entry_email, entry_phone_number, entry_login, entry_password

    label_username = Label(second_window, text=config['Labels']['UsernameLabel'])
    label_username.pack(pady=5)
    entry_username = Entry(second_window)
    entry_username.pack(pady=5)

    label_email = Label(second_window, text=config['Labels']['EmailLabel'])
    label_email.pack(pady=5)
    entry_email = Entry(second_window)
    entry_email.pack(pady=5)

    label_phone_number = Label(second_window, text=config['Labels']['PhoneNumberLabel'])
    label_phone_number.pack(pady=5)
    entry_phone_number = Entry(second_window)
    entry_phone_number.pack(pady=5)

    label_login = Label(second_window, text=config['Labels']['LoginLabel'])
    label_login.pack(pady=5)
    entry_login = Entry(second_window)
    entry_login.pack(pady=5)

    label_password = Label(second_window, text=config['Labels']['PasswordLabel'])
    label_password.pack(pady=5)
    entry_password = Entry(second_window, show='*')
    entry_password.pack(pady=5)

    btn_register = Button(second_window, text=config['Buttons']['RegisterButton'], command=register_user)
    btn_register.pack(pady=10)

def login_user():
    global tree, entry_poisk
    login_username = entry_login_username.get()
    login_password = entry_login_password.get()

    conn = sqlite3.connect(config['Database']['Filename1'])
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE login=? AND password=?', (login_username, login_password))
    result = cursor.fetchone()
    conn.close()
    if result:
        # Открываем основное окно
        welcome_window = Tk()
        welcome_window.geometry(config['Windows']['WelcomeWindowGeometry'])
        welcome_window.title(config['Windows']['WelcomeWindowTitle'])
        welcome_window.resizable(width=False, height=False)

        frame_poisk = tk.Frame(welcome_window)
        frame_poisk.pack(pady=10)

        label_poisk = tk.Label(frame_poisk, text=config['Labels']['SearchLabel'])
        label_poisk.pack(side=tk.LEFT)

        entry_poisk = tk.Entry(frame_poisk)
        entry_poisk.pack(side=tk.LEFT, padx=5)

        button_poisk = tk.Button(frame_poisk, text=config['Buttons']['SearchButton'], command=poisk_data)
        button_poisk.pack(side=tk.LEFT)

        tree = ttk.Treeview(welcome_window)
        tree["columns"] = ("ip", "time", "code", "dan")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("ip", anchor=tk.CENTER, width=120)
        tree.column("time", anchor=tk.CENTER, width=120)
        tree.column("code", anchor=tk.CENTER, width=80)
        tree.column("dan", anchor=tk.CENTER, width=180)

        tree.heading("#0", text="")
        tree.heading("ip", text=config['TableHeadings']['IpAddress'])
        tree.heading("time", text=config['TableHeadings']['Date'])
        tree.heading("code", text=config['TableHeadings']['Code'])
        tree.heading("dan", text=config['TableHeadings']['Data'])

        tree.pack(fill=tk.BOTH, expand=True)

        conn = sqlite3.connect(config['Database']['Filename2'])
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM log")
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", tk.END, text="", values=row)

        conn.close()

    else:
        tkmb.showerror(config['Messages']['ErrorTitle'], config['Messages']['InvalidCredentialsMessage'])

def poisk_data():
    keyword = entry_poisk.get().strip()
    
    tree.delete(*tree.get_children())
    
    connection = sqlite3.connect(config['Database']['Filename2'])
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM log WHERE ip LIKE ? OR time LIKE ? OR code LIKE ? OR dan LIKE ?",
                   ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", tk.END, text="", values=row)
    
    connection.close()

def register_user():
    registered_username = entry_username.get()
    registered_email = entry_email.get()
    registered_phone_number = entry_phone_number.get()
    registered_login = entry_login.get()
    registered_password = entry_password.get()

    conn = sqlite3.connect(config['Database']['Filename'])
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, phone_number, login, password) VALUES (?,?,?,?,?)', (registered_username, registered_email, registered_phone_number, registered_login, registered_password))
    conn.commit()
    conn.close()

    second_window.destroy()

label_login_username = Label(root, text=config['Labels']['LoginLabel'])
label_login_username.pack(pady=10)
entry_login_username = Entry(root)
entry_login_username.pack(pady=10)

label_login_password = Label(root, text=config['Labels']['PasswordLabel'])
label_login_password.pack(pady=10)
entry_login_password = Entry(root, show='*')
entry_login_password.pack(pady=10)

btn_login = Button(root, text=config['Buttons']['LoginButton'], command=login_user)
btn_login.pack(pady=10)

conn = sqlite3.connect(config['Database']['Filename1'])
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, phone_number TEXT, login TEXT, password TEXT)')
conn.commit()
conn.close()

btn_open_registration_window = Button(root, text=config['Buttons']['RegistrationButton'], command=open_registration_window)
btn_open_registration_window.pack(pady=10)

root.mainloop()