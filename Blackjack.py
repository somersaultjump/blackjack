import sys
import time
import os
import cards

PLAYER = cards.Player()
DEALER = cards.Player("Dealer")
dealer_deck = cards.Deck()
pot = cards.Pot()

def refresh():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    ace_check()
    show_table()

def show_table():
    print('')
    print('***********************')
    print('')
    print(f'Deck: {len(dealer_deck.all_cards)}')
    print(f'Pot: {pot.amount}')
    print('')
    print("Dealer's hand:")
    for dealer_card in DEALER.all_cards:
        if dealer_card.hidden is True:
            print(f"({dealer_card.hvalue}) > {dealer_card}")
        else:
            print(f"({dealer_card.value}) > {dealer_card}")
    if DEALER.all_cards[-1].hidden is True:
        print(f"[{DEALER.hand_value() - DEALER.all_cards[-1].value}]")
    else:
        print(f"[{DEALER.hand_value()}]")
    print('')
    print('')
    print(f"{PLAYER.name}'s hand:")
    for player_card in PLAYER.all_cards:
        print(f"({player_card.value}) > {player_card}")
    print(f"[{PLAYER.hand_value()}]")
    print('')
    print('***********************')
    print('')

def initial_deal():
    del PLAYER.all_cards[:]
    del DEALER.all_cards[:]
    PLAYER.all_cards.append(dealer_deck.deal_card())
    DEALER.all_cards.append(dealer_deck.deal_card())
    PLAYER.all_cards.append(dealer_deck.deal_card())
    DEALER.all_cards.append(dealer_deck.deal_card())
    DEALER.all_cards[-1].hide()

def next_move(): # TODO: validate choice input type
    option = int(input('''
    What do you want to do next?
    1. Stand
    2. Hit
    3. Quit
    '''))

    if option == 1: # stand
        DEALER.all_cards[-1].show()
        while DEALER.hand_value() < 17:
            DEALER.all_cards.append(dealer_deck.deal_card())
            refresh()
            time.sleep(1)
            continue
        if DEALER.hand_value() >= 17:
            who_wins()
    elif option == 2: # hit
        PLAYER.all_cards.append(dealer_deck.deal_card())
        refresh()
        if PLAYER.hand_value() > 21:
            print("BUST!!")
            pot.empty()
            return
        next_move()
    elif option == 3: # quit
        sys.exit(0)

def who_wins():
    if DEALER.hand_value() > 21:
        refresh()
        print(f"Player wins {pot.amount}!")
        PLAYER.money += pot.amount
        pot.empty()
        print(f"Player money: {PLAYER.money}")
        return

    if DEALER.hand_value() > PLAYER.hand_value():
        refresh()
        print("Dealer wins!")
        pot.empty()
        return

    if DEALER.hand_value() < PLAYER.hand_value():
        refresh()
        print(f"Player wins {pot.amount}!")
        PLAYER.money += pot.amount
        pot.empty()
        print(f"Player money: {PLAYER.money}")
        return

    if DEALER.hand_value() == PLAYER.hand_value():
        refresh()
        print("Push")
        PLAYER.money += pot.amount//2
        pot.empty()
        return

def make_bet(): # TODO: validate bet input type
    bet = int(input(f'''
    How much do you want to bet?
    ({PLAYER.money} available)
    '''))
    if bet > PLAYER.money:
        print("You can't afford that. Try again.")
        make_bet()
    PLAYER.deduct(bet)
    pot.add(bet*2)

def ace_check():
    global PLAYER
    global DEALER
    for person in [PLAYER,DEALER]:
        for card in person.all_cards:
            if card.rank == 'Ace':
                # print(f"{person.name} has an Ace...")
                if PLAYER.hand_value() == 21:
                    who_wins()
                if person.hand_value() > 21:
                    # print(f"AND {person.name} has more than 21: {person.hand_value()}")
                    # print(f'Old Ace: {card.value}')
                    card.value = 1
                    # print(f'New Ace: {card.value}')
                    return
                # print(f"BUT {person.name} has less than 21: {person.hand_value()}")
                # print(f'Ace: {card.value}')

def play_blackjack():
    make_bet()
    initial_deal()
    refresh()
    if PLAYER.hand_value() == 21:
        if len(PLAYER.all_cards) == 2:
            print(f"BLACKJACK!! Player wins {pot.amount*3//2}")
            PLAYER.money += pot.amount*3//2
            pot.empty()
            print(f"Player money: {PLAYER.money}")
            return
    next_move()
    time.sleep(4)
    os.system('clear')

while PLAYER.money > 0:
    if len(dealer_deck.all_cards) <= 13:
        dealer_deck = cards.Deck()
        print("...shuffling the deck...")
        time.sleep(3)
    play_blackjack()

print("You ran out of money.")
time.sleep(5)
