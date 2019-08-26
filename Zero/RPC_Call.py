'''
Created on 20190823
Update on 20190826
@author: Eduardo Pagotto
'''

#import logging
import json

from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose
from Zero.transport.Protocol import Protocol, ProtocolCode

from Zero.RPC_Protocol import RPC_ProtocolMethod

class RPC_Call(object):
    def __init__(self, nome_metodo, prot):
        self.protocol = prot
        self.rpc = RPC_ProtocolMethod(nome_metodo)
        #self.log = logging.getLogger('Zero')

    def __call__(self, *args, **kargs):

        msg_out = self.rpc.encode(args, kargs)
        msg_in = self.protocol.exchange(msg_out)
        return self.rpc.decode(msg_in)
