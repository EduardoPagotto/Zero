#!/usr/bin/env python3
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

        self.setSocket(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))

        #val1 = 
        self._sock.connect(server_address)
        #logging.debug('val1:{0}'.format(str(val1)))


    # def connect(self, conexao):
    #     val1 = self._sock.connect(conexao)
    #     logging.debug('val1:{0}'.format(str(val1)))