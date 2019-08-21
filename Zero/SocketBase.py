#!/usr/bin/env python3
'''
Created on 20170119
Update on 20190819
@author: Eduardo Pagotto
'''

import socket

BLOCK_SIZE = 2048

class SocketBase(object):
    def __init__(self):
        self._sock = None

    def getSocket(self):
        '''Retorna o socket atual'''
        return self._sock

    def setSocket(self, socketIn):
        '''Vincula um socket ja criado'''
        self._sock = socketIn

    def set_time_out(self, time_out=300):
        '''Define o To da conexao para sistemas bloquantes'''
        self._sock.settimeout(time_out)

    def close(self):
        '''Encerra conexa e invalida socket'''
        if (self._sock is not None) and (self._sock.socket is not None):
            self._sock.close()
            self._sock = None

    def isConnected(self):
        '''True se conectado'''
        if (self._sock is not None) and (self._sock.socket is not None):
            return True 
        
        return False

    def connect(self, conexao):
        self._sock.connect(conexao)

    def sendBlocks(self, _buffer):
        '''Envia blocos de dados ao Socket'''
        total_enviado = 0
        total_buffer = len(_buffer)
        while total_enviado < total_buffer:
            tam = total_buffer - total_enviado
            if tam > BLOCK_SIZE:
                tam = BLOCK_SIZE

            inicio = total_enviado
            fim = total_enviado + tam

            sub_buffer = bytearray(_buffer[inicio:fim])
            sent = self._sock.send(sub_buffer)
            if sent == 0:
                raise Exception("Fail Send")

            #os.write(self.io, sub_buffer)
            total_enviado = fim

        return total_enviado

    def receiveBlocks(self, _tamanho):
        '''Recebe dados em forma de blocos no Socket'''
        total_recebido = 0
        buffer_local = []

        while total_recebido < _tamanho:
            tam = _tamanho - total_recebido
            if tam > BLOCK_SIZE:
                tam = BLOCK_SIZE

            #buffer_local += os.read(self.io, tam)
            chunk = self._sock.recv(tam)
            if chunk == b'':
                raise Exception("Fail Receive")

            buffer_local += chunk

            total_recebido = len(buffer_local)

        return buffer_local