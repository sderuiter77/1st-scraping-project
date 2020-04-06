import requests
from bs4 import BeautifulSoup
from random import choice
from pyfiglet import Figlet
from termcolor import colored
from colorama import init
init()

original_url = "http://quotes.toscrape.com"

class Game:
    
    def __init__(self):
        url = original_url
        next_url = '/page/1/'
        self.quotes = []

        while next_url:
            data = requests.get(url + next_url).text
            html = BeautifulSoup(data, features="html.parser")
            quotes = html.find_all(class_="quote")
            for quote in quotes:
                self.quotes.append(Quote(
                    quote.find(class_="text").text,
                    quote.find(class_="author").text,
                    quote.find("a")["href"]
                ))
            try:
                next_url = html.find(class_="next").find('a')["href"]
            except:
                break

    def __repr__(self):
        return f"A game with {len(self.quotes)} quotes"

    def play_game(self):
        self.play_quote = choice(self.quotes)
        self.quotes.remove(self.play_quote)
        self.play_quote._guess()

class Quote:

    def __init__(self, text, author, url):
        self.text = text
        self.author = author
        self.url = url
        self.num_guess = 4

    def __repr__(self):
        return f"A quote by {self.author}"

    def _guess(self):
        if self.num_guess == 4:
            print("Here's a quote:\n")
            print(colored(self.text,color='cyan'))
        # else: 
        #     print("Here's the quote again, you idiot:\n")
        
        if self.num_guess == 4:
            guess = input("\nWho said this quote?\n")
        else: 
            guess = input(f"I'll ask you again... who said this quote? {self.num_guess} guesses remaining..\n")
        if self._quote_true(guess) == True:
            print(f"You guessed right! The author is {self.author}\n") 
        else:
            self._wrong_answer(self.num_guess)

    def _wrong_answer(self, num):
        if num == 4:
            author_data = requests.get(original_url + self.url).text
            author_html = BeautifulSoup(author_data, "html.parser")
            author_date = author_html.find(class_="author-born-date").text
            author_location = author_html.find(class_="author-born-location").text
            print(f"\nWrong! Here's a little hint: \n\nThe author is born on {author_date} {author_location}\n")
            self.num_guess -= 1
            self._guess()
        elif num == 3:
            print(
                f"\nWrong! Here's another hint: \n\nAuthor's first name starts with: {self.author[0]}\n"
        )
            self.num_guess -= 1
            self._guess()
        elif num == 2:
            last_name = self.author.split(' ')[1][0]
            print(
                f"\nWrong again! Last hint: \n\nAuthor's last name starts with: {last_name}\n")
            self.num_guess -= 1
            self._guess()
        else:
            print(f"\nWrong! You lost. The author was {self.author}\n\n")

    def _quote_true(self, guess):
        if guess.lower() == self.author.lower():
            return True
        return False

f = Figlet(font='big')
text = "QUOTE GUESSR"
color = "magenta"
print(colored(f.renderText(text),color="magenta"))
print("Welcome to the quote guessing game\n")

game = Game()

again = 'kattenplaatjes'
while again:
    game.play_game()
    while again.lower() not in ('y','yes','no','n'):
        again = input("Want to play again (y/n)? ")
    if again.lower() in ('n', 'no'):
        break
    print("\nHere's another game! \n")
    again = 'kattenplaatjes'

print("\nThank you for playing!\n")