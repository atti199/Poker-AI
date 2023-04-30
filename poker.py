import random
import itertools
from collections import Counter

RANK_ORDER = '23456789TJQKA'
RANK_VALUES = {rank: value for value, rank in enumerate(RANK_ORDER, start=2)}
HAND_RANKS = ['High Card', 'Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush']

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in "23456789TJQKA" for suit in "SHDC"]
        random.shuffle(self.cards)


    def deal(self):
        return self.cards.pop()

class Hand:
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        return " ".join(str(card) for card in self.cards)
    

class Player:
    def __init__(self, cash, hand=None):
        self.cash = cash
        self.hand = hand if hand else Hand([])

    def __str__(self):
        return f"Hand: {self.hand}, Cash: {self.cash}"
    


class PokerTable:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = [Player(500) for _ in range(num_players)]
        self.community_cards = []
        self.deck = Deck()
        self.current_bet = 0
        self.pot = 0
        self.small_blind = 10
        self.big_blind = 20

    def player_action(self, player_index):
        player = self.players[player_index]
        valid_input = False
        while not valid_input:
            action = input(f"Player {player_index + 1} ({player.cash} cash), choose your action (bet, call, raise, fold): ").lower()
            if action == "bet":
                bet_amount = int(input("Enter the bet amount: "))
                if bet_amount <= player.cash:
                    valid_input = True
                    player.cash -= bet_amount
                    self.pot += bet_amount
                    self.current_bet = bet_amount
                elif action == "call":
                    call_amount = self.current_bet - player.cash
                    if call_amount > 0:
                        valid_input = True
                        player.cash -= call_amount
                        self.pot += call_amount
                elif action == "raise":
                    raise_amount = int(input("Enter the raise amount: "))
                    if raise_amount > self.current_bet and raise_amount <= player.cash:
                        valid_input = True
                        player.cash -= raise_amount
                        self.pot += raise_amount
                        self.current_bet = raise_amount
                elif action == "fold":
                    valid_input = True
                    return "fold"
            else:
                print("Invalid input, please try again.")
        return action

    
    def deal_hole_cards(self):
        for player in self.players:
            player.hand = Hand([self.deck.deal(), self.deck.deal()])

    def deal_community_cards(self, count):
        for _ in range(count):
            self.community_cards.append(self.deck.deal())

    def reset_betting(self):
        self.current_bet = 0
        self.pot = 0

    def collect_bets(self):
        for i, player in enumerate(self.players):
            if i == 0:
                action = self.player_action(i)
                if action == "fold":
                    self.players[i] = None
            else:
                # Change this for AI betting strategy
                bet = random.randint(self.big_blind, player.cash)
                player.cash -= bet
                self.pot += bet
                self.current_bet = max(self.current_bet, bet)

        # Remove folded players
        self.players = [player for player in self.players if player is not None]


    def distribute_pot(self, winners):
        split_pot = self.pot // len(winners)
        for winner in winners:
            self.players[winner].cash += split_pot

    def play(self):
        game_over = False
        while not game_over:
            print("\nNew round started!")
            self.reset_betting()
            self.collect_bets()

            print("Dealing hole cards...")
            self.deal_hole_cards()
            for i, player in enumerate(self.players):
                print(f"Player {i + 1}: {player}")

            print("\nDealing flop...")
            self.deal_community_cards(3)
            print("Community cards:", " ".join(str(card) for card in self.community_cards))

            print("\nDealing turn...")
            self.deal_community_cards(1)
            print("Community cards:", " ".join(str(card) for card in self.community_cards))

            print("\nDealing river...")
            self.deal_community_cards(1)
            print("Community cards:", " ".join(str(card) for card in self.community_cards))

            winners, winning_hand = winning_player(self)
            winning_hand_name = HAND_RANKS[winning_hand[0]]

            if len(winners) == 1:
                print(f"\nPlayer {winners[0] + 1} wins with a {winning_hand_name}!")
            else:
                print(f"\nIt's a tie between players {', '.join(str(winner + 1) for winner in winners)} with a {winning_hand_name}!")

            self.distribute_pot(winners)
            for winner in winners:
                player_hand = self.players[winner].hand
                winning_hand_cards = best_hand(self.players[winner], self.community_cards)
                print(f"Player {winner + 1}'s hand: {player_hand}")
                print(f"Player {winner + 1}'s winning hand: {' '.join(str(card) for card in winning_hand_cards)}")

            self.community_cards.clear()
            self.deck = Deck()

            eliminated_players = [i for i, player in enumerate(self.players) if player.cash == 0]
            if eliminated_players:
                for index in sorted(eliminated_players, reverse=True):
                    print(f"\nPlayer {index + 1} has been eliminated.")
                    del self.players[index]
                    self.num_players -= 1

            if self.num_players == 1:
                print(f"\nCongratulations! Player 1 is the winner.")
                game_over = True



def best_hand(player, community_cards):
    all_cards = player.hand.cards + community_cards  # Fix: Access the cards attribute of the Hand object
    all_combinations = itertools.combinations(all_cards, 5)
    best_hand = None
    best_rank = None

    for combination in all_combinations:
        current_rank = hand_rank(combination)
        if not best_rank or current_rank < best_rank:
            best_rank = current_rank
            best_hand = combination

    return best_hand


def winning_player(poker_table):
    best_rank = None
    winners = []

    for i, player in enumerate(poker_table.players):
        player_best_hand = best_hand(player, poker_table.community_cards)
        player_rank = hand_rank(player_best_hand)

        if not best_rank or player_rank < best_rank:
            best_rank = player_rank
            winners = [i]
        elif player_rank == best_rank:
            winners.append(i)

    return winners, best_rank


if __name__ == "__main__":
    num_players = int(input("Enter the number of players: "))
    poker_table = PokerTable(num_players)
    poker_table.play()
