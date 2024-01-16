import csv
from datetime import datetime, timedelta
import random
from tinydb import TinyDB, Query
tbook_id = 1
ttitle = "Available"
tauthor = "Available"
tgenre = "Available"
tstatus = "Available"
def search_book_in_db(filename, search_term):
    db = TinyDB(filename)
    BookQuery = Query()
    search_term_lower = search_term.lower()

    for book in db.search((BookQuery.title.test(lambda v: search_term_lower in v.lower())) | 
                          (BookQuery.author.test(lambda v: search_term_lower in v.lower())) | 
                          (BookQuery.book_id.test(lambda v: search_term_lower in v.lower()))):
        return book

    return "Sorry for the inconvenience. Your requested book is unavailable"

class Book:
    def __init__(self, book_id, title, author, genre, status, issued_to, issued_datetime, return_date):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.status = status
        self.issued_to = issued_to
        self.issued_datetime = self._convert_to_datetime(issued_datetime)
        self.return_date = self._convert_to_datetime(return_date)

    @staticmethod
    def _convert_to_datetime(date_str, time_format="%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(date_str, time_format) if date_str else None
        except ValueError:
            return None



class Book:
    def __init__(self, book_id, title, author, genre, status, issued_to, issued_datetime, return_date):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.status = status
        self.issued_to = issued_to
        self.issued_datetime = self._convert_to_datetime(issued_datetime)
        self.return_date = self._convert_to_datetime(return_date)

    @staticmethod
    def _convert_to_datetime(date_str, time_format="%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(date_str, time_format) if date_str else None
        except ValueError:
            return None

class Library:
    def __init__(self, filename):
        self.db = TinyDB(filename)
        self.books = self._load_books()

    def _load_books(self):
        return [Book(**book) for book in self.db.all()]

    def donate_book(self):
        global tbook_id
        global ttitle 
        global tauthor 
        global tgenre 
        global tstatus
        book_id = input("Enter book ID: ")
        title = input("Enter title: ")
        author = input("Enter author: ")
        genre = input("Enter genre: ")
        status = "Available"

        tbook_id = book_id
        ttitle = title
        tauthor = author
        tgenre = genre
        tstatus = status

        self.db.insert({
            'book_id': book_id, 
            'title': title, 
            'author': author, 
            'genre': genre, 
            'status': status, 
            'issued_to': '', 
            'issued_datetime': '', 
            'return_date': ''
        })
        self.books = self._load_books()
        print(f"{title} - by {author} added successfully")

        if random.randint(0, 5) >= 3:
            print("\nThe Book Investigation Just Came in")
            print("The Book is well Maintained, thus you are eligible for a Gift Card")
            print("Kindly Visit the Reception for Further Details\n")

    
    def search_book(self, search_term):
        db2 = TinyDB('library_db.json')
        BookQuery = Query()
        search_term_lower = search_term.lower()

        for book_dict in db2.search((BookQuery.title.test(lambda v: search_term_lower in v.lower())) | 
                                (BookQuery.author.test(lambda v: search_term_lower in v.lower())) | 
                                (BookQuery.book_id.test(lambda v: search_term_lower in v.lower()))):
            return Book(**book_dict)

        print("Sorry for the inconvenience. Your requested book is unavailable")
        return None



    def issue_book(self, book_id, member_name):
        book = self.search_book(book_id)
        if not book or book.status == "Issued":
            print(f"Cannot issue book. Status: {book.status}" if book else "Book not found.")
            return
        
        # Update book details
        book.status = "Issued"
        book.issued_to = member_name
        book.issued_datetime = datetime.now()
        book.return_date = book.issued_datetime + timedelta(days=10)
        
        # Update the database
        self._update_book_data(book)
        print(f"Book '{book.title}' issued to {member_name}. Return Date: {book.return_date.strftime('%Y-%m-%d')}")

    def return_book(self, book_id):
        book = self.search_book(book_id)
        if not book or book.status == "Available":
            print(f"Cannot return book. Status: {book.status}" if book else "Book not found.")
            return

        # Update book details
        book.status = "Available"
        book.issued_to = ""
        book.issued_datetime = None
        book.return_date = None

        # Update the database
        self._update_book_data(book)
        print(f"Book '{book.title}' returned successfully!")


    

    def _update_book_data(self, updated_book):
        BookQuery = Query()
        self.db.update({
            'status': updated_book.status,
            'issued_to': updated_book.issued_to,
            'issued_datetime': updated_book.issued_datetime.strftime("%Y-%m-%d %H:%M:%S") if updated_book.issued_datetime else '',
            'return_date': updated_book.return_date.strftime("%Y-%m-%d") if updated_book.return_date else ''
        }, BookQuery.book_id == updated_book.book_id)


# Main execution starts here
library = Library('library_db.json')

from tinydb import TinyDB, Query





# Run the main method
   
while True:
    print("\nWelcome to Pranjal's Library Management System")
    print("Choose the following options to access our Library Management\n")
    print("1. Display Books")
    print("2. Donate a Book")
    print("3. Search for a book")
    print("4. Issue a book")
    print("5. Return a book")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "2":
        library.donate_book()

    
    elif choice == "1":
        library.books = library._load_books()
        for book in library.books:
            print(f"Book ID: {book.book_id}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}, Status: {book.status}")
        #print(f"Book ID: {tbook_id}, Title: {ttitle}, Author: {tauthor}, Genre: {tgenre}, Status: {tstatus}")
    elif choice == "3":
        # Example usage
        filename = 'library_db.json'
        search_term = input("Enter Title, Author, or Book ID to search: ")
        result = search_book_in_db(filename, search_term)
        print(result)
    
    elif choice == "4":
        book_id = input("Enter book ID: ")
        member_name = input("Enter member name: ")
        library.issue_book(book_id, member_name)
    elif choice == "5":
        book_id2 = input("Enter book ID: ")
        
        
        library.return_book(book_id2)
    elif choice == "6":
        print("Thank You for Using Pranjal's Library Management System\n")
        break
    else:
        print("Invalid Response, Kindly Try Again\n")
