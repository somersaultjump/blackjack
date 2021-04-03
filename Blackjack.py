# Milestone Project 2 - Blackjack Game
# Here are the requirements:

# You need to create a simple text-based BlackJack game
# The game needs to have one player versus an automated dealer.
# The player can stand or hit.
# The player must be able to pick their betting amount.
# You need to keep track of the player's total money.
# You need to alert the player of wins, losses, or busts, etc...
# And most importantly:

# You must use OOP and classes in some portion of your game. 
# You can not just use functions in your game. 
# Use classes to help you define the Deck and the Player's hand. 

# Try including multiple players.
# Try adding in Double-Down and card splits!

import cards
import sys

def show_table():
    print('')
    print('***********************')
    print('')
    print('Dealer hand:')
    for dealer_card in dealer.all_cards:
        print(f"({dealer_card.value}) > {dealer_card}")
    print(f"[{dealer.hand_value()}]")
    print('')
    print('')
    print('Player hand:')
    for player_card in player.all_cards:
        print(f"({player_card.value}) > {player_card}")
    print(f"[{player.hand_value()}]")
    print('')
    print('***********************')
    print('')

def initial_deal():
    player.all_cards.append(dealer_deck.deal_card())
    dealer.all_cards.append(dealer_deck.deal_card())
    player.all_cards.append(dealer_deck.deal_card())
    dealer.all_cards.append(dealer_deck.deal_card())

def make_bet(bet):
    player.deduct(bet)
    pot.add(bet*2)
    print(f"{player.name} bets {bet} dollars.")
    print(f"Pot contains {pot.amount} dollars.")

def next_move():
    option = int(input('''
    What do you want to do next?
    1. Stand
    2. Hit
    3. Quit
    '''))
    
    # if stand
    if option == 1: 
    #     while dealer.total NOT in range 17-21
        while dealer.hand_value() not in range(16,22):
    #         dealer draws card
            dealer.all_cards.append(dealer_deck.deal_card())
    #         show the table
            show_table()
    #     compare dealer score to player score
    #         if dealer score > player score 
            if dealer.hand_value() > player.hand_value():
    #             dealer wins
                print("Dealer wins!")
    #         else
            elif dealer.hand_value() < player.hand_value():
    #           player wins
                print("Player wins!")
            else:
                print("Push!")
    # elif hit
    elif option == 2:
    #     player draws card
        player.all_cards.append(dealer_deck.deal_card())
    #     if player total > 21
        if player.hand_value() > 21:
    #         dealer wins
            print("Dealer wins!")
            return
        elif player.hand_value() == 21:
            print("Player wins!")
            # check dealer hand for push
            return
        else:
            show_table()
            next_move()

    elif option == 3:
        sys.exit(0)

def check_for_win(deal_num):
    if deal_num == 1:
        if dealer.hand_value() == 21 and player.hand_value() != 21:
            print("Dealer wins!")
        elif dealer.hand_value() > 21 and player.hand_value() < 21:
            print("Player wins!")
        elif player.hand_value() > 21:
            print("Dealer wins!")

def payout(amount):
    player.add(pot.amount)
    print(f"{player.name} wins {pot.amount}!")
    pot.deduct(pot.amount)

def reset_hands():
    player.all_cards.clear()
    dealer.all_cards.clear()

def play_round():
    reset_hands()
    # Take bet
    bet = int(input(f"Choose an amount to bet ({player.money} max): "))
    # remove bet from player and put it in pot.
    make_bet(bet)
    # deal cards
    initial_deal()
    show_table()
    next_move()


# create player and dealer
player_name = input("Who is playing? ")
player = cards.Player(player_name)
dealer = cards.Player("Dealer")
game_over = False
dealer_deck = cards.Deck()
pot = cards.Pot()
deal_num = 1
print(f"Welcome, {player.name}! Let's play Blackjack!")


# Start the game
while game_over == False:
    play_round()
