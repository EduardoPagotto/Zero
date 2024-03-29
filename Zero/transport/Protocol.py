'''
Created on 20170119
Update on 20220916
@author: Eduardo Pagotto
'''

import os
import struct
import zlib
import logging
import socket

from typing import Tuple

from enum import Enum
from .SocketBase import SocketBase
from ..subsys import ExceptionZero, ExceptionZeroClose, ExceptionZeroErro

class ProtocolCode(Enum):
    """[Protocl commands id's]
    Args:
        Enum ([int]): [1 - opem connection
                       2 - Close event
                       3 - Command message
                       4 - Result of Command (3)
                       5 - File Exchange (TODO)
                       255 - Erro Message from host connected]
    """
    OPEN = 1
    CLOSE = 2
    COMMAND = 3
    RESULT = 4
    FILE = 5
    OK = 6 # Return of FILE opp
    ERRO = 255

class Protocol(SocketBase):
    """[Transference Protocol]
    Args:
        SocketBase ([type]): [description]
    """

    def __init__(self, socket : socket.socket):
        """[Contructor with low level socke]
        Args:
            socket (socket.socket): [new socket]
        """

        SocketBase.__init__(self)
        self.protocol_versao : str = "0.0.1"
        self.setSocket(socket)
        self.log = logging.getLogger('Zero')

    def sendProtocol(self, _id : ProtocolCode, _buffer : bytes) -> int:
        """[Send a data buffer to host connected]
        Args:
            _id (ProtocolCode): [id message]
            _buffer (bytes): [buffer data]
        Returns:
            int: [size sended]
        """

        tamanho_buffer : int = int(len(_buffer))
        comprimido :bytes = zlib.compress(_buffer)
        tamanho_comprimido : int = int(len(comprimido))
        crc : int = zlib.crc32(comprimido)

        headerTupleA : Tuple = (_id.value, 0, 0, 0, tamanho_buffer, tamanho_comprimido, crc, 0, 0, 0)
        formatoHeaderA : struct.Struct = struct.Struct('B B B B I I I I I I')
        headerA : bytes = formatoHeaderA.pack(*headerTupleA)

        crc2 :int = zlib.crc32(headerA)
        headerCRC : bytes = struct.pack("I", crc2)

        buffer_final : bytes = headerA + headerCRC + comprimido

        return self.sendBlocks(buffer_final)

    def receiveProtocol(self) -> Tuple[ProtocolCode, bytes]:
        """[Receive a data buffer from host connected]
        Raises:
            ExceptionZero: [Fail CRC header]
            ExceptionZero: [Fail CRC checksum]
            ExceptionZero: [Fail to set size buffer]
            ExceptionZeroClose: [Received Close evento from host connected]
            ExceptionZeroErro: [Redeived a erro message from host connected]
        Returns:
            Tuple[ProtocolCode, bytes]: [Code receved, data buffer receved]
        """

        buffer_header = bytearray(self.receiveBlocks(32))

        formatoHeader = struct.Struct('B B B B I I I I I I I')
        headerTuple = formatoHeader.unpack(buffer_header)

        valInt = int(headerTuple[0])
        idRecebido = ProtocolCode(valInt)

        tamanho_buffer = headerTuple[4]
        tamanho_comprimido = headerTuple[5]
        crc = headerTuple[6]
        crc2 = headerTuple[10]

        bufferHeader = buffer_header[:28]
        crcCalc2 = zlib.crc32(bufferHeader)
        if crc2 != crcCalc2:
            raise ExceptionZero('Protocol Receive Header CRC Erro')

        buffer_dados = bytearray(self.receiveBlocks(tamanho_comprimido))

        crcCalc = zlib.crc32(buffer_dados)

        if crc != crcCalc:
            raise ExceptionZero('Protocol Receive Payload CRC Erro')

        binario = zlib.decompress(buffer_dados)

        if len(binario) != tamanho_buffer:
            raise ExceptionZero('Protocol Receive size buffer error')

        if idRecebido == ProtocolCode.OPEN:
            msg = binario.decode('UTF-8')

            self.log.debug('handshake with host:%s', msg)

            self.sendString(ProtocolCode.RESULT, self.protocol_versao)

        elif idRecebido == ProtocolCode.CLOSE:
            #self.log.debug('closure receved:%s', binario.decode('UTF-8'))
            self.close()
            raise ExceptionZeroClose('close received:{0}'.format(binario.decode('UTF-8')))

        elif idRecebido == ProtocolCode.ERRO:
            raise ExceptionZeroErro('{0}'.format(binario.decode('UTF-8')))

        return idRecebido, binario

    def sendString(self, _id : ProtocolCode, _texto : str) -> int:
        """[Send a string and code to host connected]
        Args:
            _id (ProtocolCode): [Code of message]
            _texto (str): [Text to send]
        Returns:
            int: [size of message sended]
        """

        buffer = _texto.encode('UTF-8')
        return self.sendProtocol(_id, buffer)

    def receiveString(self) -> Tuple[ProtocolCode, str]:
        """[Receive a string and code to host connected]
        Returns:
            Tuple[ProtocolCode, str]: [Code and text receved]
        """

        buffer = self.receiveProtocol()
        return(buffer[0], buffer[1].decode('UTF-8'))

    def sendClose(self, _texto : str) -> None:
        """[Send a close command to host if is connected]
        Args:
            _texto (str): [text to host]
        """

        if self.isConnected() is True:
            self.log.info('closure sended:%s', _texto)
            self.sendString(ProtocolCode.CLOSE, _texto)
            self.close()

    def handShake(self) -> str:
        """[Execute a exchange of a handshake message to host connected]
        Returns:
            str: [message receved from host connected]
        """
        self.sendString(ProtocolCode.OPEN, self.protocol_versao)
        idRecive, msg = self.receiveString()
        if idRecive is ProtocolCode.RESULT:
            self.log.info('handshake with server: %s', msg)
            return msg

        raise ExceptionZero('Fail to Handshake')

    def exchange(self, input : str) -> str:
        """[Send a text to host and get message back]
        Args:
            input (str): [text to send]
        Raises:
            ExceptionZero: [Fail to get message back]
        Returns:
            str: [text receved]
        """

        self.sendString(ProtocolCode.COMMAND, input)
        id, msg = self.receiveString()
        if id == ProtocolCode.RESULT:
            return msg
            
        raise ExceptionZero('Resposta invalida: ({0} : {1})'.format(id, msg))

    def sendErro(self, msg : str) -> int:
        """[Send a erro Message to the host connected]
        Args:
            msg (str): [message to send]
        Returns:
            int: [size of message sended]
        """
        return self.sendString(ProtocolCode.ERRO, msg)

    def sendBin(self, buffer : bytes):
        """[Send a Binary data to host connected]
        Args:
            buffer (bytes): [buffer of data]
        Raises:
            ExceptionZero: [Fail to read a file from disk]
            ExceptionZero: [Fail to acess a file from disk]
            ExceptionZero: [host connected return a erro mensage]
        Returns:
            int: [size of file sended]
        """
        self.sendProtocol(ProtocolCode.FILE, buffer)
        idRecebido, msg = self.receiveString()
        if idRecebido is not ProtocolCode.OK or msg != 'OK':
            raise ExceptionZero(f'ACK send file erro {msg}')

    def sendFile(self, path_file_name : str) -> int:
        """[Send a file to host connected]
        Args:
            path_file_name (str): [path of file]
        Raises:
            ExceptionZero: [Fail to read a file from disk]
            ExceptionZero: [Fail to acess a file from disk]
            ExceptionZero: [host connected return a erro mensage]
        Returns:
            int: [size of file sended]
        """
        fileContent = None
        tamanho_arquivo = 0
        try:
            with open(path_file_name, mode='rb') as file:
                fileContent = file.read()
                tamanho_arquivo = len(fileContent)

        except IOError as e:
            msg_erro = f'Error IO file{path_file_name} :{str(e)}'
            self.sendErro(msg_erro)
            raise ExceptionZero(msg_erro)

        except Exception as exp:
            msg_erro = f'Critical error IO file{path_file_name} :{str(exp)}'
            self.sendErro(msg_erro)
            raise ExceptionZero(msg_erro)

        self.sendProtocol(ProtocolCode.FILE, fileContent)
        idRecebido, msg = self.receiveString()

        if idRecebido is not ProtocolCode.OK or msg != 'OK':
            raise ExceptionZero('Protocolo Send Falha no ACK do arquivo:{0} Erro:{1}'.format(path_file_name, msg))

        return tamanho_arquivo

    def receiveBin(self) -> bytes:
        id, buffer = self.receiveProtocol()
        if id == ProtocolCode.FILE:
            self.sendString(ProtocolCode.OK, 'OK')
        elif id == ProtocolCode.ERRO:
            msg_erro = f'Error Recive bin: {buffer.decode("UTF-8")}'
            self.sendErro(msg_erro)
            raise ExceptionZero(msg_erro)       

        return buffer

    def receiveFile(self, path_file_name : str) -> int:
        """[Receive a file from host connected]
        Args:
            path_file_name (str): [path to save a file]
        Raises:
            ExceptionZero: [Fail to create a dir]
            Exception: [Fail to save a file]
            Exception: [Receive a unspected command]
        Returns:
            int: [description]
        """
        id, buffer_arquivo = self.receiveProtocol()

        path, file_name = os.path.split(path_file_name)
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError as e:
            msg_erro = f'Error mkdir:{path_file_name} Erro:{str(e)}'
            self.sendErro(msg_erro)
            raise ExceptionZero(msg_erro)

        if id == ProtocolCode.FILE:
            try:
                with open(path_file_name, mode='wb') as file:
                    #file.write(bytes(int(x, 0) for x in buffer_arquivo))
                    file.write(buffer_arquivo)
                    self.sendString(ProtocolCode.OK, 'OK')
                    return len(buffer_arquivo)

            except Exception as exp:
                msg_erro = 'Erro ao gravar arquivo:{0} Erro:{1}'.format(path_file_name, str(exp))
                self.sendErro(msg_erro)
                raise Exception(msg_erro)

        else:
            msg_erro = 'Nao recebi o arquivo:{0} Erro ID:{1}'.format(path_file_name, str(id))
            self.sendErro(msg_erro)
            raise Exception(msg_erro)
