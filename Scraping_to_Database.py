# scrape data, then save to a sqlite database.

import sqlite3
import requests 
from bs4 import BeautifulSoup

# create db connection and cursor.
def scrape_books(url):
    # request url.
    response = requests.get(url)
    # initialize BS. 
    soup = BeautifulSoup(response.text, "html.parser")
    # locate data from html using BS.
    books = soup.find_all("article")
    # list to hold all book data.
    all_books = []
    # retrieve all data from each book using defined functions.
    for book in books:
        book_data = (get_title(book), get_price(book), get_rating(book))
        all_books.append(book_data)
    save_books(all_books)

# save all book data extracted from url, to a db.
def save_books(all_books):
    # establish/create connection to database.
    connection = sqlite3.connect("books.db")
    # create cursor object from connection.
    cursor = connection.cursor()
    # create table.
    cursor.execute('''CREATE TABLE books 
        (title TEXT, price REAL, rating INTEGER)''')
    cursor.executemany("INSERT INTO books VALUES (?,?,?)", all_books)
    # commit changes to db.
    connection.commit()
    # close connection when done.
    connection.close()
    
def get_title(book):
    return book.find("h3").find("a")["title"]

def get_price(book):
    price = book.select(".price_color")[0].get_text()
    return float(price.replace("Â", "").replace("£", ""))

def get_rating(book):
    ratings = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    paragraph = book.select(".star-rating")[0]
    word = paragraph.get_attribute_list("class")[-1]
    return ratings[word]

# function call to execute scraping.
scrape_books("http://books.toscrape.com/catalogue/category/books/history_32/index.html")
