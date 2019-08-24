'''
Created on 20190824
Update on 20190824
@author: Eduardo Pagotto
'''

import logging
import socket
import json

from Zero.transport.Protocol import Protocol, ProtocolCode
from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose, ExceptionZeroErro

class RPC_Responser(object):
    def __init__(self, target):
        self.log = logging.getLogger('Zero.Con')
        self.target = target


    def decodeCommand(self, msg):

        # comando_str = msg.replace("'", "\"")
        # comando_dic = json.loads(comando_str)
        # comando = comando_dic['comando']
        dados = json.loads(msg)

        return dados



    def __call__(self, *args, **kargs):

        self.log.info('RPC Response stated num: %d', args[0])

        dados_conexao = args[1]

        done = dados_conexao['done']
        protocol = None
        try:
            protocol = Protocol(dados_conexao['clientsocket'])
            protocol.settimeout(30)
            
        except Exception as exp:
            self.log.exception('falha na parametrizacao da conexao: {0}'.format(str(exp)))
            return

        while True:
            try:
                idRec, msg = protocol.receiveString()
                if idRec is ProtocolCode.COMMAND:

                    self.log.debug('Comando Recebido:{0}'.format(msg))

                    dados = self.decodeCommand(msg)
                    logging.debug('Teste: %s', str(dados))
                
                    metodo = dados['method']
                    parametro = dados['params'][0]

                    val = getattr(self.target, metodo)(parametro)

                    logging.debug('Teste: %s', str(val))

                    protocol.sendString(ProtocolCode.RESULT, 'echo: {0}'.format(msg))


            except ExceptionZeroErro as exp_erro:
                self.log.warning('recevice Erro: {0}'.format(str(exp_erro)))
                protocol.sendString(ProtocolCode.RESULT,'recived error from server')

            except ExceptionZeroClose as exp_close:
                self.log.debug('receive Close: {0}'.format(str(exp_close)))
                break

            except socket.timeout:
                self.log.debug('connection timeout..')

            except Exception as exp:
                self.log.error('error: {0}'.format(str(exp)))
                break

            if done is True:
                protocol.close()
                break

        self.log.info('RPC Response finished')