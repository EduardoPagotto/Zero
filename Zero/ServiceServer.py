#!/usr/bin/env python3
'''
Created on 20190822
Update on 20200727
@author: Eduardo Pagotto
'''

import time
import socket
import logging
import threading

from typing import List

from Zero.RPC_Responser import RPC_Responser

class ServiceServer(object):
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
        #self.t_garbage : threading.Thread = threading.Thread(target=self.garbageCon, name='garbage_conn')
        self.t_server : threading.Thread  = threading.Thread(target=self.builderConnection, name='factory_conn', args=(socket_server, serverConnection))
        self.log = logging.getLogger('Zero.RPC')

    def start(self) -> None:
        """[Start Server pooller connections]
        """
        self.log.info('service server start')
        #self.t_garbage.start()
        self.t_server.start()

    def join(self) -> None:
        """[Wait finisher all connections and clean all garbage]
        """
        self.t_server.join()
        #self.t_garbage.join()
        self.log.info('service server down')

    def stop(self) -> None:
        """[Signal to stop server]
        """
        self.log.info('service server shutting down.....')
        self.done = True

    # def garbageCon(self) -> None:
    #     """[Thread to remove connections deads]
    #     """
    #     self.log.info("garbage connections start")

    #     totais = 0
    #     while True:

    #         lista_remover = []
    #         for thread in self.lista:
    #             if thread.isAlive() is False:
    #                 self.log.info('thread removed %s, total removed: %d', thread.getName(), totais + 1)
    #                 totais += 1
    #                 thread.join()
    #                 lista_remover.append(thread)

    #         for thread in lista_remover:
    #             self.lista.remove(thread)

    #         if len(lista_remover) != 0:
    #             lista_remover.clear()

    #         if self.done is True:
    #             if len(self.lista) == 0:
    #                 break

    #         time.sleep(1)

    #     self.log.info("garbage connection stop after %d removed", totais)

    def builderConnection(self, sock : socket.socket, serverConnection: RPC_Responser):
        """[Thread factory of new connectons to client]
        Args:
            sock (socket.socket): [low severl socket]
            serverConnection (RPC_Responser): [responser json 2.0]
        """
        self.log.info("factory connections start")
        seq = 0

        while True:
            try:
                # accept connections from outside
                clientsocket, address = sock.accept()
                comm_param = {'clientsocket': clientsocket,
                              'addr' : address,
                              'done' : self.done}

                self.log.info("new connection :%s", str(address))

                t = threading.Thread(target=serverConnection, name='connection_{0}'.format(seq), args=(seq, comm_param))
                t.start()

                self.lista.append(t)

                seq += 1

            except socket.timeout:
                pass

            except Exception as exp:
                if self.done is False:
                    self.log.error('Fail:%s', str(exp))
                else:
                    break

        self.log.info("factory connection stop")
