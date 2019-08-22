#!/usr/bin/env python3
'''
Created on 20190822
Update on 20190822
@author: Eduardo Pagotto
'''

import sys
import os
import time
import threading
import logging
import socket

from Zero.transport.Protocol import Protocol, ProtocolCode
from Zero.transport.Transport import transportServer, TransportKind
from Zero.ServiceServer import ServiceServer
from Zero.ConObject import connection

from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose, ExceptionZeroErro
from Zero.subsys.GracefulKiller import GracefulKiller

class ServiceObject(object):
    def __init__(self, device_bus,  object_path):
        
        self.done = False
        self.log = logging.getLogger('Zero')

        self.server = transportServer(TransportKind.UNIX_DOMAIN, object_path)
        self.server.settimeout(10)
    
        self.service = ServiceServer(self.server.getSocket(), connection)
        self.service.start()

        self.t_guardian = threading.Thread(target=self.__guardian, name='guardian_conn')
        self.t_guardian.start()
        
    def join(self):
        self.service.join()
        self.t_guardian.join()
        self.log.info('service server down')

    def stop(self):
        self.log.info('service server shutting down.....')
        self.done = True

    def __guardian(self):
        cycle = 0
        while True:
            
            self.log.debug('cycle:%d connections:%d', cycle, len(self.service.lista))
            cycle += 1
            time.sleep(5)

            if self.done is True:
                self.server.close()
                self.service.stop()  
                break
