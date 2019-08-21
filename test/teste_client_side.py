#!/usr/bin/env python3
'''
Created on 20170119
Update on 20190819
@author: Eduardo Pagotto
'''

import sys
import os
import time
import threading
import logging

from SocketBase import SocketBase
from UnixDomainSocketServer import UnixDomainServer, UnixDomainClient
from Protocol import Protocol, ProtocolCode


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',
    )

    try:

        protocol = Protocol()
        protocol.setSocket(UnixDomainClient('/home/pagotto/Projetos/Zeke/uds_socket_teste').getSocket())

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