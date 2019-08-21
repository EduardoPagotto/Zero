#!/usr/bin/env python3
'''
Created on 20170119
Update on 20190821
@author: Eduardo Pagotto
'''

import sys
import os
import time
import threading
import logging

import common_acess

sys.path.append('../Zero')

from Zero.SocketBase import SocketBase
from Zero.UnixDomainSocketServer import UnixDomainServer, UnixDomainClient
from Zero.Protocol import Protocol, ProtocolCode

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',
    )

    try:

        protocol = Protocol()
        protocol.setSocket(UnixDomainClient(common_acess.uds_target).getSocket())

        protocol.sendString(ProtocolCode.COMMAND, 'ola 123')

        id, msg = protocol.receiveString()
        logging.info('Recebido id:{0} msg:{1}'.format(id, msg))

        protocol.sendString(ProtocolCode.COMMAND, 'Teste 1234567890......')

        id, msg = protocol.receiveString()
        logging.info('Recebido id:{0} msg:{1}'.format(id, msg))


        #idRec, msg = protocol.receiveString()
        #logging.info('Val %s', msg)

        #time.sleep(15)
        protocol.sendClose('Bye')

        logging.info('Desconectado')

    except Exception as exp:
        logging.exception('Falha {0}'.format(str(exp)))

    logging.info('App desconectado')