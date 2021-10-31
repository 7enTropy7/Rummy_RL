import socketio
from aiohttp import web
import pickle
import random
import pydealer

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

@sio.on('client_status')
async def client_status(sid, data):
    global server_status, client_statuses, hands, deck, current_player
    client_statuses[data['client_name']] = data['client_status']
    has_played = data['has_played']

    
    if client_statuses[data['client_name']] == 'ready' and hands[data['client_name']] is None:
        cards = deck.deal(10)
        hand = pydealer.Stack()
        hand.add(cards)
        hands[data['client_name']] = hand
        await sio.emit('set_hand', {'hand':pickle.dumps(hands[data['client_name']])}, room=sid)

    if check_for_readiness(client_statuses):
        server_status = 'ready'
    
    if server_status == 'ready' and has_played:
        print(data['client_name'],' has played!')
        if current_player == 'client_A':
            current_player = 'client_B'
        elif current_player == 'client_B':
            current_player = 'client_C'
        elif current_player == 'client_C':
            current_player = 'client_A'

    # print(client_statuses, deck.size)
    
    return {'server_status': server_status, 'current_player' : current_player}

def check_for_readiness(client_statuses):
    for client_status in client_statuses.values():
        if client_status != 'ready':
            return False
    return True



'''
table_top_card,
deck_top_card,
player_turn,

'''

'''
1. Server sends an emit to all clients for their status. Broadcast loop
2. Each client emits back a response.
3. Client responses get stored in a dictionary on the server.
4. Server doesn't exit the broadcast loop until all clients have responded "ready".
5. Server then sends a "start" event to all clients.

'''



'''
TODO:
send table_top_card, deck_top_card, hand to client
create 3 callbacks for these 3 
the work on ftp and model transmission
'''