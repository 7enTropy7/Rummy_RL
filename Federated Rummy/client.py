import socketio
import asyncio
import pickle
# from rummy import *

loop = asyncio.get_event_loop()
sio = socketio.AsyncClient()

client_name = 'client_C'
client_status = 'standby'
hand = None
server_status = 'standby'

@sio.event
async def connect():
    global client_status
    print('Connected to server')
    client_status = 'ready'
    sio.start_background_task(track_status)

@sio.event
async def client_status_callback(data):
    global server_status, hand
    server_status = data
    print('Server Status: ',server_status)

@sio.on('set_hand')
async def set_hand(data):
    global hand
    hand = pickle.loads(data['hand'])
    print('Hand set: ', hand)

@sio.event
async def track_status():
    global server_status, client_name
    while True:
        await sio.emit('client_status',{'client_name':client_name,'client_status':client_status}, callback=client_status_callback)
        await sio.sleep(5)
        if server_status == 'ready':
            break
    
async def start_client():
    await sio.connect('http://localhost:9999', transports=['websocket'],
                      namespaces=['/'])
        
    await sio.wait()
    await sio.disconnect()
    print('Done')

if __name__ == '__main__':
    loop.run_until_complete(start_client())