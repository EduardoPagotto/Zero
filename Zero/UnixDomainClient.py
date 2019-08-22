'''
Created on 20190821
Update on 20190822
@author: Eduardo Pagotto
'''

import socket
import logging

from Zero.SocketBase import SocketBase

class UnixDomainClient(SocketBase):
    def __init__(self, server_address):
        super().__init__()
        self.setSocket(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
        self.getSocket().connect(server_address)
        logging.debug('Connected: {0}'.format(str(server_address)))

class NetworkClient(SocketBase):
    def __init__(self, server_address):
        super().__init__()
        self.setSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.getSocket().connect(server_address)
        logging.debug('Connected: {0}'.format(str(server_address)))