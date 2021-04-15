import sys
import time
import os
import cards

PLAYER = cards.Player()
DEALER = cards.Player("Dealer")
dealer_deck = cards.Deck()
pot = cards.Pot()

def clear_screen():
    """Clear the screen, check for aces on the table, show the table."""
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def refresh():
    """Combine functions to act as a refresh of the board/gamestate."""
    clear_screen()
    ace_check()
    show_table()

def show_table():
    """Display the active game table."""
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
    """Clear player hands, deal new hand, hide second dealer card."""
    del PLAYER.all_cards[:]
    del DEALER.all_cards[:]
    PLAYER.all_cards.append(dealer_deck.deal_card())
    DEALER.all_cards.append(dealer_deck.deal_card())
    PLAYER.all_cards.append(dealer_deck.deal_card())
    DEALER.all_cards.append(dealer_deck.deal_card())
    DEALER.all_cards[-1].hide()

def get_input():
    # make sure the var is empty
    this_input = None

    # ask user for input until they get it right.
    while not isinstance(this_input,int):
        try:
            this_input = int(input("Enter a number: "))
        except:
            print(f"Invalid choice. Try again.")
    
    return this_input

def next_move(): # TODO: limit choices to 1,2, or 3
    """Get and execute next move from player."""
    print('''
    What do you want to do next?
    1. Stand
    2. Hit
    3. Quit
    ''')

    option = get_input()

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
    else:
        refresh()
        print(f'Do you see {option} in that list?  Try again.')
        next_move()

def who_wins():
    """Evaluate and act on win conditions."""
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

def make_bet():
    """Ask player to make a bet, deduct from player, add to pot."""
    print(f'''
    How much do you want to bet?
    ({PLAYER.money} available)
    ''')
    bet = get_input()
    if bet > PLAYER.money:
        print("You can't afford that. Try again.")
        make_bet()
    PLAYER.deduct(bet)
    pot.add(bet*2)

def ace_check():
    """Logic to check for aces and adjust value."""
    # TODO: see if the ace value change can be a method
    # on the class, so we don't have to use global vars here
    # W0603: Using the global statement (global-statement)
    global PLAYER
    global DEALER
    for person in [PLAYER,DEALER]:
        for card in person.all_cards:
            if card.rank == 'Ace':
                if PLAYER.hand_value() == 21:
                    who_wins()
                if person.hand_value() > 21:
                    card.value = 1
                    return

def play_blackjack():
    """Main function."""
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
