'''
Created on 20170119
Update on 20190822
@author: Eduardo Pagotto
'''

import sys
import os
import socket
import logging

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


class NetworkServer(SocketBase):
    def __init__(self, server_address):
        super().__init__()

        host_name = server_address[0]
        porta = host_name[1]

        self.setSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

        if host_name is None:
            self.getSocket().bind((socket.gethostname(), porta))
        else:
            self.getSocket().bind(server_address)

        self.getSocket().listen(5)

        logging.debug('Bind in: {0}'.format(str(server_address)))

# TODO: implementar a continuação do inetd, neste caso a conexao ja é a final, indo direto para o protocolo
class INetdServer(SocketBase):
    '''Wrapper de conexao no inetd/xinetd'''
    def __init__(self):
        super().__init__()
        self.setSocket(socket.fromfd(sys.stdin.fileno(), socket.AF_INET, socket.SOCK_STREAM))
        server_address = self.getSocket().getsockname()

        logging.debug('Connected in: {0}'.format(str(server_address)))
