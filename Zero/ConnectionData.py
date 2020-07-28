'''
Created on 20200727
Update on 20200727
@author: Eduardo Pagotto
'''

import logging

from typing import Union, Any
from datetime import datetime

from Zero.transport.Protocol import Protocol
from Zero.transport.SocketFactory import SocketFactoryClient

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