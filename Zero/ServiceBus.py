'''
Created on 20190822
Update on 20190912
@author: Eduardo Pagotto
'''

import logging

from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose
from Zero.transport.Transport import transportClient, TransportKind
from Zero.transport.Protocol import Protocol, ProtocolCode
from Zero.ProxyObject import ProxyObject

class ServiceBus(object):
    def __init__(self):
        self.object_path = None
        self.protocol = None
        self.log = logging.getLogger('Zero.RPC')

    def getObject(self, object_path):
        
        self.object_path = object_path
        try:
            self.protocol = Protocol(transportClient(TransportKind.UNIX_DOMAIN, object_path).getSocket()) 
        except Exception: 
            raise ExceptionZero('ServiceUnknown: %s', str(object_path))

        return ProxyObject(self.protocol)

    # def __del__(self):
    #     self.protocol.sendClose('bye')


       