import customtkinter
from tkinter import messagebox
import sqlite3
import hashlib

# Connect to the database
conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

# Create the table if it doesn't exist
cur.execute(""" 
CREATE TABLE IF NOT EXISTS userdata (
            id INTEGER PRIMARY KEY,
            username VARCHAR(255) NOT NULL ,
            password VARCHAR(255) NOT NULL
)          
""")

# Insert some sample data
username1, password1 = "test1", hashlib.sha256("test".encode()).hexdigest()
username2, password2 = "test12", hashlib.sha256("test2".encode()).hexdigest()
username3, password3 = "test123", hashlib.sha256("test3".encode()).hexdigest()
username4, password4 = "test1234", hashlib.sha256("test4".encode()).hexdigest()
cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username1, password1))
cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username2, password2))
cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username3, password3))
cur.execute("INSERT INTO userdata (username, password) VALUES (?,?)", (username4, password4))

conn.commit()

# Set appearance
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# Create the root window
root = customtkinter.CTk()
root.geometry("500x350")
root.title("Login Form")

# Define the login function
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    # Query the database for the provided username and password
    cur.execute("SELECT * FROM userdata WHERE username=? AND password=?", (username, hashlib.sha256(password.encode()).hexdigest()))
    result = cur.fetchone()
    
    # If a matching user is found, show success message
    if result:
        messagebox.showinfo(title="Login Success", message="You Successfully logged in.")
    else:
        messagebox.showerror(title="Error", message="Invalid login.")

# Create the frame
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Create and pack widgets
label = customtkinter.CTkLabel(master=frame, text="Login System")
label.configure(font=("Roboto", 24))
label.pack(pady=12, padx=10)

username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
username_entry.pack(pady=12, padx=10)

password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
password_entry.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
checkbox.pack(pady=12, padx=10)

# Start the main loop
root.mainloop()
