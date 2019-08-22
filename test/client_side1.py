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

from Zero.SocketBase import SocketBase
from Zero.UnixDomainClient import UnixDomainClient, NetworkClient
from Zero.Protocol import Protocol, ProtocolCode

from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    try:
        protocol = Protocol(NetworkClient(common_side1.ip_target).getSocket())
        #protocol = Protocol(UnixDomainClient(common_side1.uds_target).getSocket())
       
        logging.debug(protocol.handShake())

        protocol.sendString(ProtocolCode.COMMAND, 'ola 123')
        id, msg = protocol.receiveString()
        logging.info('Recebido id:{0} msg:{1}'.format(id, msg))

        time.sleep(15)

        protocol.sendString(ProtocolCode.ERRO, 'Erro Critico')
        id, msg = protocol.receiveString()
        logging.info('Recebido id:{0} msg:{1}'.format(id, msg))

        protocol.sendClose('Bye-Bye')

        logging.info('Desconectado')

    except Exception as exp:
        logging.exception('Falha {0}'.format(str(exp)))

    logging.info('App desconectado')