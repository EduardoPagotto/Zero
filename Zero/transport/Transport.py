'''
Created on 20190822
Update on 20200517
@author: Eduardo Pagotto
'''

#pylint: disable=C0301, C0116, W0703, C0103, C0115

import sys
import os
import socket
import logging

from enum import Enum
from Zero.transport.SocketBase import SocketBase

class TransportKind(Enum):
    UNIX_DOMAIN = 0,
    NETWORK = 1,

def get_address_from_string(s_address):
    """[Return a valid data connection]
    Arguments:
        s_address {[string]} -- [valid example ( uds://./conexao_peer | tcp:s//127.0.0.1:5151) ]
    Raises:
        Exception: [malformed TCP dats]
        Exception: [malformed string kind]
    Returns:
        [tuple (address peer (tuple('ip':port) | 'uds path', TransportKind)) ] -- [Valid connection data]
    """
    address = None
    transportKind = None

    if 'uds://' in s_address:
        address = s_address.partition('uds://')[2]
        transportKind = TransportKind.UNIX_DOMAIN
    elif 'tcp://' in s_address:
        val = s_address.partition('tcp://')[2]
        final = val.split(':')

        if len(final) != 2:
            raise Exception('Invalid TCP Address: {0}'.format(s_address))

        address = (final[0], int(final[1]))
        transportKind = TransportKind.NETWORK
    else:
        raise Exception('Invalid Address kind:{0}'.format(s_address))

    return (address, transportKind)

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

    soc.getSocket().listen(15)
    logging.getLogger('Zero').debug('Bind in: %s', str(server_address))

    return soc

def transportClient(transportKind, server_address):

    soc = SocketBase()

    if transportKind == TransportKind.UNIX_DOMAIN:
        soc.setSocket(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
    else:
        soc.setSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    soc.getSocket().connect(server_address)
    logging.getLogger('Zero').debug('Connected: %s', str(server_address))

    return soc

# TODO: implementar a continuação do inetd, neste caso a conexao ja é a final, indo direto para o protocolo
def iNetdServer():
    '''Wrapper de conexao no inetd/xinetd'''
    soc = SocketBase()
    soc.setSocket(socket.fromfd(sys.stdin.fileno(), socket.AF_INET, socket.SOCK_STREAM))
    server_address = soc.getSocket().getsockname()
    logging.getLogger('Zero').debug('Connected in: %s', str(server_address))

    return soc
