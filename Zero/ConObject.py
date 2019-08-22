'''
Created on 20190822
Update on 20190822
@author: Eduardo Pagotto
'''

import logging
import socket

from Zero.transport.Protocol import Protocol, ProtocolCode
from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose, ExceptionZeroErro

def connection(args, kwargs):

    log = logging.getLogger('Zero.Con')
    log.info('connection stated')

    done = kwargs['done']
    protocol = None
    try:
        protocol = Protocol(kwargs['clientsocket'])
        protocol.settimeout(30)
        
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
            protocol.sendString(ProtocolCode.RESULT,'recived error from server')

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