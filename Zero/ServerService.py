#!/usr/bin/env python3
'''
Created on 20190822
Update on 20190822
@author: Eduardo Pagotto
'''

import time
import socket
import logging
import threading

class ServerService(object):
    def __init__(self, socket_server, createServerConnection):
        self.lista = []
        self.done = False
        self.t_garbage = threading.Thread(target=self.garbageCon, name='garbage_conn')
        self.t_server = threading.Thread(target=self.factoryCon, name='factory_conn', args=(socket_server, createServerConnection))
        
    def start(self):
        logging.info('service server start')
        self.t_garbage.start()
        self.t_server.start()

    def join(self):
        self.t_server.join()
        self.t_garbage.join()
        logging.info('service server down')

    def stop(self):
        logging.info('service server shutting down.....')
        self.done = True

    def garbageCon(self):
        '''Remove connections deads'''

        logging.debug("garbage start")

        totais = 0
        while True:

            lista_remover = []
            for thread in self.lista:
                if thread.isAlive() is False:
                    logging.warning('thread %s removed, total: %d', thread.getName(), totais + 1)
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

        logging.debug("garbage connection stop after %d removed", totais)

    def factoryCon(self, sock, func_new_conection):

        logging.debug("factory start")
        seq = 0

        while True:
            try:
                # accept connections from outside
                clientsocket, address = sock.accept()

                logging.debug("factory server new connection")
                
                comm_param={}
                comm_param['clientsocket'] = clientsocket
                comm_param['addr'] =  address
                comm_param['done'] =  self.done

                logging.debug("connected with :%s", str(address))

                t = threading.Thread(target=func_new_conection, name='conection_{0}'.format(seq) ,args=(seq, comm_param))
                t.start()

                self.lista.append(t)

                seq += 1

            except socket.timeout:
                logging.debug('server to..')

            except Exception as exp:
                if self.done is False:
                    logging.error('Fail:%s', str(exp))
                else:
                    break

        logging.debug("factory stop")