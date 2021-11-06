import socketio
import asyncio
import pickle
from grandma import Grandma
from model import Agent
import sys
import os
from ftp_client import FTPClient

ftp_client = FTPClient('0.0.0.0', 'grandma', '123')


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

tag = 'A'
client_name = 'client_' + tag

client_status = 'standby'
ftp_client_status = 'standby'
hand = None
server_status = 'standby'
has_played = False
p_score = 0
global_done = False
table_top_card = None
deck_top_card = None
flag_deck_top_card = False
game_number = 1

agent = Agent(11,(52,),n_epochs=5,name=tag)

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
    global server_status, client_status, hand, has_played, player, p_score, global_done, table_top_card, deck_top_card, flag_deck_top_card, game_number, ftp_client_status
    server_status = data['server_status']
    current_player = data['current_player']
    table_top_card = pickle.loads(data['table_top_card'])
    deck_top_card = pickle.loads(data['deck_top_card'])
    global_done = data['global_done']
    game_number = data['game_number']
    ftp_server_status = data['ftp_server_status']


    if deck_top_card is not None:
        ftp_client_status = 'standby'
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
            
            print('Reward: {}  Done: {}'.format(p_score,done))

            print(str(client_name) + ' has played.')
            has_played = True
        else:
            has_played = False

    else:
        if game_number > 1:

            if ftp_server_status != 'aggregated' and ftp_client_status == 'standby':
                player.model.save_models()
                # Send to FTP Server
                print('Uploading local model to server...')
                ftp_client.upload('local_ckpts/actor_'+tag,'incoming_ckpts/actors/actor_'+tag) # server,client
                ftp_client.upload('local_ckpts/critic_'+tag,'incoming_ckpts/critics/critic_'+tag) # server,client
                print('Uploaded!')
                
                ftp_client_status = 'uploaded'
                client_status = 'standby'

                dir = 'local_ckpts'
                for f in os.listdir(dir):
                    os.remove(os.path.join(dir, f))

            # Get aggregated model from FTP Server
            if ftp_server_status == 'aggregated' and ftp_client_status == 'uploaded':
                print('Downloading global model from server...')
                ftp_client.download('local_ckpts/actor_G','global_ckpt/actor_G') # client,server
                ftp_client.download('local_ckpts/critic_G','global_ckpt/critic_G') # client,server
                print('Downloaded!')
                ftp_client_status = 'downloaded'

                        
                player.model.load_models()
                print('Aggregated Model loaded successfully!')

                # Cleanup old model (with name tag)
                # Cleanup old model (with name 'G')                
                dir = 'local_ckpts'
                for f in os.listdir(dir):
                    os.remove(os.path.join(dir, f))
            
        # print('Deck Empty. Starting New Game!')
        has_played = False

@sio.on('set_hand')
async def set_hand(data):
    global client_status, hand, player, agent, p_score, ftp_client_status
    hand = pickle.loads(data['hand'])
    print('Hand set: ', hand)
    player = Grandma(hand,agent)
    p_score = 0
    client_status = 'ready'
    

@sio.event
async def track_status():
    global server_status, client_name, has_played, global_done, table_top_card, flag_deck_top_card, ftp_client_status
    while True:
        await sio.emit('client_status',{'client_name':client_name,
        'client_status':client_status, 
        'ftp_client_status':ftp_client_status,
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