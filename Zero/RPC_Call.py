'''
Created on 20190823
Update on 20190823
@author: Eduardo Pagotto
'''

import logging
import json

from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose
from Zero.transport.Protocol import Protocol, ProtocolCode

class RPC_Call(object):
    def __init__(self, nome_metodo, prot):
        self.nome_metodo = nome_metodo
        self.protocol = prot
        self.log = logging.getLogger('Zero')

    def __exchange(self, entrada):

        self.log.debug('Enviado id:{0} msg:{1}'.format(ProtocolCode.COMMAND, entrada))

        self.protocol.sendString(ProtocolCode.COMMAND, entrada)
        id, msg = self.protocol.receiveString()
        
        self.log.debug('Recebido id:{0} msg:{1}'.format(id, msg))
        
        if id == ProtocolCode.RESULT:
            return msg

        raise ExceptionZero('Resposta invalida: (%d : %s)', id, msg)

    def __encodeCommand(self, *args, **kargs):

        comando = {}
        parametros = []
        keys = {}

        if args:
            for item in args[0]:
                parametros.append(item)

            keys=args[1]

        comando['method'] = self.nome_metodo
        comando['params'] = parametros
        comando['keys'] = keys

        return json.dumps(comando)

    def __decodeRes(self, json_msg):
        return json_msg



    def __call__(self, *args, **kargs):

        jmsg_out = self.__encodeCommand(args, kargs)
        jmsg_in = self.__exchange(jmsg_out)

        data = self.__decodeRes(jmsg_in)

        return data

        # if self.nome_metodo == 'setNames':
        #     execute = 'comando:{0} parametros:{1}'.format(self.nome_metodo, str(args)) 
        #     return execute

        #raise AttributeError()