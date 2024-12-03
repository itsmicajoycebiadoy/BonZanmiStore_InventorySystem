# Import necessary libraries

from tkinter import *  # Import all classes and functions from the tkinter module for creating GUI applications

from tkinter import ttk  # Import the themed tkinter module for advanced widgets like Treeview, Combobox, etc.

from tkinter import messagebox  # Import messagebox for displaying dialog boxes (like warnings and info)

import tkinter  # Import the tkinter module (not necessary since we imported everything above, but can be useful for additional functionalities)

import random  # Import the random module for generating random numbers (used in generating random item IDs)

import pymysql  # Import pymysql to connect and interact with MySQL databases

import csv  # Import csv module for reading and writing CSV files (not currently used in the provided code)

import numpy as np  # Import numpy for numerical operations (not currently used in the provided code)

from tkinter import StringVar  # Import StringVar class to create string variables that can be used with tkinter widgets

from tkcalendar import DateEntry  # Import DateEntry from tkcalendar for a calendar widget (not currently used in the provided code)

# Create the main application window

window = tkinter.Tk()

window.title("Bon-Zanmi Store Inventory System")

# Function to toggle fullscreen mode

def toggle_fullscreen(event=None):

    window.attributes('-fullscreen', True)

# Function to exit fullscreen mode

def end_fullscreen(event=None):

    window.attributes('-fullscreen', False)

# Configure the main window's background color

window.configure(bg="#DDA0DD")

# Start the window in a maximized state

window.state('zoomed')

# Initialize frames

welcome_frame = Frame(window, bg="pink")

inventory_frame = Frame(window, bg="#DDA0DD")

# Function to show the inventory frame and hide the welcome frame

def show_inventory():

    welcome_frame.pack_forget()  # Hide the welcome frame

    inventory_frame.pack(fill=BOTH, expand=True)  # Show the inventory frame

    refreshTable() 

# Button to enter the inventory system at the bottom

enter_button = Button(welcome_frame, text="Enter Inventory System", font=("Helvetica", 16), command=show_inventory)

enter_button.pack(side=BOTTOM, padx=0, pady= 10)  # Pack the button at the bottom

window.bind('<Return>', lambda event: show_inventory())

# Welcome Page

welcome_label = Label(welcome_frame, text="Welcome to Bon-Zanmi Inventory System!", font=("Times new roman", 30), bg="pink")

welcome_label.pack(pady=370)

# Pack the welcome frame first

welcome_frame.pack(fill=BOTH, expand=True)

# Start the window in a maximized state
my_tree = ttk.Treeview(window,show = 'headings',height = 20)

style=ttk.Style()

# Array to hold placeholder text for entry fields
placeholderArray = [tkinter.StringVar() for _ in range(7)]

# Define numeric and alphabetic characters for ID generation
numeric='1234567890'

alpha='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Function to handle click event on entry fields
def on_entry_click(event):

    if event.widget.get() == 'YYYY-MM-DD':
        
        event.widget.delete(0, "end") 

        event.widget.config(fg='black')  

# Function to handle focus out event on entry fields
def on_focusout(event):

    if event.widget.get() == '':

        event.widget.insert(0, 'YYYY-MM-DD') 

        event.widget.config(fg='black') 

# Function to establish a connection to the MySQL database       
def connection():

    conn = pymysql.connect(

        host = 'localhost',

        user = 'root',

        password = '',

        db = 'stockmanagementsystem'
    )
    return conn

# Establish database connection
conn = connection()

cursor = conn.cursor()


# Initialize placeholder variables for entry fields
for i in range(0,5):

    placeholderArray[i] = tkinter.StringVar()

# Function to read data from the database
def read():

    cursor.connection.ping()

    sql = f"SELECT `item_id`, `name`, `packaging_size`, `price`, `quantity`, `category`, `expiration_date` FROM stocks ORDER BY `expiration_date` ASC"

    cursor.execute(sql)

    results = cursor.fetchall()

    conn.commit()

    return results 

