'''
Created on 20200727
Update on 20200728
@author: Eduardo Pagotto
'''

import logging
import threading

from typing import Union, Any
from datetime import datetime, timedelta

from Zero.transport.Protocol import Protocol
from Zero.transport.SocketFactory import SocketFactoryClient

class ConnectionData(object):
    """[Connection with server RPC]
    Args:
        object ([type]): [description]
    """
    serial : int = 0
    mutex_serial : threading.Lock = threading.Lock()


    def __init__(self, factory : SocketFactoryClient):
        """[Constructor Connection]
        Args:
            factory (SocketFactoryClient): [Connection data]
        """
        with ConnectionData.mutex_serial:
            self.id : int = ConnectionData.serial
            ConnectionData.serial += 1

        self.connection : Union[Protocol, Any] = None
        self.last_update = datetime.now()
        self.log = logging.getLogger('Zero.RPC')
        self.connection = Protocol(factory.create_socket().getSocket())

    def update(self) -> None:
        """[update last used]
        """
        self.last_update = datetime.now()

    def is_elapsed_connection(self, time_delta : timedelta) -> bool:
        """[Test if connection elapsed, if yes close with host]
        Args:
            time_delta (timedelta): [description]
        Returns:
            bool: [True if elapsed (closed in this funcion)
                   False if valid]
        """
        now = datetime.now()
        elapse = self.last_update + time_delta
        if now > elapse:
            self.disconnection()
            return True

        return False

    def disconnection(self) -> None:
        """[Close connection]
        """
        self.log.info('shutdown connection id: %d', self.id)
        self.connection.sendClose('bye connection id: {0}'.format(self.id))
