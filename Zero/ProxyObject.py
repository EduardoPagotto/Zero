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

# class RPC_CALL(object):
#     def __init__(self, nome_metodo):
#         self.nome_metodo = nome_metodo

#     def __call__(self, *args, **kargs):

#         if self.nome_metodo == 'setNames':
#             execute = 'comando:{0} parametros:{1}'.format(self.nome_metodo, str(args)) 
#             return execute

#         raise AttributeError()

# class ProxyObject(object):
#     def __init__(self):
#         pass

#     # chama uma classe como metodo do call
#     def __getattr__(self, name):
#         return RPC_CALL(name)

#     # cria um atributo novo
#     def __setattr__(self, name, value):
#         self.__dict__[name] = value

# if __name__ == '__main__':
    
#     g = ProxyObject()
#     print(g.setNames('nome', 'dados'))
#     print(g.teste())