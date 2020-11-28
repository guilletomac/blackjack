import random

# Declare global variables

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = [
    'Two',
    'Three',
    'Four',
    'Five',
    'Six',
    'Seven',
    'Eight',
    'Nine',
    'Ten',
    'Jack',
    'Queen',
    'King',
    'Ace'
]

values = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 11
}

# project classes and function

playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    
    def __init__(self):
        self.deck = []  # Start the deck with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has: ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:

    def __init__(self):
        self.cards = []  # Start with an empty list as done in the Deck class
        self.value = 0  # Start with zero value
        self.aces = 0  # Attribute to keep track of aces

    def add_card(self, card):
        # Card passed in
        # from Deck.deal() --> single Card(suit, rank)
        self.cards.append(card)
        self.value += values[card.rank]

        # Track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        
        # If total value is greater than 21 and there's still an ace,
        # change value of ace from 11 down to 1
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self, total = 100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):

    while True:

        try:
            chips.bet = int(input('How many chips would you like to bet?: '))
        except:
            print('Please provide an integer')
        else:
            if chips.bet > chips.total:
                print('Sorry, you do not have enough chips ! You have: {}'.format(chips.total))
            else:
                break

def hit(deck, hand):

    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing  # To control an upcoming while loop

    while True:
        x = input('Hit or stand ? (enter h or s) : ')
        
        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("Player stands dealer's turn")    
            playing = False
        
        else:
            print("Sorry, I didn't understand that, please enter h or s")
            continue
        break

def show_some(player, dealer):
    print("DEALER'S HAND: ")
    print("One card hidden!")
    print(dealer.cards[1])
    print("\n")
    print("PLAYER'S HAND: ")
    for card in player.cards:
        print(card)

def show_all(player, dealer):
    print("DEALER'S HAND: ")
    for card in dealer.cards:
        print(card)
    print("\n")
    print("PLAYER'S HAND: ")
    for card in player.cards:
        print(card)

def player_busts(player, dealer, chips):
    print("BUST PLAYER!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("PLAYER WINS!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("PLAYER WINS! DEALER BUSTED!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("DEALER WINS!")
    chips.lose_bet()

def push(player, dealer):
    print("Dealer and player tie! PUSH!")

# Gameplay code and logic

while True:
    # Print opening statement
    print("WELCOME TO BLACKJACK!")

    # Create and shuffle the deck
    deck = Deck()
    deck.shuffle()

    # Create the player hand and deal two cards
    player_hand = Hand()    
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    # Create the player hand and deal two cards
    dealer_hand = Hand()    
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the player's chips
    player_chips = Chips()
    
    # Promt the player for their bet
    take_bet(player_chips)

    # Show cards (but keep one deal card hidden)
    show_some(player_hand, dealer_hand) 

    while playing: # Variable from hit_or_stand function

        # Prompt for Player Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    
    # If Player hasn't busted, play Dealer's Hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)        

    # Inform Player of their chis total
    print("\n Player total chips are at: {}".format(player_chips.total))

    # Ask to play again
    new_game = input("Would you like to play another hand? y/n:\n")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing!")
        break