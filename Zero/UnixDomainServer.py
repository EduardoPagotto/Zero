'''
Created on 20170119
Update on 20190821
@author: Eduardo Pagotto
'''

import os
import socket
import logging
import threading

from Zero.SocketBase import SocketBase

class UnixDomainServer(SocketBase):
    def __init__(self, server_address):

        super().__init__()
        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise

        self.setSocket(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
        self.getSocket().bind(server_address)
        self.getSocket().listen(5)
        logging.debug('Bind in: {0}'.format(str(server_address)))
