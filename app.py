from models import Base, session, Book, engine
import csv
import datetime
import time

#display main menu function
def menu():
    '''
    Main menu for the application
    Returns menu choice from user
    '''
    while True:
        print('''
          \nPROGRAMMING BOOKS
          \r1) Add book
          \r2) View all books
          \r3) Search for a book
          \r4) Book Analysis
          \r5) Exit
          ''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('Please choose one of the menu items above. '
                    'A number between 1-5.\nPress enter.')
#clean date function
def clean_date(date):
    '''
    Cleans the date string
    '''
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    split = date.split(' ')
    try:
        month = int(months.index(split[0]) + 1)
        day = int(split[1].split(',')[0])
        year = int(split[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input("""
            \n---------------------------DATE_ERROR!-------------------------
            \rThe date must include a valid Month Date and Year from the past
            \rEx: October 25, 2017
            \rPress enter to try again..
            \r---------------------------------------------------------------
            \r:""")
        return
    else:
        return return_date

def clean_price(price):
    '''
    Cleans the price string
    '''
    try:
        price_float = float(price)
    except ValueError:
                input("""
            \n-------------------------PRICE_ERROR!--------------------------
            \rThe price should be a number without a currency symbol
            \rEx: 29.99
            \rPress enter to try again..
            \r---------------------------------------------------------------
            \r:""")
    else: 
        return int(price_float * 100)

def clean_id(id_str, options):
    try:
        book_id = int(id_str)  
    except ValueError:
        input("""
            \n--------ID_ERROR!--------
            \rThe ID should be a number
            \rPress enter to try again..
            \r--------------------------
            \r:""")
        return
    else:
        if book_id in options:
            return book_id
        else: 
            input(f"""
            \n--------ID_ERROR!--------
            \ryour options are {options}
            \rPress enter to try again..
            \r--------------------------
            \r:""")
            return

def add_csv():
    '''
    Add books from csv to database 
    if they aren't in the DB already
    '''
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            date = clean_date(row[2])
            price = clean_price(row[3])
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                new_book = Book(title=row[0], author=row[1], published_date=date, price=price)
                session.add(new_book)
    session.commit()

def app():
    '''
    Main application function
    '''
    app_running = True
    while app_running:
        
        choice = menu()
        
        if choice == '1':
            title = input('Title: ')
            author = input('Author: ')
            
            date_error = True
            while date_error:
                date = input('Published Date(Ex: October 25, 2017): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            
            price_error = True
            while price_error:
                price = input('Price (Ex: 29.99): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            
            new_book = Book(title = title, author = author, published_date = date, price= price)
            session.add(new_book)
            session.commit()
            print('Book Added!')
            time.sleep(1.5)
        
        elif choice == '2':
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author} | {book.published_date} | {book.price}')
            input('\n Press enter to return to the main menu...')
        
        elif choice == '3':
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            
            id_error = True
            while id_error:
                id_choice = input(f"""
                    \nid Options: {id_options}
                    \rBook id: """)
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id==id_choice).first()
            print(f"""
                  \n{the_book.title} by {the_book.author}
                  \rPublished: {the_book.published_date}
                  \rPrice: ${the_book.price / 100}""")
            input('\nPress enter to continue...')
       
        elif choice == '4':
            pass
       
        else:
            print('GOODBYE')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()