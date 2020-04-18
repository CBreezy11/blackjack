# IMPORT STATEMENTS AND VARIABLE DECLARATIONS:
import random
from colorama import Fore


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


playing = True
players = []

# CLASS DEFINTIONS:


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__()  # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand():

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        result = ''
        for card in self.cards:
            result += card.__str__()+','
        return result


class Chips():

    def __init__(self, name):
        self.name = name
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# FUNCTION DEFINITIONS:

def take_bet(chips):

    while True:
        try:
            chips.bet = int(
                input(Fore.BLUE + f'{chips.name} How many chips would you like to bet?\
                     You have {chips.total} '))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed", chips.total)
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand, player):
    global playing

    while True:
        x = input(
            f"\n{player.name} would you like to Hit or Stand? Enter 1 for hit or 2 for stand ")

        if x[0].lower() == '1':
            hit(deck, hand)  # hit() function defined above

        elif x[0].lower() == '2':
            print("Player stands.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break


def show_dealer(dealer, all):
    if all:
        print("\nDealer's Hand:", *dealer.cards, sep='\n ')
        print("Dealer's Hand =", dealer.value)
    else:
        print("\nDealer's Hand:")
        print(" <card hidden>")
        print('', dealer.cards[1])


def show_some(player, chips):
    print(f"\n{chips.name}'s Hand:", *player.cards, sep='\n ')


def show_all(player, chips):
    print(f"\n{chips.name}'s Hand:", *player.cards, sep='\n ')
    print(f"{chips.name}s Hand =", player.value)


def player_busts(chips):
    print(Fore.RED + f"\n{chips.name} busts!")
    chips.lose_bet()


def player_wins(chips):
    print(f"\n{chips.name} wins!")
    chips.win_bet()


def dealer_busts(chips):
    print(f"\n{chips.name} Dealer busts! You Win!!")
    chips.win_bet()


def dealer_wins(chips):
    print(f"\n{chips.name}, The Dealer beat you")
    chips.lose_bet()


def push(player):
    print(f"\n{player.name} and Dealer tie! It's a push.")


# GAMEPLAY!

def setup():
    print('\n'*100)
    print(Fore.RED + 'Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')
    while True:
        try:
            number_of_players = int(
                input("How many people are playing? 1-5: "))
            break
        except:
            print("Please enter a valid # of 1-5")

    for player in range(number_of_players):
        player = Chips(input(f"Player {player + 1} what is your name? "))
        players.append(player)


def gameplay():
    global playing
    global players
    while True:

        # Create & shuffle the deck, deal two cards to each player
        deck = Deck()
        deck.shuffle()
        player_hands = []
        current_playing = players[:]
        busted = []

        print(Fore.WHITE + f"We have {len(players)} players in this hand")

        for player in players:
            take_bet(player)
            player_hand = Hand()
            player_hand.add_card(deck.deal())
            player_hand.add_card(deck.deal())
            player_hands.append(player_hand)

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Set up the Player's chips
        # remember the default value is 100

        # Prompt the Player for their bet:

        # Show the cards:
        show_dealer(dealer_hand, False)
        for player in range(len(players)):
            show_some(player_hands[player], players[player])

        # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        for player in range(len(players)):
            while playing:
                hit_or_stand(deck, player_hands[player], players[player])
                if playing:
                    show_some(player_hands[player], players[player])
                if player_hands[player].value > 21:
                    player_busts(players[player])
                    busted.append((players[player],
                                   player_hands[player]))
                    break
            playing = True

        for busted in busted:

            current_playing.remove(busted[0])
            player_hands.remove(busted[1])
        busted = []

     # If Player hasn't busted, play Dealer's hand

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

            # Show all cards
        show_dealer(dealer_hand, True)
        for player in range(len(current_playing)):
            if dealer_hand.value > 21:
                dealer_busts(current_playing[player])
            elif dealer_hand.value > player_hands[player].value:
                dealer_wins(current_playing[player])
            elif dealer_hand.value < player_hands[player].value:
                player_wins(current_playing[player])
            else:
                push(current_playing[player])

        # Inform Player of their chips total
        for player in range(len(players)):
            print(Fore.GREEN +
                  f"\n{players[player].name} winnings stand at: {players[player].total}")

        # Ask to play again
        for player in range(len(players)):
            if players[player].total < 1:
                print(Fore.RED +
                      f"\n{players[player].name}, you are out of money!! Thanks for playing")
                busted.append(players[player])
            else:
                new_game = input(
                    f"\n{players[player].name} would you like to play another hand? Enter 'y' or 'n' ")
                if new_game[0].lower().startswith('n'):
                    print(Fore.GREEN +
                          f'\nThanks for playing {players[player].name}\nYou are cashing out with {players[player].total}')
                    busted.append(players[player])

        for busted in busted:
            players.remove(busted)

        if len(players) > 0:
            print("\nOK next hand")
            continue
        else:
            break


if __name__ == "__main__":
    setup()
    gameplay()