# Function to refresh the data displayed in the Treeview
def refreshTable():

    for data in my_tree.get_children():

        my_tree.delete(data)

    for array in read():

        item_quantity = int(array[4])  # Assuming quantity is the 5th element in the array

        if item_quantity <= 0 :

            my_tree.insert(parent='', index='end', id=array, text="", values=(array), tag="OutOfStock")

        else:

            my_tree.insert(parent='', index='end', id=array, text="", values=(array), tag="orow")

    my_tree.tag_configure('orow', background='#FFC0CB')  # Normal items

    my_tree.tag_configure('OutOfStock', background="lavender", foreground = "black")  # Out of stock items
    
    my_tree.pack()

# Function to set placeholder text in entry fields

def setph(word,num):

    for ph in range (0,6):
        
        if ph == num:

            placeholder[ph].set(word)

# Function to generate a random item ID

def generateRand():

    itemId=''

    for i in range(0,3):

        randno = random.randrange (0,(len(numeric)-1))

        itemId = itemId + str(numeric[randno])

    radno = random.randrange (0,(len(alpha)-1))

    itemId = itemId + '-' + str(alpha[randno])

    print("generated: " + itemId)

    setph(itemId, 0)

# Function to save new item data to the database
def save():

    itemId = str(itemIdEntry.get())

    name = str(nameEntry.get())

    packaging_size = str(packagingSizeEntry.get())

    price = str(priceEntry.get())

    qnt = str(qntEntry.get())

    cat = str(categoryCombo.get())

    expiration_date = str(expirationDateEntry.get())

    valid = True

    # Check if all fields are filled
    if not (itemId and itemId.strip()) or not (name and name.strip()) or not (packaging_size and packaging_size.strip()) or not (price and price.strip()) or not (qnt and qnt.strip()) or not (cat and cat.strip()) or not (expiration_date and expiration_date.strip()):

        messagebox.showwarning("", "Please fill up all entries")

        return

    # Validate Item Id format
    if len(itemId) < 5 or not (itemId[3] == '-'):

        messagebox.showwarning("", "Invalid Item Id")

        return

    for i in range(0, 3):

        if not (itemId[i] in numeric):

            valid = False

            break

    if not (itemId[4] in alpha):

        valid = False

    if not valid:

        messagebox.showwarning("", "Invalid Item Id")

        return

    try:
        cursor.connection.ping()

        # Check if item_id or name already exists in the database
        cursor.execute("SELECT * FROM stocks WHERE `item_id` = %s OR `name` = %s", (itemId, name))

        existing_item = cursor.fetchall()
        
        if existing_item:

            messagebox.showwarning("", "The Item Id or Name is already used.")

            return

        # Insert new item into the database
        sql = f"INSERT INTO stocks (`item_id`, `name`, `packaging_size`, `price`, `quantity`, `category`, `expiration_date`) VALUES ('{itemId}', '{name}', '{packaging_size}', '{price}', '{qnt}', '{cat}', '{expiration_date}')"

        cursor.execute(sql)

        conn.commit()

        # Refresh the table

        refreshTable()

        messagebox.showinfo("", "Item saved successfully.")

    except Exception as e:

        messagebox.showwarning("", f"Error while saving: {str(e)}")


# Function to update item data to the database
def update():

    try:

        selectedItem = my_tree.selection()[0]

        selectedItemId = str(my_tree.item(selectedItem)['values'][0])

    except IndexError:

        messagebox.showwarning("", "Please select a data row")

        return

    itemId = str(itemIdEntry.get())

    name = str(nameEntry.get())

    packaging_size = str(packagingSizeEntry.get())

    price = str(priceEntry.get())

    qnt = str(qntEntry.get())

    cat = str(categoryCombo.get())

    expiration_date = str(expirationDateEntry.get())

    # Check if all fields are filled
    if not (itemId and itemId.strip()) or not (name and name.strip()) or not (packaging_size and packaging_size.strip()) or not (price and price.strip()) or not (qnt and qnt.strip()) or not (cat and cat.strip()) or not (expiration_date and expiration_date.strip()):

        messagebox.showwarning("", "Please fill up all entries")

        return

    # Check if the selected item ID is being changed (which should not happen)
    if selectedItemId != itemId:

        messagebox.showwarning("", "You can't change Item ID.")

        return

    try:
        cursor.connection.ping()

        # Check if the new name or item_id already exists in the database

        cursor.execute("SELECT * FROM stocks WHERE (`item_id` = %s OR `name` = %s) AND `item_id` != %s", (itemId, name, selectedItemId))

        existing_item = cursor.fetchall()

        if existing_item:

            messagebox.showwarning("", "The Item Id or Name is already used by another item.")

            return

        # Update the item in the database
        sql = f"UPDATE stocks SET name='{name}', packaging_size='{packaging_size}', price='{price}', quantity='{qnt}', category='{cat}', expiration_date='{expiration_date}' WHERE item_id='{selectedItemId}'"

        cursor.execute(sql)

        conn.commit()

        # Refresh the table and clear the form
        messagebox.showinfo("", "Data has been successfully updated.")

        clear()
        
        refreshTable()

    except Exception as e:

        messagebox.showwarning("", f"Error occurred while updating: {str(e)}")


