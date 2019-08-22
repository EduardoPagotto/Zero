#!/usr/bin/env python3
'''
Created on 20190822
Update on 20190822
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

from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose, ExceptionZeroErro
from Zero.subsys.GracefulKiller import GracefulKiller

def connection(args, kwargs):

    log = logging.getLogger('Zero.Con')
    log.info('connection stated')

    # done = kwargs['done']
    # protocol = None
    # try:
    #     protocol = Protocol(kwargs['clientsocket'])
    #     protocol.settimeout(30)
        
    # except Exception as exp:
    #     log.exception('falha na parametrizacao da conexao: {0}'.format(str(exp)))
    #     return

    # while True:
    #     try:
    #         idRec, msg = protocol.receiveString()
    #         if idRec is ProtocolCode.COMMAND:

    #             # comando_str = msg.replace("'", "\"")
    #             # comando_dic = json.loads(comando_str)
    #             # comando = comando_dic['comando']

    #             log.debug('Comando Recebido:{0}'.format(msg))

    #             if msg == 'ola 123':
    #                 protocol.sendString(ProtocolCode.RESULT, 'echo: {0}'.format(msg))
    #             else:
    #                 protocol.sendString(ProtocolCode.RESULT, 'teste 2')

    #     except ExceptionZeroErro as exp_erro:
    #         log.warning('recevice Erro: {0}'.format(str(exp_erro)))
    #         protocol.sendString(ProtocolCode.RESULT,'recived error from server')

    #     except ExceptionZeroClose as exp_close:
    #         log.debug('receive Close: {0}'.format(str(exp_close)))
    #         break

    #     except socket.timeout:
    #         log.debug('connection timeout..')

    #     except Exception as exp:
    #         log.error('error: {0}'.format(str(exp)))
    #         break

    #     if done is True:
    #         protocol.close()
    #         break

    log.info('connection finished')

class ServiceObject(object):
    def __init__(self, device_bus,  object_path):
        
        self.done = False
        self.log = logging.getLogger('Zero')

        self.server = transportServer(TransportKind.UNIX_DOMAIN, object_path)
        self.server.settimeout(10)
    
        self.service = ServiceServer(self.server.getSocket(), connection)
        self.service.start()

        self.t_guardian = threading.Thread(target=self.__guardian, name='guardian_conn')
        self.t_guardian.start()
        
    def join(self):
        self.service.join()
        self.t_guardian.join()
        self.log.info('service server down')

    def stop(self):
        self.log.info('service server shutting down.....')
        self.done = True

    def __guardian(self):
        cycle = 0
        while True:
            
            self.log.debug('cycle:%d connections:%d', cycle, len(self.service.lista))
            cycle += 1
            time.sleep(5)

            if self.done is True:
                self.server.close()
                self.service.stop()  
                break
