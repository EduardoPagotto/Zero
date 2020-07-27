#!/usr/bin/env python3
'''
Created on 20190822
Update on 20200627
@author: Eduardo Pagotto
'''

import time
import threading
import logging

from Zero import SocketFactoryServer
from Zero import GracefulKiller
from Zero.ServiceServer import ServiceServer
from Zero.RPC_Responser import RPC_Responser

class ServiceObject(object):

    def __init__(self, s_address : str, target : object):
        """[Start Server RPC]
        Args:
            s_address (str): [valids: uds://./conexao_peer amd tcp:s//127.0.0.1:5151]
            target (object): [Self of derivade class]
        """

        self.done = False
        self.log = logging.getLogger('Zero.RPC')

        self.server =  SocketFactoryServer(s_address).create_socket() # TODO encapsular em ServiceServer ??
        self.server.settimeout(10)

        self.service = ServiceServer(self.server.getSocket(), RPC_Responser(target)) # servicos diferentes do RPC trocar esta classe
        self.service.start()

        self.t_guardian = threading.Thread(target=self.__guardian, name='guardian_conn')
        self.t_guardian.start()

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
        self.t_guardian.join()
        self.log.info('service object down')

    def stop(self) -> None:
        """[Signal to stop]
        """
        self.log.info('service object shutting down.....')
        self.done = True

    def __guardian(self) -> None:
        """[Log connections total and wait signal to shutdown]
        """
        cycle = 0
        anterior = 0
        while True:
            atual = len(self.service.lista)
            if atual != anterior:
                anterior = atual
                self.log.debug('cycle:%d connections:%d', cycle, atual)

            cycle += 1
            time.sleep(5)

            if self.done is True:
                self.server.close()
                self.service.stop()
                break

    def loop_blocked(self, killer:GracefulKiller=None) -> None:
        try:
            while self.done is False:
                time.sleep(5)
                if killer is not None:
                    if killer.kill_now is True:
                        self.stop()

            self.join()

        except Exception as exp:
            self.log.error('Falha Critica: %s', str(exp))
