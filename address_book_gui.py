# address_book_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import csv
from address_book import AddressBook

class AddressBookGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Address Book")
        self.master.geometry("400x500")

        self.address_book = AddressBook()

        self.label_name = tk.Label(master, text="Name:")
        self.label_phone = tk.Label(master, text="Phone:")
        self.label_email = tk.Label(master, text="Email:")

        self.entry_name = tk.Entry(master)
        self.entry_phone = tk.Entry(master)
        self.entry_email = tk.Entry(master)

        self.button_add = tk.Button(master, text="Add Contact", command=self.add_contact, bg="#4CAF50", fg="white")
        self.button_view = tk.Button(master, text="View Contact", command=self.view_contact, bg="#2196F3", fg="white")
        self.button_edit = tk.Button(master, text="Edit Contact", command=self.edit_contact, bg="#FFC107", fg="black")
        self.button_delete = tk.Button(master, text="Delete Contact", command=self.confirm_delete_contact, bg="#F44336", fg="white")
        self.button_list = tk.Button(master, text="List Contacts", command=self.list_contacts, bg="#607D8B", fg="white")
        self.button_search = tk.Button(master, text="Search Contact", command=self.search_contact, bg="#795548", fg="white")

        self.label_confirmation = tk.Label(master, text="", fg="green")
        self.label_search_result = tk.Label(master, text="", fg="blue")

        # Layout
        self.label_name.place(relx=0.5, rely=0.05, anchor="center")
        self.label_phone.place(relx=0.5, rely=0.15, anchor="center")
        self.label_email.place(relx=0.5, rely=0.25, anchor="center")

        self.entry_name.place(relx=0.5, rely=0.10, anchor="center", width=200)
        self.entry_phone.place(relx=0.5, rely=0.20, anchor="center", width=200)
        self.entry_email.place(relx=0.5, rely=0.30, anchor="center", width=200)

        self.button_add.place(relx=0.5, rely=0.47, anchor="center", width=150)
        self.button_view.place(relx=0.5, rely=0.54, anchor="center", width=150)
        self.button_edit.place(relx=0.5, rely=0.61, anchor="center", width=150)
        self.button_delete.place(relx=0.5, rely=0.68, anchor="center", width=150)
        self.button_list.place(relx=0.5, rely=0.75, anchor="center", width=150)
        self.button_search.place(relx=0.5, rely=0.82, anchor="center", width=150)

        self.label_confirmation.place(relx=0.5, rely=0.89, anchor="center")
        self.label_search_result.place(relx=0.5, rely=0.96, anchor="center")

    def add_contact(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()

        if name and phone and email:
            self.address_book.add_contact(name, phone, email)
            self.clear_entry_fields()
            self.save_to_file()
            self.label_confirmation.config(text=f"Contact {name} added successfully!")
        else:
            self.label_confirmation.config(text="Please fill in all fields.", fg="red")

    def view_contact(self):
        name = self.entry_name.get()
        self.address_book.view_contact(name)

    def edit_contact(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()

        if name:
            self.address_book.edit_contact(name, phone, email)
            self.clear_entry_fields()
            self.save_to_file()
            self.label_confirmation.config(text=f"Contact {name} updated successfully!")
        else:
            messagebox.showwarning("Incomplete Information", "Please enter a name.")

    def confirm_delete_contact(self):
        name = self.entry_name.get()
        if name:
            confirm = messagebox.askokcancel("Confirmation", f"Are you sure you want to delete {name}?")
            if confirm:
                self.address_book.delete_contact(name)
                self.clear_entry_fields()
                self.save_to_file()
                self.label_confirmation.config(text=f"Contact {name} deleted successfully!")
        else:
            messagebox.showwarning("Incomplete Information", "Please enter a name.")

    def list_contacts(self):
        contacts = self.address_book.get_contacts()
        self.show_list_window(contacts)

    def search_contact(self):
        name = self.entry_name.get()
        result = self.address_book.search_contact(name)
        if result:
            self.entry_name.delete(0, tk.END)
            self.entry_phone.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)

            self.entry_name.insert(0, name)
            self.entry_phone.insert(0, result['Phone'])
            self.entry_email.insert(0, result['Email'])

            self.label_search_result.config(text=f"Contact {name} found: {result['Phone']}, {result['Email']}")
        else:
            self.label_search_result.config(text=f"Contact {name} not found.", fg="red")

    def clear_entry_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

    def save_to_file(self):
        with open('contacts.csv', 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Phone', 'Email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for contact in self.address_book.contacts:
                writer.writerow({'Name': contact['Name'], 'Phone': contact['Phone'], 'Email': contact['Email']})

    def show_list_window(self, contacts):
        list_window = tk.Toplevel(self.master)
        list_window.title("Contacts List")

        tree = ttk.Treeview(list_window, columns=('Name', 'Phone', 'Email'), show='headings')

        tree.heading('Name', text='Name')
        tree.heading('Phone', text='Phone')
        tree.heading('Email', text='Email')

        for contact in contacts:
            tree.insert("", "end", values=(contact['Name'], contact['Phone'], contact['Email']))

        tree.pack(expand=True, fill='both')

        close_button = tk.Button(list_window, text="Close", command=list_window.destroy, bg="#F44336", fg="white")
        close_button.pack(pady=10)
