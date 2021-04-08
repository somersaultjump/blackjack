import sys
import time
import os
import cards

player = cards.Player()
dealer = cards.Player("Dealer")
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
    for dealer_card in dealer.all_cards:
        if dealer_card.hidden is True:
            print(f"({dealer_card.hvalue}) > {dealer_card}")
        else:
            print(f"({dealer_card.value}) > {dealer_card}")
    if dealer.all_cards[-1].hidden is True:
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

def next_move(): # TODO: validate choice input type
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

    if dealer.hand_value() < player.hand_value():
        refresh()
        print(f"Player wins {pot.amount}!")
        player.money += pot.amount
        pot.empty()
        print(f"Player money: {player.money}")
        return

    if dealer.hand_value() == player.hand_value():
        refresh()
        print("Push")
        player.money += pot.amount//2
        pot.empty()
        return

def make_bet(): # TODO: validate bet input type
    bet = int(input(f'''
    How much do you want to bet?
    ({player.money} available)
    '''))
    if bet > player.money:
        print("You can't afford that. Try again.")
        make_bet()
    player.deduct(bet)
    pot.add(bet*2)

def ace_check():
    global player
    global dealer
    for person in [player,dealer]:
        for card in person.all_cards:
            if card.rank == 'Ace':
                # print(f"{person.name} has an Ace...")
                if player.hand_value() == 21:
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
    if player.hand_value() == 21:
        if len(player.all_cards) == 2:
            print(f"BLACKJACK!! Player wins {pot.amount*3//2}")
            player.money += pot.amount*3//2
            pot.empty()
            print(f"Player money: {player.money}")
            return
    next_move()
    time.sleep(4)
    os.system('clear')

while player.money > 0:
    if len(dealer_deck.all_cards) <= 13:
        dealer_deck = cards.Deck()
        print("...shuffling the deck...")
        time.sleep(3)
    play_blackjack()

print("You ran out of money.")
time.sleep(5)
