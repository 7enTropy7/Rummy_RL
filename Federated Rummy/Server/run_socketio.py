from aiohttp import web
from socketio_server import app

if __name__ == '__main__':
    print("Starting server...")
    web.run_app(app, port=9999)