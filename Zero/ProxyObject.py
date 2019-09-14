'''
Created on 20190822
Update on 20190914
@author: Eduardo Pagotto
'''

from Zero.RPC_Call import RPC_Call

class ProxyObject(object):
    def __init__(self, conn_control):
        self.conn_control = conn_control

    def __getattr__(self, name):
        return RPC_Call(name, self.conn_control)

    # cria um atributo novo
    def __setattr__(self, name, value):
        self.__dict__[name] = value
