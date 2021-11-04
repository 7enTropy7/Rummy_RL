import socketio
import asyncio
import pickle
from grandma import Grandma
from model import Agent
import argparse
import sys

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

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()

parser = argparse.ArgumentParser()
parser.add_argument("--client_name", help="Set the client name",type=str)
args = parser.parse_args()

client_name = 'client_'+ args.client_name

client_status = 'standby'
hand = None
server_status = 'standby'
has_played = False
p_score = 0
global_done = False
table_top_card = None
deck_top_card = None
flag_deck_top_card = False


agent = Agent(11,(52,),n_epochs=5)
# agent.load_models()

player = None

@sio.event
async def connect():
    global client_status
    print('Connected to server')
    
    sio.start_background_task(track_status)

@sio.event
async def disconnect():
    print('Disconnected from server')
    sys.exit()

@sio.event
async def client_status_callback(data):
    global server_status, client_status, hand, has_played, player, p_score, global_done, table_top_card, deck_top_card, flag_deck_top_card
    server_status = data['server_status']
    current_player = data['current_player']
    table_top_card = pickle.loads(data['table_top_card'])
    deck_top_card = pickle.loads(data['deck_top_card'])
    global_done = data['global_done']

    if deck_top_card is not None:

        # print('Server Status: ' + str(server_status) + '   Current Player: ' + str(current_player))
        if server_status == 'ready' and current_player == client_name:

            table_top_card, action, probs, crit_val, reward, done, flag_deck_top_card = player.choose_action(table_top_card, deck_top_card)
            p_score = round(reward,2)

            print(player.matrix,'\n')

            if done:
                print('############# WINNER ###############')
                print('\nWinner\'s Hand: \n {}'.format(player.matrix))
                print('!!!!!!!!!!!! GAME OVER !!!!!!!!!!!!')
                global_done = True
            
            player.remember(player.binary_matrix, action, probs, crit_val, reward, done)
                
            player.learn()
            # player.model.save_models()
            
            print('Reward: {}  Done: {}'.format(p_score,done))


            print(str(client_name) + ' has played.')
            has_played = True
        else:
            has_played = False

    else:
        print('Deck Empty. Starting New Game!')
        # client_status = 'standby'
        has_played = False

@sio.on('set_hand')
async def set_hand(data):
    global client_status, hand, player, agent, p_score
    hand = pickle.loads(data['hand'])
    print('Hand set: ', hand)
    player = Grandma(hand,agent)
    p_score = 0
    client_status = 'ready'

@sio.event
async def track_status():
    global server_status, client_name, has_played, global_done, table_top_card, flag_deck_top_card
    while True:
        await sio.emit('client_status',{'client_name':client_name,
        'client_status':client_status, 
        'has_played':has_played,
        'global_done':global_done,
        'table_top_card':pickle.dumps(table_top_card),
        'flag_deck_top_card':flag_deck_top_card}, callback=client_status_callback)
        
        await sio.sleep(0.5)
        # if server_status == 'ready':
            # break
    
async def start_client():
    await sio.connect('http://localhost:9999', transports=['websocket'],
                      namespaces=['/'])
        
    await sio.wait()
    await sio.disconnect()

if __name__ == '__main__':
    loop.run_until_complete(start_client())