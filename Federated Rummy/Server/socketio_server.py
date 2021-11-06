import socketio
from aiohttp import web
import pickle
import random
import pydealer
from socketio import server
import sys
import os
from utils import aggregate_models

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='aiohttp', async_handlers=True)

# Creates a new Aiohttp Web Application
app = web.Application()

# Binds our Socket.IO server to our Web App instance
sio.attach(app)


@sio.event
async def connect(sid, environ):
    print('Connected: ', sid)
    

@sio.event
async def disconnect(sid):
    print('Disconnected: ', sid)

server_status = 'standby'

client_statuses = {'client_A': 'standby', 'client_B': 'standby', 'client_C': 'standby'}
current_player = 'client_A'
ftp_client_statuses = {'client_A': 'standby', 'client_B': 'standby', 'client_C': 'standby'}
ftp_server_status = 'standby'
hands = {'client_A': None, 'client_B': None, 'client_C': None}
deck = pydealer.Deck()
deck.shuffle()
table_top_card = deck.deal(1)[0]
deck_top_card = None
global_done = False
game_number = 1



@sio.on('client_status')
async def client_status(sid, data):
    global server_status, client_statuses, hands, deck, current_player, table_top_card, deck_top_card, global_done, game_number, ftp_client_statuses, ftp_server_status
    client_statuses[data['client_name']] = data['client_status']
    ftp_client_statuses[data['client_name']] = data['ftp_client_status']
    has_played = data['has_played']
    global_done = data['global_done']
    flag_deck_top_card = data['flag_deck_top_card']


    if deck.size == 0:
        global_done = False
        print('------------------ Restart Game ------------------' + '    Game Count: ' + str(game_number))
        
        # actor_path = 'incoming_ckpts/actors'
        # num_act_wts = [name for name in os.listdir(actor_path) if os.path.isfile(os.path.join(actor_path, name))]

        # critic_path = 'incoming_ckpts/critics'
        # num_crt_wts = [name for name in os.listdir(critic_path) if os.path.isfile(os.path.join(critic_path, name))]

        # print('@@@@@@@@@@@@@@@@@@@@@')
        # print(num_act_wts,num_crt_wts)

        # if len(num_act_wts) ==3 and len(num_crt_wts) == 3:
        #     aggregate_models()



        game_number += 1
        deck = pydealer.Deck()
        deck.shuffle()
        table_top_card = deck.deal(1)[0]
        deck_top_card = None
        hands = {'client_A': None, 'client_B': None, 'client_C': None}
        client_statuses = {'client_A': 'standby', 'client_B': 'standby', 'client_C': 'standby'}
        current_player = 'client_A'
        
        has_played = False
        server_status = 'standby'

    if FTP_check_for_uploaded_readiness(ftp_client_statuses) and ftp_server_status != 'aggregated':
        aggregate_models()
        ftp_server_status = 'aggregated'
            

    if global_done:
        server_status = 'GAME OVER'
        print('@@@@@@@@@@@@@@@@@@@@@@@ WINNER @@@@@@@@@@@@@@@@@@@@@')
        print(data['client_name'],' has won the GAME!')
        sys.exit()
        
    
    if hands[data['client_name']] is None and (FTP_check_for_downloaded_readiness(ftp_client_statuses) or game_number==1):
        cards = deck.deal(10)
        hand = pydealer.Stack()
        hand.add(cards)
        hands[data['client_name']] = hand
        ftp_server_status = 'standby'
        await sio.emit('set_hand', {'hand':pickle.dumps(hands[data['client_name']])}, room=sid)

    if check_for_readiness(client_statuses) and server_status != 'GAME OVER':        
        
        server_status = 'ready'
        deck_top_card = deck[deck.size-1]
        
    if server_status == 'ready' and has_played:
        table_top_card = pickle.loads(data['table_top_card'])
        if flag_deck_top_card:
            temp = deck.deal(1)
            if deck.size > 0:
                deck_top_card = deck[deck.size-1]
            else:
                deck_top_card = None

        print(str(data['client_name']) + ' has played ' + str(table_top_card) + '    Deck Size: ' + str(deck.size))
        if current_player == 'client_A':
            current_player = 'client_B'
        elif current_player == 'client_B':
            current_player = 'client_C'
        elif current_player == 'client_C':
            current_player = 'client_A'


    return {'server_status': server_status, 
    'current_player' : current_player, 
    'table_top_card': pickle.dumps(table_top_card), 
    'deck_top_card': pickle.dumps(deck_top_card), 
    'global_done':global_done,
    'game_number':game_number,
    'ftp_server_status':ftp_server_status}

def FTP_check_for_downloaded_readiness(ftp_client_statuses):
    for ftp_client_status in ftp_client_statuses.values():
        if ftp_client_status != 'downloaded':
            return False
    return True

def FTP_check_for_uploaded_readiness(ftp_client_statuses):
    for ftp_client_status in ftp_client_statuses.values():
        if ftp_client_status != 'uploaded':
            return False
    return True

def check_for_readiness(client_statuses):
    for client_status in client_statuses.values():
        if client_status != 'ready':
            return False
    return True