# Function to delete item data to the database
def delete():

    try:

        if(my_tree.selection()[0]):

            decision = messagebox.askquestion("","Delete the selected data?")

            if(decision != 'yes'):

                return

            else:

                selectedItem = my_tree.selection()[0]

                itemId = str(my_tree.item(selectedItem)['values'][0])

                try:

                    cursor.connection.ping()

                    sql = f"DELETE FROM stocks WHERE `item_id` = '{itemId}' "

                    cursor.execute(sql)

                    conn.commit()

                    conn.close()

                    messagebox.showinfo("","Data has been successfully deleted")

                except:

                    messagebox.showinfo("","Sorry, an error occured")

                refreshTable()

    except:

        messagebox.showwarning("","Please select a data row")

# Function to select item data to the database
def select():

    try:

        selectedItem = my_tree.selection()[0]

        itemId = str(my_tree.item(selectedItem)['values'][0])

        name = str(my_tree.item(selectedItem)['values'][1])

        packaging_size = str(my_tree.item(selectedItem)['values'][2])

        price = str(my_tree.item(selectedItem)['values'][3])

        qnt = str(my_tree.item(selectedItem)['values'][4])

        cat = str(my_tree.item(selectedItem)['values'][5])

        expiration_date = str(my_tree.item(selectedItem)['values'][6])

        setph(itemId,0)

        setph(name,1)

        setph(packaging_size,2)

        setph(price,3)

        setph(qnt,4)

        setph(cat,5)

        setph(expiration_date,6)

    except IndexError:

        messagebox.showwarning("", "Please select a data row")

    except Exception as e:

        messagebox.showwarning("", "An error occurred: " + str(e))

# Function to find item data to the database

def find():

    itemId = str(itemIdEntry.get())

    name = str(nameEntry.get())

    packaging_size = str(packagingSizeEntry.get())

    price = str(priceEntry.get())

    qnt = str(qntEntry.get())

    cat = str(categoryCombo.get())

    expiration_date = str(expirationDateEntry.get())  

    cursor.connection.ping()

    query_conditions = []
    
    if itemId and itemId.strip():

        query_conditions.append(f"`item_id` LIKE '%{itemId}%'")

    if name and name.strip():

        query_conditions.append(f"`name` LIKE '%{name}%'")

    if packaging_size and packaging_size.strip(): 

        query_conditions.append(f"`packaging_size` LIKE '%{packaging_size}%'")

    if price and price.strip():

        query_conditions.append(f"`price` LIKE '%{price}%'")

    if qnt and qnt.strip():

        query_conditions.append(f"`quantity` LIKE '%{qnt}%'")

    if cat and cat.strip():

        query_conditions.append(f"`category` LIKE '%{cat}%'")

    if expiration_date and expiration_date.strip():

        query_conditions.append(f"`expiration_date` LIKE '%{expiration_date}%'")  

    if not query_conditions:

        messagebox.showwarning("", "Please fill up one of the entries")

        return

    sql = f"SELECT `item_id`, `name`, `packaging_size`, `price`, `quantity`, `category`, `expiration_date` FROM stocks WHERE {' OR '.join(query_conditions)}"
    
    cursor.execute(sql)

    try:

        result = cursor.fetchall()

        if result:

            for num in range(0, 7):

                setph(result[0][num], num)
        else:

            messagebox.showwarning("", "No data found")

    except Exception as e:

        messagebox.showwarning("", "Error occurred: " + str(e))

