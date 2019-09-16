#!/usr/bin/env python3
'''
Created on 20190822
Update on 20190904
@author: Eduardo Pagotto
'''

import logging
import time

import sys
sys.path.append('../Zero')

import common_rpc as rpc

from Zero.subsys.GracefulKiller import GracefulKiller
from Zero.ServiceObject import ServiceObject
from Zero.subsys.ExceptionZero import ExceptionZeroRPC

class ServerRPC(ServiceObject):
    def __init__(self):
        device_bus = ''
        self.vivo = True
        self.nome = ''
        self.log = logging.getLogger('Server')
        super().__init__(device_bus, rpc.BUS_PATH, self)

    def teste_targuet(self, entrada):
        self.log.debug('ESTOU CHEGANDO JEANY!!!!')

        if entrada == 0:
            raise Exception('teste 0 ...')
        elif entrada == 1:
            raise ExceptionZeroRPC()
        elif entrada == 2:
            raise ExceptionZeroRPC('teste 2 ...')
        elif entrada == 3:
            raise ExceptionZeroRPC('teste 3 ...', -32099)

        return False

    @ServiceObject.rpc_call(rpc.IS_ALIVE_INTERFACE, input=(), output=('b',))
    def is_alive_bitch(self):
        return self.vivo  

    @ServiceObject.rpc_call(rpc.SET_NOME_INTERFACE, input=('s',), output=())
    def setNome(self, nome):
        self.nome = nome

    @ServiceObject.rpc_call(rpc.GET_NOME_INTERFACE, input=(''), output=('s',))
    def getNome(self):
        return self.nome

    @ServiceObject.rpc_call(rpc.GET_DICIONARIO_INTERFACE, input=('d',), output=('d'))
    def get_dict(self, dicionario):
        dicionario['novo'] = 'ola'
        return dicionario

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    server = ServerRPC()
    server.loop_blocked()
