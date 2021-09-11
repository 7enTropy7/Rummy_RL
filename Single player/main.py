import pydealer
from test import Agent
import numpy as np

inverse_values = {
    13:"King",
    12:"Queen",
    11:"Jack",
    10:"10",
    9:"9",
    8:"8",
    7:"7",
    6:"6",
    5:"5",
    4:"4",
    3:"3",
    2:"2",
    1:"Ace"
}

inverse_suits = {
    4:"Spades",
    3:"Hearts",
    2:"Clubs",
    1:"Diamonds"
}

deck = pydealer.Deck()

deck.shuffle()
cards = deck.deal(10)

hand = pydealer.Stack()
hand.add(cards)

agent = Agent(hand)

print(agent.matrix)

agent.get_binary_matrix()

index = int(input('index: '))

print(agent.card_from_index(index))

# card = agent.drop_card_from_hand()
# value, suit = np.argmax(card[0])
# card_to_drop = pydealer.Card(inverse_values[value+1], inverse_suits[suit+1])
# print(card_to_drop)

