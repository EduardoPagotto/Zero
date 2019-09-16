#!/usr/bin/env python3
'''
Created on 20190822
Update on 20190916
@author: Eduardo Pagotto
'''

import time
import socket
import logging
import threading

class ServiceServer(object):
    def __init__(self, socket_server, serverConnection):
        self.lista = []
        self.done = False
        self.t_garbage = threading.Thread(target=self.garbageCon, name='garbage_conn')
        self.t_server = threading.Thread(target=self.builderConnection, name='factory_conn', args=(socket_server, serverConnection))
        self.log = logging.getLogger('Zero.RPC')

    def start(self):
        self.log.info('service server start')
        self.t_garbage.start()
        self.t_server.start()

    def join(self):
        self.t_server.join()
        self.t_garbage.join()
        self.log.info('service server down')

    def stop(self):
        self.log.info('service server shutting down.....')
        self.done = True

    def garbageCon(self):
        '''Remove connections deads'''

        self.log.info("garbage connections start")

        totais = 0
        while True:

            lista_remover = []
            for thread in self.lista:
                if thread.isAlive() is False:
                    self.log.debug('thread %s removed, total: %d', thread.getName(), totais + 1)
                    totais += 1
                    thread.join()
                    lista_remover.append(thread)

            for thread in lista_remover:
                self.lista.remove(thread)

            if len(lista_remover) is not 0:
                lista_remover.clear()

            if self.done is True:
                if len(self.lista) == 0:
                    break

            time.sleep(1)

        self.log.info("garbage connection stop after %d removed", totais)

    def builderConnection(self, sock, serverConnection):

        self.log.info("factory connections start")
        seq = 0

        while True:
            try:
                # accept connections from outside
                clientsocket, address = sock.accept()

                #self.log.debug("factory server new connection")
                
                comm_param={}
                comm_param['clientsocket'] = clientsocket
                comm_param['addr'] =  address
                comm_param['done'] =  self.done

                self.log.info("connected with :%s", str(address))

                t = threading.Thread(target=serverConnection, name='conection_{0}'.format(seq) ,args=(seq, comm_param))
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