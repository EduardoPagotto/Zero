#!/usr/bin/env python3
'''
Created on 20190822
Update on 20210212
@author: Eduardo Pagotto
'''

import time
import logging

from .transport import SocketFactoryServer
from .subsys import GracefulKiller
from .ServiceServer import ServiceServer
from .RPC_Responser import RPC_Responser

class ServiceObject(object):

    def __init__(self, s_address : str, target : object):
        """[Start Server RPC]
        Args:
            s_address (str): [valids: unix:./conexao_peer amd tcp:s//127.0.0.1:5151]
            target (object): [Self of derivade class]
        """

        self.done = False
        self.log = logging.getLogger('Zero.RPC')

        self.server =  SocketFactoryServer(s_address).create_socket() # TODO encapsular em ServiceServer ??
        self.server.settimeout(10)

        self.service = ServiceServer(self.server.getSocket(), RPC_Responser(target)) # servicos diferentes do RPC trocar esta classe
        self.service.start()


    def rpc_call(self, identicador, input=None, output=None):
        def decorator(func):
            def wrapper(self, *args, **kwargs):

                self.log.debug('RPC identificador:%s In:%s Out:%s args:%s, kwargs:%s', identicador, str(input), str(output), str(args), str(kwargs))

                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    def join(self) -> None:
        """[Wait until all connections be closed]
        """
        self.service.join()
        self.log.info('service object down')

    def stop(self) -> None:
        """[Signal to stop]
        """
        if self.done is False:
            self.log.info('service object signal shutting down.....')
            self.server.close()
            self.service.stop()

            self.done = True

    def loop_blocked(self, killer:GracefulKiller) -> None:
        try:
            self.log.info("Service RPC start")

            while self.done is False:

                if killer.kill_now is True:
                    self.stop()

                self.service.garbage()
                time.sleep(5)

            self.join()
            self.log.info("Service RPC stop after %d connections", self.service.total)

        except Exception as exp:
            self.log.critical('Fail: %s', str(exp))
