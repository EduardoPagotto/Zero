'''
Created on 20190822
Update on 20200727
@author: Eduardo Pagotto
'''

import sys
import os
import socket
import logging
import time

from typing import Tuple, Union
from abc import ABC, abstractmethod

from enum import Enum
from Zero.transport.SocketBase import SocketBase
from Zero.subsys.ExceptionZero import ExceptionZero

class SocketFactory(ABC):
    """[Factory of new connections]
    Args:
        ABC ([type]): [description]
    """

    def __init__(self, s_address : str):
        """[Host connection]
        Args:
            s_address (str): [valids: uds://./conexao_peer amd tcp:s//127.0.0.1:5151]
        Raises:
            Exception: [malformed TCP/IP]
            Exception: [malformed UDS path]
        """

        self.log = logging.getLogger('Zero')
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

    @abstractmethod
    def create_socket(self) -> SocketBase:
        pass

class SocketFactoryServer(SocketFactory):
    """[Factory of new Server Bind]
    Args:
        SocketFactory ([type]): [description]
    """

    def __init__(self, s_address):
        """[summary]
        Args:
            s_address (str): [valids: uds://./conexao_peer amd tcp:s//127.0.0.1:5151]
        """
        super().__init__(s_address)

    def create_socket(self) -> SocketBase:
        """[Create a socket server]
        Returns:
            SocketBase: [Server binded Socket]
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
        self.log.debug('bind in: %s', str(self.s_address))

        return soc

class SocketFactoryClient(SocketFactory):
    """[Factory of new Client connectiom]
    Args:
        SocketFactory ([type]): [description]
    """

    def __init__(self, s_address : str, re_try: int=3):
        """[summary]
        Args:
            s_address (str): [valids: uds://./conexao_peer amd tcp:s//127.0.0.1:5151]
            re_try (int, optional): [re-try befor exception]. Defaults to 3.
        """
        super().__init__(s_address)
        self.re_try = re_try

    def create_socket(self) -> SocketBase:
        """[Create a connection with server RPC]
        Raises:
            ExceptionZero: [raise if fail to connect]
        Returns:
            SocketBase: [Socket connected to server]
        """

        counter = 0
        while counter < self.re_try:
            try:
                soc = SocketBase()
                if self.kind == 0:
                    soc.setSocket(socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
                    soc.getSocket().connect(self.uds)
                else:
                    soc.setSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                    soc.getSocket().connect(self.tcp_ip)

                self.log.info('connected: %s', str(self.s_address))
                return soc

            except Exception as exp:
                self.log.debug('connection %s error (%d/%d)', str(self.s_address), counter + 1, self.re_try)

            time.sleep(5) # delay entre as tentativas
            counter += 1

        raise ExceptionZero('connection {0} fail'.format(str(self.s_address)))

    # # TODO: implementar a continuação do inetd, neste caso a conexao ja é a final, indo direto para o protocolo
    # def iNetdServer(self) -> SocketBase:
    #     '''Wrapper de conexao no inetd/xinetd'''
    #     soc = SocketBase()
    #     soc.setSocket(socket.fromfd(sys.stdin.fileno(), socket.AF_INET, socket.SOCK_STREAM))
    #     server_address = soc.getSocket().getsockname()
    #     logging.getLogger('Zero').debug('Connected in: %s', str(server_address))

    #     return soc
