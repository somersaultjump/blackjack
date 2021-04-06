import random

suits = (
    'Hearts', 'Diamonds', 'Spades', 'Clubs'
    )

ranks = (
    'Two','Three','Four','Five','Six','Seven',
    'Eight','Nine','Ten','Jack','Queen','King',
    'Ace'
    )

values = { # TODO: figure out how to make ace 1 or 11
    'Two':2,'Three':3,'Four':4,'Five':5,
    'Six':6,'Seven':7,'Eight':8,'Nine':9,
    'Ten':10,'Jack':10,'Queen':10,'King':10,
    'Ace':11
    }

class Card():

    def __init__(self,rank,suit,hidden=False):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]
        self.hidden = hidden
        self.hrank = "????"
        self.hsuit = "??????"
        self.hvalue = 0

    def __str__(self):
        if self.hidden == True:
            return self.hrank + " of " + self.hsuit
        else:
            return self.rank + " of " + self.suit

    # add functionality to hide card properties, as if its facedown.
    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

class Deck():

    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(rank,suit))

        random.shuffle(self.all_cards)

    def deal_card(self):
        return self.all_cards.pop(0)

class Player():

    def __init__(self,name="Player"):
        self.name = name
        self.all_cards = []
        self.money = 100
    
    def add(self,amount):
        self.money += amount

    def deduct(self,amount):
        self.money -= amount

    def hand_value(self):
        total = 0
        for card in self.all_cards:
            total += card.value
        return total

    def clear_hand(self):
        self.all_cards[:]

class Pot():
    
    def __init__(self):
        self.amount = 0

    def __str__(self):
        return f"Pot contains {self.amount} dollars."

    def add(self,amount):
        self.amount += amount

    def deduct(self,amount):
        self.amount -= amount

    def empty(self):
        self.amount = 0