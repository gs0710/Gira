import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database initialization
def initialize_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (email TEXT PRIMARY KEY, password TEXT)''')
    
    # Create items table for CRUD operations
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  user_email TEXT,
                  FOREIGN KEY(user_email) REFERENCES users(email))''')
    
    conn.commit()
    conn.close()

initialize_database()

class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Login System")
        
        # Login Frame
        self.login_frame = tk.Frame(master)
        self.login_frame.pack(pady=20)
        
        # Email
        self.lbl_email = tk.Label(self.login_frame, text="Email:")
        self.lbl_email.grid(row=0, column=0)
        self.ent_email = tk.Entry(self.login_frame)
        self.ent_email.grid(row=0, column=1)
        
        # Password
        self.lbl_password = tk.Label(self.login_frame, text="Password:")
        self.lbl_password.grid(row=1, column=0)
        self.ent_password = tk.Entry(self.login_frame, show="*")
        self.ent_password.grid(row=1, column=1)
        
        # Buttons
        self.btn_login = tk.Button(self.login_frame, text="Login", command=self.login)
        self.btn_login.grid(row=2, column=0, pady=10)
        
        self.btn_register = tk.Button(self.login_frame, text="Register", command=self.register)
        self.btn_register.grid(row=2, column=1, pady=10)
    
    def login(self):
        email = self.ent_email.get()
        password = self.ent_password.get()
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            self.master.destroy()
            root = tk.Tk()
            app = MainApplication(root, email)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid email or password")
    
    def register(self):
        email = self.ent_email.get()
        password = self.ent_password.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration successful!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists")

class MainApplication:
    def __init__(self, master, email):
        self.master = master
        self.email = email
        self.master.title("CRUD Application")
        
        # Items Frame
        self.items_frame = tk.Frame(master)
        self.items_frame.pack(pady=20)
        
        # Listbox
        self.lst_items = tk.Listbox(self.items_frame, width=50)
        self.lst_items.pack(side=tk.LEFT)
        
        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.items_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.lst_items.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lst_items.yview)
        
        # Entry and Buttons
        self.ent_item = tk.Entry(master, width=50)
        self.ent_item.pack()
        
        self.btn_add = tk.Button(master, text="Add", command=self.add_item)
        self.btn_add.pack(side=tk.LEFT, padx=5)
        
        self.btn_update = tk.Button(master, text="Update", command=self.update_item)
        self.btn_update.pack(side=tk.LEFT, padx=5)
        
        self.btn_delete = tk.Button(master, text="Delete", command=self.delete_item)
        self.btn_delete.pack(side=tk.LEFT, padx=5)
        
        self.load_items()
    
    def load_items(self):
        self.lst_items.delete(0, tk.END)
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM items WHERE user_email=?", (self.email,))
        items = c.fetchall()
        conn.close()
        
        for item in items:
            self.lst_items.insert(tk.END, f"{item[0]}: {item[1]}")
    
    def add_item(self):
        item = self.ent_item.get()
        if item:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO items (name, user_email) VALUES (?, ?)", (item, self.email))
            conn.commit()
            conn.close()
            self.ent_item.delete(0, tk.END)
            self.load_items()
    
    def update_item(self):
        selected = self.lst_items.curselection()
        if selected:
            new_text = self.ent_item.get()
            if new_text:
                item_id = self.lst_items.get(selected[0]).split(":")[0]
                conn = sqlite3.connect('users.db')
                c = conn.cursor()
                c.execute("UPDATE items SET name=? WHERE id=?", (new_text, item_id))
                conn.commit()
                conn.close()
                self.load_items()
    
    def delete_item(self):
        selected = self.lst_items.curselection()
        if selected:
            item_id = self.lst_items.get(selected[0]).split(":")[0]
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("DELETE FROM items WHERE id=?", (item_id,))
            conn.commit()
            conn.close()
            self.load_items()

if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()


This application includes:

1. *Database Setup*:
   - SQLite database (users.db)
   - Two tables:
     - users for storing email and password
     - items for CRUD operations with user association

2. *Login System*:
   - Email-based authentication
   - Registration system
   - Password field masking
   - Error handling for existing emails

3. *CRUD Operations*:
   - Add items
   - Update items
   - Delete items
   - List items
   - User-specific data management

4. *GUI Features*:
   - Tkinter-based interface
   - Scrollable listbox
   - Input validation
   - User feedback messages

To use this application:

1. Run the script
2. Register with an email and password
3. Login with your credentials
4. Use the CRUD interface to:
   - Add items (type in the entry field and click Add)
   - Update items (select item, edit text, click Update)
   - Delete items (select item and click Delete)

The database will be automatically created in the same directory as the script (users.db).

You can enhance this further by:
- Adding password hashing
- Implementing email validation
- Adding more fields to user registration
- Adding search functionality
- Implementing proper error handling
- Adding a logout system
- Adding admin privileges
- Implementing database connection pooling