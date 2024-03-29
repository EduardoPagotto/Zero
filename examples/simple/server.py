#!/usr/bin/env python3
'''
Created on 20170119
Update on 20220921
@author: Eduardo Pagotto
'''

import time
import logging
import socket

import common

from Zero import Protocol, ProtocolCode, SocketFactoryServer
from Zero import ServiceServer, ExceptionZeroClose, ExceptionZeroErro, GracefulKiller

def connection(args, kwargs):

    log = logging.getLogger('Zero.Con')

    log.info('connection stated')

    done = kwargs['done']
    protocol = None
    try:
        protocol = Protocol(kwargs['clientsocket'])
        protocol.settimeout(10)

    except Exception as exp:
        log.exception('falha na parametrizacao da conexao: {0}'.format(str(exp)))
        return

    while True:
        try:
            idRec, msg = protocol.receiveString()
            if idRec is ProtocolCode.COMMAND:

                # comando_str = msg.replace("'", "\"")
                # comando_dic = json.loads(comando_str)
                # comando = comando_dic['comando']

                log.debug('Comando Recebido:{0}'.format(msg))

                if msg == 'ola 123':
                    protocol.sendString(ProtocolCode.RESULT, 'echo: {0}'.format(msg))
                else:
                    protocol.sendString(ProtocolCode.RESULT, 'teste 2')

        except ExceptionZeroErro as exp_erro:
            log.warning('recevice Erro: {0}'.format(str(exp_erro)))
            protocol.sendString(ProtocolCode.RESULT, 'recived error from server')

        except ExceptionZeroClose as exp_close:
            log.debug('receive Close: {0}'.format(str(exp_close)))
            break

        except socket.timeout:
            log.debug('connection timeout..')

        except Exception as exp:
            log.error('error: {0}'.format(str(exp)))
            break

        if done is True:
            protocol.close()
            break

    log.info('connection finished')

def main():

    log = logging.getLogger('Server')
    logging.getLogger('Zero').setLevel(logging.INFO)

    killer = GracefulKiller()

    server = SocketFactoryServer(common.ADDRESS).create_socket()
    server.settimeout(10)

    log.debug('server timeout: %s', str(server.gettimeout()))

    service = ServiceServer(server.getSocket(), connection)

    service.start()

    cycle = 0
    while True:

        log.info('cycle:%d connections:%d', cycle, len(service.lista))
        cycle += 1
        time.sleep(5)

        if killer.kill_now is True:
            server.close()
            service.stop()
            break

    service.join()

if __name__ == '__main__':

    common.enable_log()

    main()
