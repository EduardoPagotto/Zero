#!/usr/bin/env python3
'''
Created on 20190822
Update on 20200916
@author: Eduardo Pagotto
'''

import time
import socket
import logging
import threading

from datetime import datetime, timezone, timedelta
from typing import List

from Zero.RPC_Responser import RPC_Responser

class ServiceServer(object): # TODO: implementar chamada de thread em __call__
    """[Class facture new connections threads]
    Args:
        object ([type]): [description]
    """
    def __init__(self, socket_server : socket.socket, serverConnection : RPC_Responser):
        """[Initialize with socket and rresponser]
        Args:
            socket_server (socket.socket): [description]
            serverConnection (RPC_Responser): [description]
        """
        self.lista : List[threading.Thread]= []
        self.done :bool = False
        self.t_server : threading.Thread  = threading.Thread(target=self.createConn, name='factory_conn', args=(socket_server, serverConnection))
        self.log = logging.getLogger('Zero.RPC')

        self.total = 0
        self.anterior = 0
        self.startApp = datetime.timestamp(datetime.now(tz=timezone.utc))

    def start(self) -> None:
        """[Start Server pooller connections]
        """
        self.log.info('Service server start')
        self.t_server.start()

    def join(self) -> None:
        """[Wait finisher all connections and clean all garbage]
        """
        self.t_server.join()
        self.log.info('Service server down')

    def stop(self) -> None:
        """[Signal to stop server]
        """
        self.log.info('Service server shutting down.....')
        self.done = True

    def garbage(self) -> None:
        """[Thread to remove connections deads]
        """
        lista_remover = []
        for th in self.lista:
            if th.isAlive() is False:
                th.join()
                lista_remover.append(th)

        for th in lista_remover:
            self.log.debug('Thread removed %s', th.getName())
            self.lista.remove(th)

        removed = len(lista_remover)
        if removed > 0:
            self.total += removed
            lista_remover.clear()

        atual = len(self.lista)
        if (atual != self.anterior) or (removed > 0):
            self.anterior = atual

            time_online = int(datetime.timestamp(datetime.now(tz=timezone.utc)) - self.startApp)
            self.log.info('alive[%s] run[%d] sweeped[%d]', str(timedelta(seconds=time_online)), atual, self.total)

    def createConn(self, sock : socket.socket, serverConnection: RPC_Responser):
        """[Thread factory of new connectons to client]
        Args:
            sock (socket.socket): [low severl socket]
            serverConnection (RPC_Responser): [responser json 2.0]
        """
        self.log.info("Sevice Server factory connections start")
        seq = 0

        while self.done is False:
            try:
                # accept connections from outside
                clientsocket, address = sock.accept()
                comm_param = {'clientsocket': clientsocket,
                              'addr' : address,
                              'done' : self.done}

                #self.log.info("new connection :%s", str(address))

                t = threading.Thread(target=serverConnection, name='tConn_{0}'.format(seq), args=(seq, comm_param))
                t.start()

                self.lista.append(t)

                seq += 1

            except socket.timeout:
                pass

            except Exception as exp:
                if self.done is False:
                    self.log.error('Fail:%s', str(exp))

        self.log.info("Sevice Server factory connection stop")
