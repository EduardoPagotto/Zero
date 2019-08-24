'''
Created on 20190822
Update on 20190822
@author: Eduardo Pagotto
'''

from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose
from Zero.transport.Protocol import Protocol, ProtocolCode
from Zero.RPC_Call import RPC_Call

class ProxyObject(object):
    def __init__(self, protocol):
        self.protocol = protocol
        #self.log = logging.getLogger('Zero.RPC')

    # chama uma classe como metodo do call
    def __getattr__(self, name):
        return RPC_Call(name, self.protocol)

    # cria um atributo novo
    def __setattr__(self, name, value):
        self.__dict__[name] = value
