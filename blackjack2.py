# starting over clean

import cards
import sys

# initial setup
# make the player, dealer, deck, and pot
player_name = input("Who is playing? ")
player = cards.Player(player_name)
dealer = cards.Player("Dealer")
dealer_deck = cards.Deck()
pot = cards.Pot()
# set game state variables
game_over = False
deal_num = 1

print(f"Welcome, {player.name}! Let's play Blackjack!")





sys.exit(0)
