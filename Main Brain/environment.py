from model import Brain
import pydealer
import numpy as np

class Env:
    def __init__(self):
        self.players = []
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        self.current_player = 0
        self.table_card = None

    def reset(self):
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        self.current_player = 0

        for i in range(3):
            cards = deck.deal(10)
            hand = pydealer.Stack()
            hand.add(cards)
            self.players.append(Agent(hand))
        
        self.table_card = self.deck.deal(1)
    
    
    def step(self,action):
        self.players[self.current_player].play_turn(self.table_card,self.deck)



        self.current_player = (self.current_player + 1) % len(self.players)