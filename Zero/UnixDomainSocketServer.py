
#!/usr/bin/env python3
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

class UnixDomainServer(SocketBase):
    def __init__(self, server_address):

        super().__init__()

        self.lista_thread_online = []
        self.server_address = server_address
        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise

        self.setSocket(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))

        self._sock.bind(server_address)
        self._sock.listen(5)

    def loop(self, conexao_ativa):
        '''Executa servidor quando conectado ou TO'''
        while True:

            logging.info("Esperando nova conexao")

            # accept connections from outside
            clientsocket, address = self._sock.accept()

            my_dict={}
            my_dict['clientsocket'] = clientsocket
            my_dict['addr']=  address

            logging.info("Conectado com :%s", str(address))

            tot = len(self.lista_thread_online)
            t = threading.Thread(target=conexao_ativa, args=(tot, my_dict))#, kwargs=my_dict)
            t.start()

            self.lista_thread_online.append(t)