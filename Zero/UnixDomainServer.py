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
        logging.debug('Bind in: {0}'.format(str(self.server_address)))

    def loop(self, conexao_ativa):
        '''Executa servidor quando conectado ou TO'''
        while True:

            try:
                logging.debug("Esperando nova conexao")

                # accept connections from outside
                clientsocket, address = self._sock.accept()

                comm_param={}
                comm_param['clientsocket'] = clientsocket
                comm_param['addr']=  address

                logging.debug("Conectado com :%s", str(address))

                tot = len(self.lista_thread_online)
                t = threading.Thread(target=conexao_ativa, args=(tot, comm_param))
                t.start()

                self.lista_thread_online.append(t)

            except socket.timeout:
                logging.debug('Server to..')

            except Exception as exp:
                logging.exception('Falha:%s', str(exp))
                break

        logging.debug("listen encerrado")