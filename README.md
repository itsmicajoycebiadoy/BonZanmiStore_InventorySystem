# Bon-Zanmi Store Inventory System

## I. Project Overview

The Bon-Zanmi Store Inventory System is a Python-based graphical user interface (GUI) application that is designed to facilitate the management of inventory items in a retail environment, and this application allows users to add, update, delete, and search for items within the inventory while providing a user-friendly interface. In addition, the system connects to a Xampp (MySQL) database that ensure that all inventory data is stored persistently and can be easily accessed and modified. All in all, this project aims to streamline inventory management processes, thereby enhancing operational efficiency in stores.

## II. Explanation of Python Concepts and Libraries Applied

### Python Concepts
- Object-Oriented Programming (OOP): This application is structured using functions that encapsulate specific functionalities which promotes code reusability and organization.
- Error Handling: The application includes error handling mechanisms using try-except blocks to manage exceptions that may arise during database operations or user input.

### Libraries Used
- Tkinter: A standard GUI toolkit for Python, Tkinter is used to create the graphical interface of the application, allowing users to interact with the inventory system easily.
- ttk (Themed Tkinter): An extension of Tkinter, ttk is used for advanced widgets like `Treeview` and `Combobox`, enhancing the visual appeal and functionality of the GUI.
- pymysql: This library is used to connect and interact with a MySQL database, enabling the application to perform CRUD (Create, Read, Update, Delete) operations on inventory data.
- random: The random module is utilized to generate random Item IDs for new inventory items.
- tkcalendar: Although not currently implemented in the provided code, this library can be used for enhanced date selection functionalities.

## III. Details of the Chosen SDGs and Their Integration into the Project

The project integrates the principles of all 17 Sustainable Development Goals (SDGs) by promoting sustainable practices in inventory management. Here’s how the application aligns with each goal:

Zero Hunger: Efficient tracking of food items can help reduce waste and ensure that food products are sold before expiration, contributing to food security.
Industry, Innovation, and Infrastructure: The application encourages the adoption of technology in small retail businesses, fostering innovation.
Responsible Consumption and Production: The application promotes efficient inventory management, reducing waste and encouraging sustainable consumption patterns.

## IV. Instructions for Running the Program

### Prerequisites
- Python 3.x installed on your machine.
- MySQL server installed and running.

### Installation Steps
1. Clone the Repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
