'''
Created on 20190914
Update on 20200728
@author: Eduardo Pagotto
'''

import time
import logging
import threading

from typing import List, Union, Any
from datetime import datetime, timedelta

from Zero.transport.SocketFactory import SocketFactoryClient
from Zero.ConnectionData import ConnectionData

class ConnectionControl(object):
    """[Manager Connecton pool]
    Args:
        object ([type]): [description]
    """

    def __init__(self, factory : SocketFactoryClient, time_delta : timedelta, max_threads : int):
        """[summary]
        Args:
            factory (SocketFactoryClient): [Conection data]
            time_delta (timedelta): [delta time to ellapsed this connection if not used]
            max_threads (int): [num max of cooncurrency]
        """
        self.factory : SocketFactoryClient = factory
        self.time_delta : timedelta = time_delta
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
        self.log.info('thread cleanner_conn start')
        while self.done is False:
            try:
                with self.mutex_free:
                    for item in reversed(self.lines_free): # necessary interator fix!!!

                        if item.is_elapsed_connection(self.time_delta) is True:
                            self.lines_free.remove(item)
                            del item

            except Exception as exp:
                self.log.critical('cleanner_conn fail: %s', str(exp))

            time.sleep(5)

        self.log.info('cleanner_conn stopping...')
        while len(self.lines_free) > 0:
            comm = self.lines_free.pop()
            comm.disconnection()
            del comm

        self.log.info('thread cleanner_conn stop')
