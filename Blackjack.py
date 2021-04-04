import cards
import sys
import time
import os

# initial setup; make the player, dealer, deck, and pot
player = cards.Player()
dealer = cards.Player("Dealer")
dealer_deck = cards.Deck()
pot = cards.Pot()

def refresh():
    os.system('clear')
    show_table()

def show_table():
    print('')
    print('***********************')
    print('')
    print(f'Pot: {pot.amount}')
    print('')
    print("Dealer's hand:")
    for dealer_card in dealer.all_cards:
        if dealer_card.hidden == True:
            print(f"({dealer_card.hvalue}) > {dealer_card}")
        else:
            print(f"({dealer_card.value}) > {dealer_card}")
    if dealer.all_cards[-1].hidden == True:
        print(f"[{dealer.hand_value() - dealer.all_cards[-1].value}]")
    else:
        print(f"[{dealer.hand_value()}]")
    print('')
    print('')
    print(f"{player.name}'s hand:")
    for player_card in player.all_cards:
        print(f"({player_card.value}) > {player_card}")
    print(f"[{player.hand_value()}]")
    print('')
    print('***********************')
    print('')

def initial_deal():
    del player.all_cards[:]
    del dealer.all_cards[:]
    player.all_cards.append(dealer_deck.deal_card())
    dealer.all_cards.append(dealer_deck.deal_card())
    player.all_cards.append(dealer_deck.deal_card())
    dealer.all_cards.append(dealer_deck.deal_card())
    dealer.all_cards[-1].hide()

def next_move():
    option = int(input('''
    What do you want to do next?
    1. Stand
    2. Hit
    3. Quit
    '''))

    if option == 1: # stand
        dealer.all_cards[-1].show()
        while dealer.hand_value() < 17:
            dealer.all_cards.append(dealer_deck.deal_card())
            refresh()
            time.sleep(1)
            continue
        
        if dealer.hand_value() >= 17:
            who_wins()

    elif option == 2: # hit
        player.all_cards.append(dealer_deck.deal_card())
        refresh()
        if player.hand_value() > 21:
            print("BUST!!")
            pot.empty()
            return
        next_move()
        
    elif option == 3: # quit
        sys.exit(0)

def who_wins():
    if dealer.hand_value() > 21:
        refresh()
        print(f"Player wins {pot.amount}!")
        player.money += pot.amount
        pot.empty()
        print(f"Player money: {player.money}")
        return

    if dealer.hand_value() > player.hand_value():
        refresh()
        print("Dealer wins!")
        pot.empty()
        return

    elif dealer.hand_value() < player.hand_value():
        refresh()
        print(f"Player wins {pot.amount}!")
        player.money += pot.amount
        pot.empty()
        print(f"Player money: {player.money}")
        return

    elif dealer.hand_value() == player.hand_value():
        refresh()
        print("Push")
        player.money += pot.amount/2
        pot.empty()
        return

def make_bet():
    bet = int(input(f'''
    How much do you want to bet?
    ({player.money} available)
    '''))
    if bet > player.money:
        print("You can't afford that. Try again.")
        make_bet()
    player.deduct(bet)
    pot.add(bet*2)

def play_blackjack():
    make_bet()
    initial_deal()
    refresh()
    next_move()
    time.sleep(4)
    os.system('clear')

while player.money > 0:
    play_blackjack()

print("You ran out of money.")
time.sleep(5)
