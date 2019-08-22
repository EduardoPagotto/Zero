'''
Created on 20190822
Update on 20190822
@author: Eduardo Pagotto
'''

import logging
from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose

from Zero.transport.Protocol import Protocol, ProtocolCode

class ProxyObject(object):
    def __init__(self, protocol):
        self.protocol = protocol
        self.log = logging.getLogger('Zero.RPC')

    def exchange(self, entrada):

        self.log.debug('Enviado id:{0} msg:{1}'.format(ProtocolCode.COMMAND, entrada))

        self.protocol.sendString(ProtocolCode.COMMAND, entrada)
        id, msg = self.protocol.receiveString()
        
        self.log.debug('Recebido id:{0} msg:{1}'.format(id, msg))
        
        if id == ProtocolCode.RESULT:
            return msg

        raise ExceptionZero('Resposta invalida: (%d : %s)', id, msg)