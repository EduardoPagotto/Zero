'''
Created on 20190824
Update on 20200725
@author: Eduardo Pagotto
'''

import logging
import socket

from Zero.transport.Protocol import Protocol, ProtocolCode
from Zero.subsys.ExceptionZero import ExceptionZeroClose, ExceptionZeroErro

from Zero.RPC_Call import RPC_Result

class RPC_Responser(object):
    """[Connection thread with server RPC ]
    Args:
        object ([type]): [description]
    """

    def __init__(self, target : object):
        """[summary]
        Args:
            target (object): [Method Name to run in RPC Server]
        """
        self.log = logging.getLogger('Zero.RPC')
        self.target : object= target

    def __call__(self, *args, **kargs):
        """[execute exchange of json's messages with server RPC]
        """

        self.log.info('RPC Response start num: %d', args[0])

        dados_conexao = args[1]

        indice_conexao = args[0]

        done = dados_conexao['done']
        protocol = None
        try:
            protocol = Protocol(dados_conexao['clientsocket'])
            protocol.settimeout(30)

        except Exception as exp:
            self.log.exception('falha na parametrizacao da conexao: %s', str(exp))
            return

        count_to = 0

        while True:
            try:
                idRec, msg_in = protocol.receiveString()

                count_to = 0

                if idRec is ProtocolCode.COMMAND:

                    msg_out = RPC_Result(self.target, msg_in)
                    protocol.sendString(ProtocolCode.RESULT, msg_out)

            except ExceptionZeroErro as exp_erro:
                self.log.warning('recevice Erro: %s', str(exp_erro))
                protocol.sendString(ProtocolCode.RESULT, 'recived error from server')

            except ExceptionZeroClose as exp_close:
                self.log.debug('receive Close: %s', str(exp_close))
                break

            except socket.timeout:
                count_to += 1
                self.log.debug('connection %d timeout %d ..', indice_conexao, count_to)

            except Exception as exp:
                self.log.error('error: %s', str(exp))
                break

            if done is True:
                protocol.close()
                break

        self.log.info('RPC Response finished')
