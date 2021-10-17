import socketio
import pickle

sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')
    sio.start_background_task(game)

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event(namespace='/rummy')
def message(data=None):
    print('Received message: ', data)

@sio.event(namespace='/rummy')
def game_callback(data=None):
    print('Received game callback: ', data)

@sio.on('deal', namespace='/rummy')
def deal(data=None):
    print('Received deal: ', data)

@sio.event(namespace='/rummy')
def handshake_callback(data=None):
    print('Received handshake callback: ', pickle.loads(data))

@sio.event(namespace='/rummy')
def game():
    for i in range(2):
        sio.emit('handshake', {'data':'Handshake'},namespace='/rummy', callback=handshake_callback)
        sio.sleep(5)
    while True:
        sio.emit('game', {'data': 'Hello World!'},namespace='/rummy',callback=game_callback)
        sio.sleep(5)

sio.connect('http://localhost:9999', namespaces=['/rummy'])
sio.wait()