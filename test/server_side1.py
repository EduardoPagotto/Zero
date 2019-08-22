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
import socket

import common_side1

sys.path.append('../Zero')

from Zero.UnixDomainServer import UnixDomainServer
from Zero.Protocol import Protocol, ProtocolCode
from Zero.ServerService import ServerService

from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose, ExceptionZeroErro
from Zero.subsys.GracefulKiller import GracefulKiller

def connection(args, kwargs):

    logging.info('connection stated')

    done = kwargs['done']
    protocol = None
    try:
        protocol = Protocol(kwargs['clientsocket'])
        protocol.settimeout(10)
        
    except Exception as exp:
        logging.exception('falha na parametrizacao da conexao: {0}'.format(str(exp)))
        return

    while True:
        try:
            idRec, msg = protocol.receiveString()
            if idRec is ProtocolCode.COMMAND:

                # comando_str = msg.replace("'", "\"")
                # comando_dic = json.loads(comando_str)
                # comando = comando_dic['comando']

                logging.info('Comando Recebido:{0}'.format(msg))

                if msg == 'ola 123':
                    protocol.sendString(ProtocolCode.RESULT, 'echo: {0}'.format(msg))
                else:
                    protocol.sendString(ProtocolCode.RESULT, 'teste 2')

        except ExceptionZeroErro as exp_erro:
            logging.debug('recevice Erro: {0}'.format(str(exp_erro)))
            protocol.sendString(ProtocolCode.RESULT,'recived error from server')

        except ExceptionZeroClose as exp_close:
            logging.debug('receive Close: {0}'.format(str(exp_close)))
            break

        except socket.timeout:
            logging.debug('connection timeout..')

        except Exception as exp:
            logging.error('error: {0}'.format(str(exp)))
            break

        if done is True:
            protocol.close()
            break

    logging.info('connection finished')


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    killer = GracefulKiller()

    server = UnixDomainServer(common_side1.uds_target)
    server.settimeout(10)
    logging.debug('server timeout: %s',str(server.gettimeout()))

    service = ServerService(server.getSocket(), connection)

    service.start()

    cycle = 0
    while True:
        
        logging.info('cycle:%d connections:%d', cycle, len(service.lista))
        cycle += 1
        time.sleep(1)

        if killer.kill_now is True:
            server.close()
            service.stop()  
            break

    service.join()
