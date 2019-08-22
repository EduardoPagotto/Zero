#!/usr/bin/env python3
'''
Created on 20170119
Update on 20190822
@author: Eduardo Pagotto
'''

import sys
import os
import time
import threading
import logging

import common_side1

sys.path.append('../Zero')

from Zero.transport.SocketBase import SocketBase
from Zero.transport.Transport import transportClient, TransportKind
from Zero.transport.Protocol import Protocol, ProtocolCode

from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose

# class Bus(object):

#     def __init__(self, object_path):

#         #self.object_path = object_path
#         try:
#             self.protocol = Protocol(transportClient(TransportKind.UNIX_DOMAIN, object_path).getSocket()) 
#         except Exception: 
#             raise ExceptionZero('ServiceUnknown: %s', str(object_path))

#     def exchange(self, entrada):
#         pass

# def main():
#     log = logging.getLogger('Client')
#     bus = Bus(common_side1.uds_target)
#     log.info(str(bus))

def main():

    log = logging.getLogger('Client')
    logging.getLogger('Zero').setLevel(logging.INFO)

    try:
        #protocol = Protocol(transportClient(TransportKind.NETWORK, common_side1.ip_target).getSocket())
        protocol = Protocol(transportClient(TransportKind.UNIX_DOMAIN, common_side1.uds_target).getSocket()) 

        log.info(protocol.handShake())

        protocol.sendString(ProtocolCode.COMMAND, 'ola 123')
        id, msg = protocol.receiveString()
        log.info('Recebido id:{0} msg:{1}'.format(id, msg))

        time.sleep(15)

        protocol.sendString(ProtocolCode.ERRO, 'Erro Critico')
        id, msg = protocol.receiveString()
        log.info('Recebido id:{0} msg:{1}'.format(id, msg))

        protocol.sendClose('Bye-Bye')

        log.info('Desconectado')

    except Exception as exp:
        log.exception('Falha {0}'.format(str(exp)))

    log.info('App desconectado')

if __name__ == '__main__':

    common_side1.enable_log()

    main()
