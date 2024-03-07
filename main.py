# main.py

import tkinter as tk
from address_book_gui import AddressBookGUI
from address_book import AddressBook

if __name__ == "__main__":
    root = tk.Tk()
    app = AddressBookGUI(root)
    root.mainloop()
