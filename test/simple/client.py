#!/usr/bin/env python3
'''
Created on 20170119
Update on 20200725
@author: Eduardo Pagotto
'''

import time
import logging
import common

from Zero import TransportKind, SocketFactory
from Zero import Protocol, ProtocolCode

def main():

    log = logging.getLogger('Client')
    logging.getLogger('Zero').setLevel(logging.INFO)

    try:
        #protocol = Protocol(transportClient(TransportKind.NETWORK, common.ip_target).getSocket())
        protocol = Protocol(transportClient(SocketFactory(TransportKind.UNIX_DOMAIN, common.uds_target)).getSocket())

        log.info(protocol.handShake())

        protocol.sendString(ProtocolCode.COMMAND, 'ola 123')
        id, msg = protocol.receiveString()
        log.info('Recebido id:%d msg:%s', id, msg)

        time.sleep(15)

        protocol.sendString(ProtocolCode.ERRO, 'Erro Critico')
        id, msg = protocol.receiveString()
        log.info('Recebido id:%d msg:%s', id, msg)

        protocol.sendClose('Bye-Bye')

        log.info('Desconectado')

    except Exception as exp:
        log.exception('Falha %s', str(exp))

    log.info('App desconectado')

if __name__ == '__main__':

    common.enable_log()

    main()
