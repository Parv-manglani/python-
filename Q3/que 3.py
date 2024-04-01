from datetime import datetime, timedelta

class Library:
    def _init_(self):
        self.catalog = {}
        self.users = {}
        self.transactions = []

    def add_book(self, book_id, title, author, quantity):
        self.catalog[book_id] = {'title': title, 'author': author, 'quantity': quantity}

    def display_catalog(self):
        print("Catalog:")
        for book_id, details in self.catalog.items():
            print(f"ID: {book_id}, Title: {details['title']}, Author: {details['author']}, Quantity Available: {details['quantity']}")

    def register_user(self, user_id, name):
        self.users[user_id] = {'name': name, 'books_checked_out': []}

    def checkout_book(self, user_id, book_id):
        if user_id not in self.users:
            print("User not registered.")
            return
        if book_id not in self.catalog:
            print("Book not found in catalog.")
            return
        if len(self.users[user_id]['books_checked_out']) >= 3:
            print("User has already checked out the maximum number of books.")
            return
        if self.catalog[book_id]['quantity'] == 0:
            print("Book not available for checkout.")
            return

        self.transactions.append({'user_id': user_id, 'book_id': book_id, 'checkout_date': datetime.now()})
        self.catalog[book_id]['quantity'] -= 1
        self.users[user_id]['books_checked_out'].append(book_id)
        print("Book checked out successfully.")

    def return_book(self, user_id, book_id):
        if user_id not in self.users:
            print("User not registered.")
            return
        if book_id not in self.users[user_id]['books_checked_out']:
            print("Book not checked out by this user.")
            return

        checkout_date = None
        for transaction in self.transactions:
            if transaction['user_id'] == user_id and transaction['book_id'] == book_id:
                checkout_date = transaction['checkout_date']
                self.transactions.remove(transaction)
                break

        self.catalog[book_id]['quantity'] += 1
        self.users[user_id]['books_checked_out'].remove(book_id)
        print("Book returned successfully.")

        if checkout_date:
            due_date = checkout_date + timedelta(days=14)
            if datetime.now() > due_date:
                days_overdue = (datetime.now() - due_date).days
                fine = days_overdue * 1
                print(f"Book returned {days_overdue} days overdue. Fine: ${fine}")

    def list_overdue_books(self, user_id):
        if user_id not in self.users:
            print("User not registered.")
            return

        overdue_books = []
        total_fine = 0
        for transaction in self.transactions:
            if transaction['user_id'] == user_id:
                book_id = transaction['book_id']
                checkout_date = transaction['checkout_date']
                due_date = checkout_date + timedelta(days=14)
                if datetime.now() > due_date:
                    days_overdue = (datetime.now() - due_date).days
                    fine = days_overdue * 1
                    overdue_books.append({'book_id': book_id, 'days_overdue': days_overdue, 'fine': fine})
                    total_fine += fine

        if overdue_books:
            print("Overdue Books:")
            for book in overdue_books:
                print(f"Book ID: {book['book_id']}, Days Overdue: {book['days_overdue']}, Fine: ${book['fine']}")
            print(f"Total Fine: ${total_fine}")
        else:
            print("No overdue books found for this user.")

# Example usage:
library = Library()
library.add_book(1, "The Great Gatsby", "F. Scott Fitzgerald", 5)
library.add_book(2, "To Kill a Mockingbird", "Harper Lee", 3)
library.add_book(3, "1984", "George Orwell", 2)

library.register_user(1, "Alice")
library.register_user(2, "Bob")

library.display_catalog()

library.checkout_book(1, 1)
library.checkout_book(1, 2)
library.checkout_book(1, 3)
library.checkout_book(2, 2)

library.return_book(1, 1)
library.return_book(1, 3)

library.list_overdue_books(1)