def clear():

    # Clears all the placeholder entries by setting them to empty strings
    for num in range(0, 7):

        setph('', (num))  # Calls setph to clear the value in each placeholder

# Left Frame for form inputs
left_frame = Frame(window, bg="#FF69B4")

left_frame.pack(side=LEFT, fill=Y, padx=(20, 0), pady=20)

# Color for buttons
btnColor = "#EE82EE"

# Right Frame for other content (e.g., tree view, tables)
right_frame = Frame(window)

right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(0, 20), pady=20)

# LabelFrame for the input form fields
entriesFrame = LabelFrame(left_frame, text="Stock Management System", borderwidth=5)

entriesFrame.pack(fill=X, pady= 10, padx=10)

# Labels for each form field
itemIdLabel = Label(entriesFrame, text="ITEM ID", anchor="e", width=10)

itemIdLabel.grid(row=0, column=0, padx=20)

nameLabel = Label(entriesFrame, text="NAME", anchor="e", width=10)

nameLabel.grid(row=1, column=0, padx=20)

packagingSizeLabel = Label(entriesFrame, text="PCKGNG SIZE", anchor="e", width=10)

packagingSizeLabel.grid(row=2, column=0, padx=20)

priceLabel = Label(entriesFrame, text="PRICE", anchor="e", width=10)

priceLabel.grid(row=3, column=0, padx=20)

qntLabel = Label(entriesFrame, text="STOCKS PER PC", anchor="e", width=12)

qntLabel.grid(row=4, column=0, padx=20)

categoryLabel = Label(entriesFrame, text="CATEGORY", anchor="e", width=10)

categoryLabel.grid(row=5, column=0, padx=20)

expirationDateLabel = Label(entriesFrame, text="EXPIRATION DATE", anchor="e", width=15)

expirationDateLabel.grid(row=6, column=0, padx=20)

# Label to show date format instruction
expirationFormatLabel = Label(entriesFrame, text="Format: YYYY-MM-DD", anchor="w", fg='black')

expirationFormatLabel.grid(row=7, column=2, padx=5, pady=5)

# Category options for the combobox
categoryArray = ['Instant Noodles', 'Canned Goods', 'Candy', 'Soda', 'Detergent', 'Rice', 'Coffee', 'Shampoo', 'Conditioner', 'Toothpaste', 'Medicine', 'Snacks', 'Diapers', 'Cigarettes']

# Entries for each form field, using placeholders
itemIdEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[0])

itemIdEntry.grid(row=0, column=2, padx=10, pady=30)

nameEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[1])

nameEntry.grid(row=1, column=2, padx=10, pady=30)

packagingSizeEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[2])

packagingSizeEntry.grid(row=2, column=2, padx=10, pady=30)

priceEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[3])

priceEntry.grid(row=3, column=2, padx=10, pady=30)

qntEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[4])

qntEntry.grid(row=4, column=2, padx=10, pady=30)

# Category dropdown combo box
categoryCombo = ttk.Combobox(entriesFrame, width=47, textvariable=placeholderArray[5], values=categoryArray)

categoryCombo.grid(row=5, column=2, padx=10, pady=30)

# Expiration date entry with placeholder text
expirationDateEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[6])

expirationDateEntry.insert(0, 'YYYY-MM-DD')  # Default text for expiration date

expirationDateEntry.bind("<FocusIn>", on_entry_click)  # Focus in event handler for placeholder

expirationDateEntry.bind("<FocusOut>", on_focusout)  # Focus out event handler to revert placeholder

expirationDateEntry.config(fg='black') 

expirationDateEntry.grid(row=6, column=2, padx=10, pady=30)

# Manage Frame for action buttons (Save, Update, Delete, etc.)
manageFrame = LabelFrame(left_frame, text="Manage", borderwidth=5)

manageFrame.pack(fill=X, padx=10, pady=10)

# Buttons for various actions
saveBtn = Button(manageFrame, text="SAVE", width=10, borderwidth=3, bg=btnColor, fg='bLACK', command=save)

updateBtn = Button(manageFrame, text="UPDATE", width=10, borderwidth=3, bg=btnColor, fg='bLACK', command=update)

