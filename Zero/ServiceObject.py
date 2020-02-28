#!/usr/bin/env python3
'''
Created on 20190822
Update on 20190924
@author: Eduardo Pagotto
'''

import sys
import os
import time
import threading
import logging
import socket

from Zero.transport.Protocol import Protocol, ProtocolCode
from Zero.transport.Transport import transportServer, TransportKind
from Zero.ServiceServer import ServiceServer
from Zero.RPC_Responser import RPC_Responser


from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose, ExceptionZeroErro
from Zero.subsys.GracefulKiller import GracefulKiller

class ServiceObject(object):
    def __init__(self, transportKind,  address, target):
        
        self.done = False

        self.log = logging.getLogger('Zero.RPC')

        self.server = transportServer(transportKind, address)
        self.server.settimeout(10)
    
        self.service = ServiceServer(self.server.getSocket(), RPC_Responser(target)) # servicos diferentes do RPC trocar esta classe
        self.service.start()

        self.t_guardian = threading.Thread(target=self.__guardian, name='guardian_conn')
        self.t_guardian.start()

    def rpc_call(self, identicador, input=None, output=None):
        def decorator(func):
            def wrapper(self, *args, **kwargs):

                self.log.debug('RPC identificador:%s In:%s Out:%s args:%s, kwargs:%s', identicador, str(input), str(output), str(args), str(kwargs))

                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    def join(self):
        self.service.join()
        self.t_guardian.join()
        self.log.info('service object down')

    def stop(self):
        self.log.info('service object shutting down.....')
        self.done = True

    def __guardian(self):
        cycle = 0
        anterior = 0
        while True:
            atual = len(self.service.lista)
            if atual != anterior:
                anterior = atual
                self.log.debug('cycle:%d connections:%d', cycle, atual)

            cycle += 1
            time.sleep(5)

            if self.done is True:
                self.server.close()
                self.service.stop()  
                break

    def loop_blocked(self):
        try:
            killer = GracefulKiller()
            while True:
                time.sleep(1)
                if killer.kill_now is True:
                    self.stop()  
                    break

            self.join()

        except Exception as exp:
            self.log.Exception('Falha Critica: %s', str(exp))
