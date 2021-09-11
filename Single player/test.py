from model import Brain
import pydealer
import numpy as np


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

class Agent():
    def __init__(self, hand):
        self.hand = hand
        self.score = 0
        self.done = False
        self.pure_sequence = 0
        self.first_sequence = 0
        self.second_sequence = 0
        self.matrix = self.get_matrix()
        self.model = Brain().model
        self.binary_matrix = None

    def get_binary_matrix(self):
        self.binary_matrix = self.matrix.reshape(1,52)
        self.binary_matrix = np.where(self.binary_matrix > 0, 1, 0)


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
        input_matrix = np.expand_dims(input_matrix,axis=0)
        
        output_ = self.model.predict(input_matrix)
        index = np.argmax(output_)

        value, suit = self.card_from_index(index)
        card_to_drop = pydealer.Card(inverse_values[value+1], inverse_suits[suit+1])
        return card_to_drop
        
    def card_from_index(self,index):
        c = 0
        ans = 0
        print(self.binary_matrix.shape[1])
        for i in range(self.binary_matrix.shape[1]):
            if self.binary_matrix[0][i] == 1:
                if c == index:
                    ans = i
                    break
                c += 1

        value = ans % 13
        suit = ans // 13
        return value, suit

    def draw_deck_top(self,deck):
        return deck.deal(1)[0]

    def play_turn(self,prev_player_card,deck):
        '''
        r1 = evaluate score of 10 cards.
        pick prev pplayer card.
        eliminate one card using drop.
        r2 = evaluate score again
        if r2<=r1:
            put back the eliminated card
            return the prev players card and pick new one from deck.
        elif r2>r1:
            eliminate a card using drop.
    
        r3 = evaluate score again
        use r3 for training. maximize r3.
        '''

        final_card_to_drop = None

        r1 = self.evaluate_score()
        print('pure sequence: ', self.pure_sequence)
        print('first sequence: ', self.first_sequence)
        print('second sequence: ', self.second_sequence)

        # pick prev players card and put in matrix.
        self.matrix[suits[prev_player_card.suit]-1][values[prev_player_card.value]-1] = values[prev_player_card.value]
        
        # drop card
        drop_card = self.drop_card_from_hand()
        self.matrix[suits[drop_card.suit]-1][values[drop_card.value]-1] = 0
        
        r2 = self.evaluate_score()  
        if r2 <= r1:
            self.matrix[suits[drop_card.suit]-1][values[drop_card.value]-1] = values[drop_card.value]
            
            self.matrix[suits[prev_player_card.suit]-1][values[prev_player_card.value]-1] = 0
            
            new_card_from_deck = self.draw_deck_top(deck)
            self.matrix[suits[new_card_from_deck.suit]-1][values[new_card_from_deck.value]-1] = values[new_card_from_deck.value]
            
            final_card_to_drop = self.drop_card_from_hand()
            
            self.matrix[suits[final_card_to_drop.suit]-1][values[final_card_to_drop.value]-1] = 0        
            

        else:
            final_card_to_drop = drop_card
            
        
        r3 = self.evaluate_score()
        print('pure sequence: ', self.pure_sequence)
        print('first sequence: ', self.first_sequence)
        print('second sequence: ', self.second_sequence)
        
        if self.pure_sequence + self.first_sequence + self.second_sequence == 3 and self.pure_sequence > 0:
            self.done = True


        return final_card_to_drop, self.done, r3

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
        print('------------------')
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

deck = pydealer.Deck()

deck.shuffle()
cards = deck.deal(10)

hand = pydealer.Stack()
hand.add(cards)

grandma = Agent(hand)

prev_card = deck.deal(1)[0]

print(grandma.matrix)

print(grandma.play_turn(prev_card,deck))

print(grandma.matrix)