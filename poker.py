import random
import itertools


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


class PokerTable:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = [Hand([]) for _ in range(num_players)]
        self.community_cards = []
        self.deck = Deck()

    def deal_hole_cards(self):
        for player in self.players:
            player.cards = [self.deck.deal(), self.deck.deal()]

    def deal_community_cards(self, count):
        for _ in range(count):
            self.community_cards.append(self.deck.deal())

    def play(self):
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




from collections import Counter

RANK_ORDER = '23456789TJQKA'
RANK_VALUES = {rank: value for value, rank in enumerate(RANK_ORDER, start=2)}
HAND_RANKS = ['High Card', 'Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush']


def hand_rank(hand):
    ranks = [RANK_VALUES[card.rank] for card in hand]
    suits = [card.suit for card in hand]
    rank_counts = Counter(ranks)
    most_common_ranks = rank_counts.most_common()

    is_flush = len(set(suits)) == 1
    is_straight = len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4
    is_ace_low_straight = set(ranks) == {14, 2, 3, 4, 5}

    if is_flush and is_straight:
        return (8, max(ranks)) if not is_ace_low_straight else (8, 5)
    if is_flush:
        return 5, sorted(ranks, reverse=True)
    if is_straight or is_ace_low_straight:
        return 4, max(ranks) if not is_ace_low_straight else 5

    highest_rank, highest_count = most_common_ranks[0]
    if highest_count == 4:
        return 7, highest_rank, most_common_ranks[1][0]
    if highest_count == 3 and most_common_ranks[1][1] == 2:
        return 6, highest_rank, most_common_ranks[1][0]

    if highest_count == 3:
        return 3, highest_rank, sorted([rank for rank, count in most_common_ranks if count != highest_count], reverse=True)
    if highest_count == 2 and most_common_ranks[1][1] == 2:
        return 2, most_common_ranks[0][0], most_common_ranks[1][0], most_common_ranks[2][0]
    if highest_count == 2:
        return 1, highest_rank, sorted([rank for rank, count in most_common_ranks if count != highest_count], reverse=True)

    return 0, sorted(ranks, reverse=True)


def best_hand(player_hand, community_cards):
    all_cards = player_hand.cards + community_cards
    all_combinations = itertools.combinations(all_cards, 5)
    return max(all_combinations, key=hand_rank)


def winning_player(poker_table):
    best_hands = [best_hand(player, poker_table.community_cards) for player in poker_table.players]
    ranked_hands = [hand_rank(hand) for hand in best_hands]
    winning_hand = max(ranked_hands)
    winners = [i for i, hand in enumerate(ranked_hands) if hand == winning_hand]
    return winners, winning_hand


def play_game():
    num_players = int(input("Enter the number of players: "))
    poker_table = PokerTable(num_players)
    poker_table.play()

    winners, winning_hand = winning_player(poker_table)
    winning_hand_name = HAND_RANKS[winning_hand[0]]

    if len(winners) == 1:
        print(f"\nPlayer {winners[0] + 1} wins with a {winning_hand_name}!")
    else:
        print(f"\nIt's a tie between players {', '.join(str(winner + 1) for winner in winners)} with a {winning_hand_name}!")

    for winner in winners:
        player_hand = poker_table.players[winner].cards
        winning_hand_cards = best_hand(poker_table.players[winner], poker_table.community_cards)
        print(f"Player {winner + 1}'s hand: {poker_table.players[winner]}")
        print(f"Player {winner + 1}'s winning hand: {' '.join(str(card) for card in winning_hand_cards)}")


if __name__ == "__main__":
    play_game()