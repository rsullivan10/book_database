from models import Base, session, Book, engine

# create a database 
# books.db
# create a modle
# title , author, date published, price

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    