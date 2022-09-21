#!/usr/bin/env python3
'''
Created on 20170119
Update on 20220921
@author: Eduardo Pagotto
'''

import time
import logging
import common

from src import SocketFactoryClient
from src import Protocol, ProtocolCode

def main():

    log = logging.getLogger('Client')
    logging.getLogger('Zero').setLevel(logging.INFO)

    try:
        protocol = Protocol(SocketFactoryClient(common.ADDRESS).create_socket().getSocket())

        log.info(protocol.handShake())

        protocol.sendString(ProtocolCode.COMMAND, 'ola 123')
        idval, msg = protocol.receiveString()
        log.info('Recebido id:%s msg:%s', str(idval), msg)

        time.sleep(5)

        protocol.sendString(ProtocolCode.ERRO, 'Erro Critico')
        idVal, msg = protocol.receiveString()
        log.info('Recebido id:%s msg:%s', idVal, msg)

        protocol.sendClose('Bye-Bye')

        log.info('Desconectado')

    except Exception as exp:
        log.exception('Falha %s', str(exp))

    log.info('App desconectado')

if __name__ == '__main__':

    common.enable_log()

    main()
