'''
Created on 20190821
Update on 20190821
@author: Eduardo Pagotto
'''

import os
import socket
import logging
import threading

from Zero.SocketBase import SocketBase

class UnixDomainClient(SocketBase):
    def __init__(self, server_address):
        super().__init__()
        self.server_address = server_address
        self.setSocket(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
        self.getSocket().connect(self.server_address)
        logging.debug('Connected: {0}'.format(str(self.server_address)))