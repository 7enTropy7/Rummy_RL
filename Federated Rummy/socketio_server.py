import socketio
from aiohttp import web
import pickle
import random
import pydealer
from socketio import server

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='aiohttp', async_handlers=True)

# Creates a new Aiohttp Web Application
app = web.Application()

# Binds our Socket.IO server to our Web App instance
sio.attach(app)

# deck = None
# deck.shuffle()

@sio.event
async def connect(sid, environ):
    print('Connected: ', sid)
    

@sio.event
async def disconnect(sid):
    print('Disconnected: ', sid)

server_status = 'standby'

client_statuses = {'client_A': 'standby', 'client_B': 'standby', 'client_C': 'standby'}
current_player = 'client_A'

hands = {'client_A': None, 'client_B': None, 'client_C': None}
deck = pydealer.Deck()
deck.shuffle()
table_top_card = deck.deal(1)[0]
deck_top_card = None
global_done = False

@sio.on('client_status')
async def client_status(sid, data):
    global server_status, client_statuses, hands, deck, current_player, table_top_card, deck_top_card, global_done
    client_statuses[data['client_name']] = data['client_status']
    has_played = data['has_played']
    global_done = data['global_done']
    flag_deck_top_card = data['flag_deck_top_card']

    if deck.size == 0:
        global_done = True
        print('Restart Game' + '    Deck Size: ' + str(deck.size))

    if global_done:
        server_status = 'GAME OVER'
    
    if client_statuses[data['client_name']] == 'ready' and hands[data['client_name']] is None:
        cards = deck.deal(10)
        hand = pydealer.Stack()
        hand.add(cards)
        hands[data['client_name']] = hand
        await sio.emit('set_hand', {'hand':pickle.dumps(hands[data['client_name']])}, room=sid)

    if check_for_readiness(client_statuses) and server_status != 'GAME OVER':
        server_status = 'ready'
        deck_top_card = deck[deck.size-1]
        
    if server_status == 'ready' and has_played and server_status != 'GAME OVER':
                
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
    'global_done':global_done}

def check_for_readiness(client_statuses):
    for client_status in client_statuses.values():
        if client_status != 'ready':
            return False
    return True
