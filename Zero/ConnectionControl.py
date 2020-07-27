'''
Created on 20190914
Update on 20200727
@author: Eduardo Pagotto
'''

import time
import logging
import threading

from typing import List, Union, Any
from datetime import datetime, timedelta

from Zero.transport.SocketFactory import SocketFactoryClient
from Zero.transport.Protocol import Protocol

class ConnectionData(object):
    """[Connection with server RPC]
    Args:
        object ([type]): [description]
    """
    serial : int = 0

    def __init__(self, factory : SocketFactoryClient):
        """[Constructor Connection]
        Args:
            factory (SocketFactoryClient): [Connection data]
        """
        self.id : int = ConnectionData.serial
        self.connection : Union[Protocol, Any] = None
        self.last_update = datetime.now()
        self.log = logging.getLogger('Zero.RPC')
        self.connection = Protocol(factory.create_socket().getSocket())

    def update(self) -> None:
        """[update last used]
        """
        self.last_update = datetime.now()

class ConnectionControl(object):
    """[Manager Connecton pool]
    Args:
        object ([type]): [description]
    """

    def __init__(self, factory : SocketFactoryClient, max_threads : int):
        """[summary]
        Args:
            factory (SocketFactoryClient): [Conection data]
            max_threads (int): [num max of cooncurrency]
        """

        self.factory = factory

        self.done :bool = False
        self.lines_free : List[ConnectionData]= []
        self.log = logging.getLogger('Zero.RPC')
        self.mutex_free : threading.Lock = threading.Lock()
        self.semaphore : threading.Semaphore = threading.Semaphore(max_threads)
        self.t_cleanner : threading.Thread = threading.Thread(target=self.cleanner, name='cleanner_conn')
        self.t_cleanner.start()

    def get_connection(self) -> ConnectionData:
        """[Get Next avaible connection or create one if has free slot]
        Returns:
            ConnectionData: [Connection free from list or new connection if is avaible]
        """

        self.semaphore.acquire()
        with self.mutex_free:
            return self.lines_free.pop() if len(self.lines_free) > 0 else ConnectionData(self.factory)

    def release_connection(self, line_comm : ConnectionData) -> None:
        """[Release connectiom no more used ]
        Args:
            line_comm (ConnectionData): [Connection with server RPC]
        """
        with self.mutex_free:
            line_comm.update()
            self.lines_free.append(line_comm)

        self.semaphore.release()

    def stop(self) -> None:
        """[signal to stop all]
        """
        self.done = True

    def join(self) -> None:
        """[wait until cleaner has finished]
        """
        self.t_cleanner.join()

    def cleanner(self) ->None:
        """[Garbage collector of connections elapsed]
        """

        self.log.debug('cleanner_conn start')
        while self.done is False:

            try:
                now = datetime.now()
                with self.mutex_free:
                    if len(self.lines_free) > 0:
                        elapse = self.lines_free[0].last_update + timedelta(minutes=1)
                        while (now > elapse) and (len(self.lines_free) > 0):
                            comm = self.lines_free.pop(0)
                            self.log.debug('close id: %d', comm.id)
                            comm.connection.sendClose('bye')
                            del comm #comm = None

            except Exception as exp:
                self.log.error('cleanner_conn falha critica: %s', str(exp))

            time.sleep(5)

        self.log.debug('cleanner_conn stopping...')

        while len(self.lines_free) > 0:
            comm = self.lines_free.pop()
            self.log.debug('Shutdown close id: %d', comm.id)
            comm.connection.sendClose('bye')
            del comm #comm = None

        self.log.debug('cleanner_conn down')
