# game logic part of project.

import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

# main web page.
BASE_URL = "http://quotes.toscrape.com"

def read_quotes(filename):
    with open(filename, "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)

def start_game(quotes):
    # get a randomly chose quote.
    quote = choice(quotes)
    # remaning number of guesses.
    remaining_guesses = 4
    # initiate users guess.
    guess = ''
    # display quote.
    print("Here's a quote: ")
    print(quote["text"])
    # give users multiple attempts, until number of remaining guesses is 0.
    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses}.\n")
        # check if user guesses correctly.
        if guess.lower() == quote["author"].lower():
            print("YOU GOT IT RIGHT!")
            break
        # if user didnt guess correctly, decrement guesses remaining.
        remaining_guesses -= 1
        # if user has guessed once already, give a hint, where author was born.
        if remaining_guesses == 3:
            # grab hint from "bio-link" of author/quote.
            res = requests.get(f"{BASE_URL}{quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            # store authors born date and location.
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            # display hint to user.
            print(f"Here's a hint: The author was born on {birth_date} {birth_place}.")
        # if user has guesses twice, give a hint using authors first name.
        elif remaining_guesses == 2:
            print(f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
        # if user has guesses three times, give another hint using authors last name.
        elif remaining_guesses == 1:
            last_initial = quote["author"].split(" ")[1][0]
            print(f"Here's a hint: The author's last name starts with: {last_initial}")
        # no more guesses remaining, reveal answer to user.
        else:
            print(f"Sorry you ran out of guesses. The answer was {quote['author']}")
    # ask the user if they would like to play again.
    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (y/n)?")
    if again.lower() in ('yes', 'y'):
        print("OK, YOU PLAY AGAIN!")
        return start_game(quotes)
    else:
        print("OK, GOODBYE!")

# get quotes from csv file.
quotes = read_quotes("quotes.csv")
# play game, passing all.
start_game(quotes)