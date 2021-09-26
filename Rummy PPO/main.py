import pydealer
from grandma import Grandma
import numpy as np
from model import Agent

values = {
    "King": 13,
    "Queen": 12,
    "Jack": 11,
    "10": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "Ace": 1
}

suits = {
    "Spades": 4,
    "Hearts": 3,
    "Clubs": 2,
    "Diamonds": 1
}

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

agent = Agent(11,(52,),n_epochs=5)

def reset():
    players = []
    deck = pydealer.Deck()
    deck.shuffle()
    current_player = 0
    table_card = None
    for i in range(3):
        cards = deck.deal(10)
        hand = pydealer.Stack()
        hand.add(cards)
        players.append(Grandma(hand,agent))
    
    table_card = deck.deal(1)[0]
    return players, table_card, deck
    
n_games = 20
rounds = 0

global_done = False

for n in range(n_games):
    done = False
    players, table_card, deck = reset()
    
    p_score = [0,0,0] 
    rounds = 0
    print('---------------------- New Game -----------------------------')
    while not done:
        for i in range(3):
            
            if rounds == 0:
                print(players[i].matrix,'\n')
                        
            table_card,action, probs, crit_val, reward, done = players[i].choose_action(table_card, deck)
            p_score[i] = reward
            p_score[i] = round(p_score[i],2)
            if done:
                print('Winner is player: {} \n Winner\'s matrix: \n {}'.format(i+1,players[i].matrix))
                global_done = True
                break
            
            players[i].remember(players[i].binary_matrix, action, probs, crit_val, reward, done)
            
            players[i].learn()
            
            if deck.size == 0:
                done = True
                break
            
        rounds += 1
        
        if rounds > 15:
            done = True
                  
        print('Round:{}  Scores:{}  Done:{}'.format(rounds,p_score,done))
    
    print('Game number:{}'.format(n))
    
    if global_done:
        break
    