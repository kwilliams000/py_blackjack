# Playing blackjack

import random

class Deck():
    def __init__(self) -> None:
        self.cards: list = []
        self.suits: list[str] = ['Spades', 'Hearts','Clubs','Diamonds']
        self.ranks: list[dict] = self.create_ranks()
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(suit,rank))

    def shuffle(self)->None:
        if len(self.cards) > 1: random.shuffle(self.cards)

    def deal(self,num: int = 1)-> list[list]:
        cards_dealt: list[list] = []
        for x in range(num):
            if len(self.cards) > 0:
                cards_dealt.append(self.cards.pop())
        return cards_dealt

    def create_ranks(self)->list[dict]:
        ranks_keys: list[str] = ['A','K','Q','J']
        ranks_nums: list[int] = list(range(10,1,-1))
        ranks_keys.extend(map(str,ranks_nums))

        ranks_value: list[dict] = []
        for rank in ranks_keys:
            try:
                int(rank)
            except ValueError:
                if rank == 'A':
                    ranks_value.append({'rank':rank,'value':11})
                else:
                    ranks_value.append({'rank':rank,'value':10})
            else:
                ranks_value.append({'rank':rank,'value':int(rank)})

        #ranks_dict = ({k:v for (k,v) in zip(ranks_keys,ranks_value)})
        return ranks_value
    
    def __str__(self) -> str:
        return f'{self.cards.index}'
    
class Card:
    def __init__(self, suit, rank) -> None:
        self.suit = suit
        self.rank = rank
    
    def __str__(self) -> str:
        return f'{self.rank["rank"]} of {self.suit}'
    
class Hand:
    def __init__(self, dealer:bool = False) -> None:
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)
    
    def calculate_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank['value'])
            self.value += card_value
            if card.rank['rank'] =='A':
                has_ace = True
        
        if has_ace and self.value > 21:
            self.value -= 10
    
    def get_value(self):
        self.calculate_value()
        return self.value
    
    def is_blackjack(self):
        return self.get_value() == 21
    
    def display(self, show_all_dealer_cards: bool = False):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand: ''')
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards \
                and not self.is_blackjack():
                print('Hidden')
            else:
                print(card)
        
        if not self.dealer:
            print('Value: ',self.get_value())
        print()

class Game:
    def play(self):
        game_number: int = 0
        games_to_play: int = 0

        while games_to_play <=0:
            try:
                games_to_play = int(input('How many games do you want to play? '))
            except ValueError:
                print('You must enter a number.')
        
        while game_number < games_to_play:
            game_number += 1

            deck: Deck = Deck()
            deck.shuffle()

            player_hand: Hand = Hand()
            dealer_hand: Hand = Hand(dealer=True)

            for i in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print()
            print('*' * 30)
            print(f'Game {game_number} of {games_to_play}')
            print('*' * 30)
            player_hand.display()
            dealer_hand.display()

            choice = ''
            while player_hand.get_value() < 21 and choice not in ['s','stand']:
                choice = input('Please choose "Hit" or "Stand": ').lower()
                print()
                while choice not in ['h','s','hit','stand']:
                    input('Please enter "Hit" or "Stand" (or H/S)').lower()
                    print()
                if choice in ['hit','h']:
                    player_hand.add_card(deck.deal())
                    player_hand.display()
            
            if self.check_winner(player_hand,dealer_hand):
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal())
                dealer_hand_value = dealer_hand.get_value()
            
            dealer_hand.display(show_all_dealer_cards=True)

            if self.check_winner(player_hand,dealer_hand):
                continue

            print('Final Results')
            print(f'Your hand: {player_hand_value}')
            print(f'Dealer\'s hand: {dealer_hand_value}')

            self.check_winner(player_hand,dealer_hand,True)
        print('\nThanks for playing!')

    def check_winner(self, player_hand, dealer_hand, game_over = False) -> bool:
        if not game_over:
            if player_hand.get_value() > 21:
                print('You busted. Dealer wins!')
                return True
            elif dealer_hand.get_value() > 21:
                print(' Dealer busted. You win!')
            elif player_hand.is_blackjack() and dealer_hand.is_blackjack():
                print('Both players have blackjack. Tie!')
                return True
            elif player_hand.is_blackjack():
                print('You have blackjack. You win!')
                return True
            elif dealer_hand.is_blackjack():
                print('Dealer has blackjack. Dealer wins!')
                return True
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print('You win!')
            elif dealer_hand.get_value() == player_hand.get_value():
                print('Tie!')
            else:
                print('Dealer wins!')
            return True
        return False

def main()->None:
    deck = Deck()
    #for x in deck.cards:
    #    print(x)
    #[print(x) for x in deck.cards]
    #deck.shuffle()
    #hand = Hand()
    #hand.add_card(deck.deal(2))
    #print(hand.cards[0],hand.cards[1])

    g = Game()
    g.play()

if __name__ == '__main__':
    main()