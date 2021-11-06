from pyftpdlib import authorizers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
import json
import sys
from hashlib import md5

class DummyMD5Authorizer(DummyAuthorizer):

    def validate_authentication(self, username, password, handler):
        if sys.version_info >= (3, 0):
            password = password.encode('latin1')
        hash = md5(password).hexdigest()
        try:
            if self.user_table[username]['pwd'] != hash:
                raise KeyError
        except KeyError:
            raise AuthenticationFailed

class FTP_Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.usernames, self.passwords = self.load_usernames_passwords()
        self.hashes = [md5(password.encode('latin1')).hexdigest() for password in self.passwords]
        self.save_directory = "."
        self.handler = self.initialize_handler()
        self.ftp_server = FTPServer((self.host, self.port),self.handler)
    
    def load_usernames_passwords(self):
        with open('config.json', 'r') as openfile:
            details = json.load(openfile)
        return list(details.keys()), list(details.values())

    def initialize_handler(self):
        authorizer = DummyMD5Authorizer()
        for i in range(len(self.usernames)):
            authorizer.add_user(self.usernames[i], self.hashes[i], self.save_directory, perm='elradfmw')
        
        # print(authorizer.user_table)
        # with open("user_table.json", "w") as outfile:
        #     json.dump(authorizer.user_table, outfile)

        handler = FTPHandler
        handler.authorizer = authorizer
        return handler

    def run(self):
        self.ftp_server.serve_forever()

ftp_server = FTP_Server("0.0.0.0", 21)
ftp_server.run()