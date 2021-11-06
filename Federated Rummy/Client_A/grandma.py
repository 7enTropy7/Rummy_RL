import pydealer
import numpy as np
import torch as T

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

def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

class Grandma():
    def __init__(self, hand, agent):
        self.hand = hand
        self.score = 0
        self.done = False
        self.pure_sequence = 0
        self.first_sequence = 0
        self.second_sequence = 0
        self.matrix = self.get_matrix()
        self.model = agent
        self.binary_matrix = None

    def get_binary_matrix(self):
        self.binary_matrix = self.matrix.reshape(1,52)
        self.binary_matrix = np.where(self.binary_matrix > 0, 1, 0)

    def remember(self,state, action, probs, vals, reward, done):
        self.model.remember(state, action, probs, vals, reward, done)
        
    def learn(self):
        self.model.learn()

    def get_matrix(self):
        matrix_representation = np.zeros((4,13))

        for card in self.hand:
            matrix_representation[suits[card.suit]-1][values[card.value]-1] = values[card.value]

        return matrix_representation

    def drop_card_from_hand(self):
        """
        Uses NN to choose which card must be discarded
        returns card to be discarded.
        """
        self.get_binary_matrix()
        input_matrix = self.binary_matrix
        
        action, probs, value = self.model.choose_action(input_matrix)

        value_, suit_ = self.card_from_index(action)
        card_to_drop = pydealer.Card(inverse_values[value_+1], inverse_suits[suit_+1])

        return card_to_drop, action, probs, value
        
    def card_from_index(self,index):
        c = 0
        ans = 0
        for i in range(self.binary_matrix.shape[1]):
            if self.binary_matrix[0][i] == 1:
                if c == index:
                    ans = i
                    break
                c += 1

        value = ans % 13
        suit = ans // 13
        return value, suit

    def choose_action(self, prev_player_card, deck_top_card):
        flag_deck_top_card = False
        final_card_to_drop = None

        r1 = self.evaluate_score()

        # pick prev players card and put in matrix.
        self.matrix[suits[prev_player_card.suit]-1][values[prev_player_card.value]-1] = values[prev_player_card.value]
        
        # drop card
        drop_card, action, probs, crit_val = self.drop_card_from_hand()
        self.matrix[suits[drop_card.suit]-1][values[drop_card.value]-1] = 0
        
        r2 = self.evaluate_score()  
        if r2 <= r1:
            self.matrix[suits[drop_card.suit]-1][values[drop_card.value]-1] = values[drop_card.value]
            
            self.matrix[suits[prev_player_card.suit]-1][values[prev_player_card.value]-1] = 0
            
            new_card_from_deck = deck_top_card
            flag_deck_top_card = True

            self.matrix[suits[new_card_from_deck.suit]-1][values[new_card_from_deck.value]-1] = values[new_card_from_deck.value]
            
            final_card_to_drop, action, probs, crit_val  = self.drop_card_from_hand()
            
            self.matrix[suits[final_card_to_drop.suit]-1][values[final_card_to_drop.value]-1] = 0        
            

        else:
            final_card_to_drop = drop_card
            
        r3 = self.evaluate_score()
        
        if self.pure_sequence + self.first_sequence + self.second_sequence == 3 and self.pure_sequence > 0:
            self.done = True

        reward = r3
        # returns action
        return final_card_to_drop, action, probs, crit_val, reward, self.done, flag_deck_top_card 


    def count_elements(self):
        t = 0
        for row in self.matrix:
            t += np.count_nonzero(row)
        return t

    def evaluate_score(self):
        self.pure_sequence = 0
        self.first_sequence = 0
        self.second_sequence = 0

        isolated_cards = 0
        partial_sequences = 0
        for row in self.matrix:
            row_score = 0
            temp = consecutive(row)
            for t in temp:
                if t.size == 1:
                    isolated_cards += 1
                elif t.size == 2:
                    partial_sequences += 1
                elif t.size == 3 or t.size == 4 or t.size == 5:
                    row_score += 1
                elif t.size == 6 or t.size == 7:
                    row_score += 2
            self.pure_sequence += row_score
        
        if self.pure_sequence == 2:
            self.pure_sequence -= 1
            self.first_sequence += 1

        col_set = 0
        transpose_matrix = np.transpose(self.matrix)
        col_score = 0
        for row in transpose_matrix:
            col_score = np.count_nonzero(row)
            if col_score == 1:
                isolated_cards += 1
            elif col_score == 2:
                partial_sequences += 1
            elif col_score >= 3:
                col_set += 1

        if col_set > 0:
            if self.first_sequence == 0:
                self.first_sequence += 1
            else:
                self.second_sequence += 1

        reward_weight_factor = 1
        reward = ((self.pure_sequence + self.first_sequence + self.second_sequence) * reward_weight_factor) + (partial_sequences * 0.15) #+ (isolated_cards * (-0.5)) 
        
        return reward