'''
Created on 20190822
Update on 20200725
@author: Eduardo Pagotto
'''

import sys
import os
import socket
import logging

from typing import Tuple, Union

from enum import Enum
from Zero.transport.SocketBase import SocketBase

class SocketFactory(object):
    """[Factory of new connections]
    Args:
        object ([type]): [description]
    """

    def __init__(self, s_address : str):
        """[Host connection]
        Args:
            s_address (str): [valids: uds://./conexao_peer amd tcp:s//127.0.0.1:5151]
        Raises:
            Exception: [malformed TCP/IP]
            Exception: [malformed UDS path]
        """

        self.kind : int = 0 # 0=UDS ; 1=TCPIP
        self.s_address : str = s_address
        self.uds:str
        self.tcp_ip: Tuple[str, int]

        if 'uds://' in s_address:
            self.uds = s_address.partition('uds://')[2]

        elif 'tcp://' in s_address:
            self.kind = 1
            val = s_address.partition('tcp://')[2]
            final = val.split(':')

            if len(final) != 2:
                raise Exception('Invalid TCP Address: {0}'.format(s_address))

            self.tcp_ip = (final[0], int(final[1]))

        else:
            raise Exception('Invalid Address :{0}'.format(s_address))

    def get_server(self) -> SocketBase:
        """[Create a socket server]
        Returns:
            SocketBase: [socket]
        """
        host_name = None
        porta = 80
        soc = None

        if self.kind == 0:
            try:
                os.unlink(self.uds)
            except OSError:
                if os.path.exists(self.uds):
                    raise

            soc = SocketBase()
            soc.setSocket(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
            soc.getSocket().bind(self.uds)

        else:
            host_name = self.tcp_ip[0]
            porta = self.tcp_ip[1]

            soc = SocketBase()
            soc.setSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

            if host_name is None:
                soc.getSocket().bind((soc.getSocket().gethostname(), porta))
            else:
                soc.getSocket().bind(self.tcp_ip)

        soc.getSocket().listen(15)
        logging.getLogger('Zero').debug('Bind in: %s', str(self.s_address))

        return soc

    def get_client(self)-> SocketBase:
        """[summary]
        Returns:
            SocketBase: [description]
        """

        soc = SocketBase()

        if self.kind == 0:
            soc.setSocket(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
            soc.getSocket().connect(self.uds)
        else:
            soc.setSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            soc.getSocket().connect(self.tcp_ip)

        logging.getLogger('Zero').debug('Connected: %s', str(self.s_address))

        return soc

    # # TODO: implementar a continuação do inetd, neste caso a conexao ja é a final, indo direto para o protocolo
    # def iNetdServer(self) -> SocketBase:
    #     '''Wrapper de conexao no inetd/xinetd'''
    #     soc = SocketBase()
    #     soc.setSocket(socket.fromfd(sys.stdin.fileno(), socket.AF_INET, socket.SOCK_STREAM))
    #     server_address = soc.getSocket().getsockname()
    #     logging.getLogger('Zero').debug('Connected in: %s', str(server_address))

    #     return soc
