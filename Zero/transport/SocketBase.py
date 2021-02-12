'''
Created on 20170119
Update on 20210212
@author: Eduardo Pagotto
'''

import socket

from typing import Any, Optional, Union, List
from ..subsys import ExceptionZero

BLOCK_SIZE = 2048

class SocketBase(object):
    """[Class Socket]
    Args:
        object ([type]): [description]
    """

    def __init__(self):
        """[Create a empty socket]
        """

        self._sock : Union[socket.socket, Any] = None

    def getSocket(self) -> socket.socket:
        """[Return a socket value]
        Returns:
            socket.socket: [low level socket]
        """

        return self._sock

    def setSocket(self, socketIn: socket.socket) -> None:
        """[Set a low level socket]
        Args:
            socketIn (socket.socket): [new socket]
        """

        self._sock = socketIn

    def settimeout(self, time_out: Optional[float]=300) -> None:
        """[Set a Time-out to receave]
        Args:
            time_out (Optional[float], optional): [time in sec]. Defaults to 300.
        """

        self._sock.settimeout(time_out)

    def gettimeout(self) -> Optional[float]:
        """[Get a time-out to receive]
        Returns:
            Optional[float]: [Value of time-out]
        """

        return self._sock.gettimeout()

    def close(self) -> None:
        """[Close de connection, delete de socket]
        """

        if self._sock is not None:
            self._sock.close()
            self._sock = None

    def isConnected(self) -> bool:
        """[Get status Connection]
        Returns:
            bool: [True if connected]
        """

        return True if self._sock is not None else False

    def connect(self, conexao: Union[Union[tuple, str], bytes]) -> None:
        """[Connect with peear using conexao data]
        Args:
            conexao (Union[socket._Address, bytes]): [address of server]
        """

        self._sock.connect(conexao)

    def sendBlocks(self, _buffer : bytes) -> int:
        """[Send chunk's to host connected]
        Args:
            _buffer (bytes): [Data to transfer]
        Raises:
            ExceptionZero: [Raise if chunk's fail]
        Returns:
            int: [Total receved]
        """

        total_enviado : int = 0
        total_buffer :int = len(_buffer)
        while total_enviado < total_buffer:
            tam : int = total_buffer - total_enviado
            if tam > BLOCK_SIZE:
                tam = BLOCK_SIZE

            inicio = total_enviado
            fim = total_enviado + tam

            sub_buffer = bytearray(_buffer[inicio:fim])
            sent = self._sock.send(sub_buffer)
            if sent == 0:
                raise ExceptionZero("Fail to send a chunk")

            #os.write(self.io, sub_buffer)
            total_enviado = fim

        return total_enviado

    def receiveBlocks(self, _tamanho : int) -> bytes:
        """[Receive chunk's from host connected]
        Args:
            _tamanho (int): [total to receve]
        Raises:
            ExceptionZero: [Raise if chunk's fail]
        Returns:
            bytes: [Buffer with data receved]
        """

        total_recebido : int = 0
        buffer_local : bytes = bytes()

        while total_recebido < _tamanho:
            tam : int = _tamanho - total_recebido
            if tam > BLOCK_SIZE:
                tam = BLOCK_SIZE

            #buffer_local += os.read(self.io, tam)
            chunk : bytes = self._sock.recv(tam)
            if chunk == b'':
                raise ExceptionZero("Fail Receive a chunk")

            buffer_local += chunk

            total_recebido = len(buffer_local)

        return buffer_local
