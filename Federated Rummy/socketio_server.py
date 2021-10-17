import socketio
from aiohttp import web
import pickle
import pydealer

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='aiohttp', async_handlers=True)

# Creates a new Aiohttp Web Application
app = web.Application()

# Binds our Socket.IO server to our Web App instance
sio.attach(app)

deck = pydealer.Deck()
deck.shuffle()

@sio.event
async def connect(sid, environ):
    print('Connected: ', sid)
    

@sio.event
async def disconnect(sid):
    print('Disconnected: ', sid)

@sio.on('handshake',namespace='/rummy')
def handshake(sid, data):
    global deck
    print('Handshake')
    return pickle.dumps(deck)

@sio.on('game',namespace='/rummy')
def game(sid, data):
    print('game: ', data)
    return 10
