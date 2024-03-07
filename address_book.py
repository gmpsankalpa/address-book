# address_book.py

import csv
from tkinter import messagebox

class AddressBook:
    def __init__(self):
        self.contacts = []
        self.load_from_file()

    def load_from_file(self):
        try:
            with open('contacts.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.contacts.append({'Name': row['Name'], 'Phone': row['Phone'], 'Email': row['Email']})
        except FileNotFoundError:
            # File doesn't exist yet; it will be created when saving
            pass

    def add_contact(self, name, phone, email):
        self.contacts.append({'Name': name, 'Phone': phone, 'Email': email})

    def edit_contact(self, name, phone=None, email=None):
        for contact in self.contacts:
            if contact['Name'] == name:
                if phone is not None:
                    contact['Phone'] = phone
                if email is not None:
                    contact['Email'] = email
                break

    def view_contact(self, name):
        for contact in self.contacts:
            if contact['Name'] == name:
                info = f"Name: {contact['Name']}\nPhone: {contact['Phone']}\nEmail: {contact['Email']}"
                messagebox.showinfo("Contact Details", info)
                break
        else:
            messagebox.showerror("Error", f"Contact {name} not found.")

    def list_contacts(self):
        return self.contacts

    def delete_contact(self, name):
        for i, contact in enumerate(self.contacts):
            if contact['Name'] == name:
                del self.contacts[i]
                break
        else:
            messagebox.showerror("Error", f"Contact {name} not found.")

    def search_contact(self, name):
        for contact in self.contacts:
            if contact['Name'] == name:
                return contact
        else:
            return None

    def get_contacts(self):
        return self.contacts
