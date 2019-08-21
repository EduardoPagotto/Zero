#!/usr/bin/env python3
'''
Created on 20170119
Update on 20190821
@author: Eduardo Pagotto
'''

import os
import errno
import struct
import zlib
import logging

from enum import Enum
from Zero.SocketBase import SocketBase

class ProtocolCode(Enum):
    '''Comandos Enviados pelo Protocolo'''
    OPEN = 1
    CLOSE = 2
    HANDSHAKE = 3
    COMMAND = 4
    OK = 5
    RESULT = 6
    FILE = 7
    ERRO = 255

class Protocol(SocketBase):
    '''Wrapper de servidor socket'''

    def __init__(self):
        SocketBase.__init__(self)
        self.protocol_versao = "0.0.1"
        # self.ipAddr = None

    # def connect(self, conexao):
    #     '''Establelece coneccao com o servidor'''
    #     logging.info('------>')
    #     logging.info('Cliente a conectar em %s:%d', conexao[0], conexao[1])

    #     try:
    #         Socket.connect(self, conexao)
    #     except OSError as msg:
    #         raise SubExceptionProtocol(ProtocolErro.CONNECT, 'Falha ao instanciar Socket:{0}'.format(print(msg)))

    #     self.sendHandShake()
    #     logging.info('Conectado.')

    def close(self):
        ''''Encerra a conexao local'''
        try:
            self.close()
        except:
            raise Exception('Falha no Close local')

    def sendProtocol(self, _id, _buffer):
        '''Envia um buffer com comando do Protocolo'''
        buffer_final = []

        tamanho_buffer = int(len(_buffer))
        comprimido = zlib.compress(_buffer)
        tamanho_comprimido = int(len(comprimido))
        crc = zlib.crc32(comprimido)

        headerTupleA = (_id.value, 0, 0, 0, tamanho_buffer, tamanho_comprimido, crc, 0, 0, 0)
        formatoHeaderA = struct.Struct('B B B B I I I I I I')
        headerA = formatoHeaderA.pack(*headerTupleA)
        buffer_final += headerA

        crc2 = zlib.crc32(headerA)
        headerCRC = struct.pack("I", crc2)
        buffer_final += headerCRC

        buffer_final += comprimido

        self.sendBlocks(buffer_final)

    def receiveProtocol(self):
        '''Recebe um comando ou dados do protocolo'''

        buffer_header = bytearray(self.receiveBlocks(32))

        formatoHeader = struct.Struct('B B B B I I I I I I I')
        headerTuple = formatoHeader.unpack(buffer_header)

        valInt = int(headerTuple[0])
        idRecebido = ProtocolCode(valInt)
        #res1 = headerTuple[1]
        #res2 = headerTuple[2]
        #res3 = headerTuple[3]
        tamanho_buffer = headerTuple[4]
        tamanho_comprimido = headerTuple[5]
        crc = headerTuple[6]
        crc2 = headerTuple[10]

        bufferHeader = buffer_header[:28]
        crcCalc2 = zlib.crc32(bufferHeader)
        if crc2 != crcCalc2:
            raise Exception('Protocol Receive Header CRC Erro')

        buffer_dados = bytearray(self.receiveBlocks(tamanho_comprimido))

        crcCalc = zlib.crc32(buffer_dados)

        if crc != crcCalc:
            raise Exception('Protocol Receive Payload CRC Erro')

        binario = zlib.decompress(buffer_dados)

        if len(binario) != tamanho_buffer:
            raise Exception('Protocol Receive size buffer error')

        if idRecebido == ProtocolCode.HANDSHAKE:
            msg = binario.decode('UTF-8')

            logging.info('HandShake, cliente:%s', msg)

            self.sendString(ProtocolCode.OK, self.protocol_versao)

        elif idRecebido == ProtocolCode.CLOSE:

            logging.info('Close recebido:%s', binario.decode('UTF-8'))

            self.close()
            #raise Exception('Protocol Close received:{0}'.format(binario.decode('UTF-8')))

        #elif idRecebido == ProtocolCode.ERRO:
        #    raise Exception('{0}'.format(binario.decode('UTF-8')))

        return (idRecebido, binario)

    def sendString(self, _id, _texto):
        '''Envida texto com id'''
        buffer = _texto.encode('UTF-8')
        return self.sendProtocol(_id, buffer)

    def receiveString(self):
        '''recebe texto com id'''
        buffer = self.receiveProtocol()

        if buffer[0] is not None:
            return(buffer[0], buffer[1].decode('UTF-8'))

        return buffer

    def sendErro(self, msg):
        '''Envia uma MSG de erro ao peer'''
        self.sendString(ProtocolCode.ERRO, msg)

    def sendClose(self, _texto):
        '''Envia o fechamento'''
        if self.isConnected is True:
            #logging.info('Close enviado ao cliente:%s', _texto)
            self.sendString(ProtocolCode.CLOSE, _texto)

    def sendHandShake(self):
        '''Envia Hand automatico'''
        self.sendString(ProtocolCode.HANDSHAKE, self.protocol_versao )
        idRecive, msg = self.receiveString()
        if idRecive is ProtocolCode.OK:
            logging.info('Conexao Servidor: %s', msg)

    def sendFile(self, path_file_name):
        '''Envia arquivo ao ponto'''
        fileContent = None
        tamanho_arquivo = 0
        try:
            with open(path_file_name, mode='rb') as file:
                fileContent = file.read()
                tamanho_arquivo = len(fileContent)
        except IOError as e:
            self.sendErro('Falha IO na leitura do arquivo:{0}'.format(str(e)))
            raise Exception('Protocolo Send File:{0}'.format(str(e)))
        except:
            msg_erro = 'Falha critica no arquivo:{0}'.format(str(path_file_name))
            self.sendErro(msg_erro)
            raise Exception('Protocolo Send File: {0} '.format(msg_erro))

        self.sendProtocol(ProtocolCode.FILE, fileContent)
        idRecebido, msg = self.receiveProtocol()

        if idRecebido is not ProtocolCode.OK or msg != 'OK':
            raise Exception('Protocolo Send Falha no ACK do arquivo:{0} Erro:{1}'.format(path_file_name, msg))

        return tamanho_arquivo

    def receiveFile(self, path_file_name):
        '''
        Recebe um arquivo no protocolo com nome passado
        '''
        id, buffer_arquivo = self.receiveProtocol()

        path, file_name = os.path.split(path_file_name)
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                msg_erro = 'Erro ao criar o diretorio:{0} Erro:{1}'.format(path_file_name, str(e))
                self.sendErro(msg_erro)
                raise Exception(msg_erro)

        if id == ProtocolCode.FILE:
            try:
                with open(path_file_name, mode='wb') as file:
                    file.write(bytes(int(x, 0) for x in buffer_arquivo))

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



#if __name__ == '__main__':
    # configure_logging('log/testez1.log')
    # logging.info('Ativado Teste')

    # try:

    #     protocol = NeoProtocol('testez1 v0.0.0')
    #     protocol.create()

    #     addr = ('VirtualDevPosixZ1', 1313)

    #     protocol.connect(addr)
    #     protocol.sendString(10, 'Teste 1234567890......')
    #     idRec, msg = protocol.receiveString()
    #     logging.info('Val %s', msg)

    #     time.sleep(15)
    #     protocol.sendClose('Bye')

    #     logging.info('Desconectado')

    # except NeoExceptionProtocol as exp:
    #     print('NeoExceptionProtocol {0}'.format(exp.msg))
    # except NeoExceptionSocket as exs:
    #     print('NeoExceptionSocket {0}'.format(exs.msg))
    # except Exception as exx:
    #     print('NeoExceptionSocket {0}'.format(exx.args))

    # logging.info('App desconectado')
