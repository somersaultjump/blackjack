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
    'Ace':1
    }

class Card():

    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

    def hidden(self):
        # add functionality to hide card properties, as if its facedown.
        pass

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

    def __init__(self,name):
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

class Pot():
    
    def __init__(self):
        self.amount = 0

    def __str__(self):
        return f"Pot contains {self.amount} dollars."

    def add(self,amount):
        self.amount += amount

    def deduct(self,amount):
        self.amount -= amount
