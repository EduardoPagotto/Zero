'''
Created on 20190822
Update on 20190822
@author: Eduardo Pagotto
'''

import sys
import os
import socket
import logging

from enum import Enum
from Zero.transport.SocketBase import SocketBase

class TransportKind(Enum):
    UNIX_DOMAIN = 0,
    NETWORK = 1,

def transportServer(transportKind, server_address):

    host_name = None
    porta = 80
    soc = None

    if transportKind == TransportKind.UNIX_DOMAIN:
        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise

        soc = SocketBase()
        soc.setSocket(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
        soc.getSocket().bind(server_address)

    else:
        host_name = server_address[0]
        porta = server_address[1]

        soc = SocketBase()
        soc.setSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

        if host_name is None:
            soc.getSocket().bind((soc.getSocket().gethostname(), porta))
        else:
            soc.getSocket().bind(server_address)

    soc.getSocket().listen(5)
    logging.getLogger('Zero').debug('Bind in: {0}'.format(str(server_address)))

    return soc

def transportClient(transportKind, server_address):

    soc = SocketBase()

    if transportKind == TransportKind.UNIX_DOMAIN:
        soc.setSocket(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
    else:
        soc.setSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    soc.getSocket().connect(server_address)
    logging.getLogger('Zero').debug('Connected: {0}'.format(str(server_address)))

    return soc

# TODO: implementar a continuação do inetd, neste caso a conexao ja é a final, indo direto para o protocolo
def iNetdServer():
    '''Wrapper de conexao no inetd/xinetd'''
    soc = SocketBase()
    soc.setSocket(socket.fromfd(sys.stdin.fileno(), socket.AF_INET, socket.SOCK_STREAM))
    server_address = soc.getSocket().getsockname()
    logging.getLogger('Zero').debug('Connected in: {0}'.format(str(server_address)))

    return soc
