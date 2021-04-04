import cards
import sys
import time

# initial setup; make the player, dealer, deck, and pot
player = cards.Player()
dealer = cards.Player("Dealer")
dealer_deck = cards.Deck()
pot = cards.Pot()

def show_table():
    print('')
    print('***********************')
    print('')
    print("Dealer's hand:")
    for dealer_card in dealer.all_cards:
        print(f"({dealer_card.value}) > {dealer_card}")
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
    player.all_cards.append(dealer_deck.deal_card())
    dealer.all_cards.append(dealer_deck.deal_card())
    player.all_cards.append(dealer_deck.deal_card())
    dealer.all_cards.append(dealer_deck.deal_card())

def next_move():
    option = int(input('''
    What do you want to do next?
    1. Stand
    2. Hit
    3. Quit
    '''))

    if option == 1: # stand
        while dealer.hand_value() < 17:
            dealer.all_cards.append(dealer_deck.deal_card())
            show_table()
            time.sleep(1)
            continue
        
        if dealer.hand_value() >= 17:
            who_wins()

    elif option == 2: # hit
        player.all_cards.append(dealer_deck.deal_card())
        show_table()
        if player.hand_value() > 21:
            print("BUST!!")
            return
        next_move()
        
    elif option == 3: # quit
        sys.exit(0)

def who_wins():
    if dealer.hand_value() > player.hand_value():
        show_table()
        print("Dealer wins!")
        return

    elif dealer.hand_value() < player.hand_value():
        show_table()
        print(f"{player.name} wins!")
        return

    elif dealer.hand_value() == player.hand_value():
        show_table()
        print("Push")
        return

initial_deal()
show_table()
next_move()
