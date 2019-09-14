'''
Created on 20190914
Update on 20190914
@author: Eduardo Pagotto
'''

import time
import logging
import threading

from datetime import datetime, timedelta

from Zero.subsys.ExceptionZero import ExceptionZeroRPC
from Zero.subsys.GracefulKiller import GracefulKiller
from Zero.transport.Transport import transportClient, TransportKind
from Zero.transport.Protocol import Protocol

class ConnectionData(object):

    serial = 0

    def __init__(self, data_conn, max):
        
        self.id = ConnectionData.serial
        self.connection = None
        self.time = None
        self.log = logging.getLogger('Zero.RPC')

        contador = 0
        while contador < max:
            try:
                self.connection =  Protocol(transportClient(TransportKind.UNIX_DOMAIN, data_conn).getSocket())
                ConnectionData.serial += 1

                self.log.debug('New connection id: %d peer: %s OK',self.id, str(data_conn))
                return
            except Exception:
                self.log.debug('New connection peer %s fail (%d/%d)',str(data_conn), contador+1, max)
                time.sleep(2)
                contador += 1

        raise ExceptionZeroRPC('New connection peer {0} erro'.format(str(data_conn)))
                
    def update(self):
        self.time = datetime.now()

class ConnectionControl(object):
    def __init__(self, data_conn, max):
        self.data_conn = data_conn
        self.max = max
        self.done = False
        self.lines_free = []
        self.log = logging.getLogger('Zero.RPC')
        self.mutex_free = threading.Lock()

        self.t_cleanner = threading.Thread(target=self.cleanner, name='cleanner_conn')
        self.t_cleanner.start()

    def get_connection(self):
        with self.mutex_free:
            return self.lines_free.pop() if len(self.lines_free) > 0 else ConnectionData(self.data_conn, self.max)

    def release_connection(self, line_comm):
        with self.mutex_free:
            line_comm.update()
            self.lines_free.append(line_comm)

    def stop(self):
        self.done = True

    def join(self):
        self.t_cleanner.join()

    def cleanner(self):

        self.log.debug('cleanner_conn start')
        while self.done is False:
            
            try:
                now = datetime.now()
                with self.mutex_free:
                    if len(self.lines_free) > 0:
                        elapse = self.lines_free[0].time + timedelta(minutes=1)
                        while (now > elapse) and (len(self.lines_free) > 0):
                            comm = self.lines_free.pop(0)
                            self.log.debug('close id: %d', comm.id)
                            comm.connection.sendClose('bye')
                            comm = None

            except Exception as exp:
                self.log.Exception('cleanner_conn falha critica: %s', str(exp))

            time.sleep(5)

        self.log.debug('cleanner_conn stopping...')

        while len(self.lines_free) > 0:
            comm = self.lines_free.pop()
            self.log.debug('Shutdown close id: %d', comm.id)
            comm.connection.sendClose('bye')
            comm = None

        self.log.debug('cleanner_conn down')