deleteBtn = Button(manageFrame, text="DELETE", width=10, borderwidth=3, bg=btnColor, fg='bLACK', command=delete)

selectBtn = Button(manageFrame, text="SELECT", width=10, borderwidth=3, bg=btnColor, fg='bLACK', command=select)

findBtn = Button(manageFrame, text="FIND", width=10, borderwidth=3, bg=btnColor, fg='bLACK', command=find)

clearBtn = Button(manageFrame, text="CLEAR", width=10, borderwidth=3, bg=btnColor, fg='bLACK', command=clear)

# Positioning buttons in the grid layout
saveBtn.grid(row=0, column=0, padx=5, pady=5)

updateBtn.grid(row=0, column=1, padx=5, pady=5)

deleteBtn.grid(row=0, column=2, padx=5, pady=5)

selectBtn.grid(row=0, column=3, padx=5, pady=5)

findBtn.grid(row=0, column=4, padx=5, pady=5)

clearBtn.grid(row=0, column=5, padx=5, pady=5)

# Keyboard shortcuts for button actions
window.bind('<Control-s>', lambda event: save())  # Save action

window.bind('<Control-u>', lambda event: update())  # Update action

window.bind('<Control-d>', lambda event: delete())  # Delete action

window.bind('<Control-Return>', lambda event: select())  # Select action

window.bind('<Control-f>', lambda event: find())  # Find action

window.bind('<Control-c>', lambda event: clear())  # Clear action

# Button to generate random item ID
generateIdBtn = Button(entriesFrame, text="GENERATE ID", borderwidth=3, bg=btnColor, fg='BLACK', command=generateRand)

generateIdBtn.grid(row=0, column=3, padx=5, pady=5)

# Apply styles to Treeview widget
style = ttk.Style()

style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"), background="FF1493")

style.configure("Treeview", font=("Arial", 13), background="#FF1493", fieldbackground="#FF1493", foreground="BLACK")

style.configure("OutOfStock", background="#FFB6C1")

my_tree = ttk.Treeview(right_frame, show='headings', height=60)

# Setting up the Treeview columns and their properties
my_tree['columns'] = ("Item Id", "Name", "Pckgng Size", "Price", "Qnt Stocks", "Category", "Exp Date")

# Treeview column configurations
my_tree.column("#0", width=0, stretch=NO)

my_tree.column("Item Id", anchor=W, width=80)

my_tree.column("Name", anchor=W, width=200)

my_tree.column("Pckgng Size", anchor=W, width=120)

my_tree.column("Price", anchor=W, width=80)

my_tree.column("Qnt Stocks", anchor=W, width=100)

my_tree.column("Category", anchor=W, width=180)

my_tree.column("Exp Date", anchor=W, width=100)

# Setting Treeview headings (labels)
my_tree.heading("Item Id", text="Item Id", anchor=W)

my_tree.heading("Name", text="Name", anchor=W)

my_tree.heading("Pckgng Size", text="Pckgng Size", anchor=W)

my_tree.heading("Price", text="Price", anchor=W)

my_tree.heading("Qnt Stocks", text="Qnt Stocks", anchor=W)

my_tree.heading("Category", text="Category", anchor=W)

my_tree.heading("Exp Date", text="Exp Date", anchor=W)

# Treeview row style configuration
my_tree.tag_configure('orow', background="#C71585")

my_tree.pack(fill=BOTH, expand=True)

# Function to set placeholder text for the form fields
def setph(word, num):

    for ph in range(0, 7):

        if ph == num:

            placeholderArray[ph].set(word)  # Update placeholderArray with new value

def exit_application():
    if messagebox.askyesno("Confirm Exit", "Do you really want to exit?"):
        window.destroy()  # This will close the Tkinter window

# Exit Button
exit_button = Button(left_frame, text="Exit", font=("Helvetica", 16), width=10, borderwidth=3, bg=btnColor, fg='bLACK', command=exit_application)

exit_button.pack(side=BOTTOM, padx=10, pady=10)  # Pack the button at the bottom

window.bind('<Escape>', lambda event: exit_application())

# Refresh the data in the table (not defined here)
refreshTable()

# Make the window non-resizable
window.resizable(False, False)

# Start the main loop for the Tkinter window
window.mainloop()
