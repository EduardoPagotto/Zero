#!/usr/bin/env python3
'''
Created on 20170119
Update on 20190821
@author: Eduardo Pagotto
'''

import sys
import os
import time
import threading
import logging
import socket

import common_side1

sys.path.append('../Zero')

from Zero.UnixDomainServer import UnixDomainServer
from Zero.Protocol import Protocol, ProtocolCode
from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose, ExceptionZeroErro
from Zero.subsys.GracefulKiller import GracefulKiller

def garbageT(lista):
    '''Remove connections deads'''

    logging.debug("garbage connection begin")

    totais = 1
    while True:
        lista_remover = []
        for thread in lista:
            if thread.isAlive() is False:
                logging.warning('thread %s removed, total: %d', thread.getName(), totais)
                totais += 1
                thread.join()
                lista_remover.append(thread)

        for thread in lista_remover:
            lista.remove(thread)

        if len(lista_remover) is not 0:
            lista_remover.clear()

        time.sleep(1)

    logging.debug("garbage connection finished after %d removed", totais)

def factoryServerConn(sock, lista_comm, func_new_conection):

    logging.debug("factory server connection start")
    seq = 0

    while True:
        try:
            logging.debug("factory server new connection")

            # accept connections from outside
            clientsocket, address = sock.accept()

            comm_param={}
            comm_param['clientsocket'] = clientsocket
            comm_param['addr']=  address

            logging.debug("connected with :%s", str(address))

            t = threading.Thread(target=func_new_conection, name='conection_{0}'.format(seq) ,args=(seq, comm_param))
            t.start()

            lista_comm.append(t)

            seq += 1

        except socket.timeout:
            logging.debug('server to..')

        except Exception as exp:
            logging.exception('Fail:%s', str(exp))
            break

    logging.debug("factory server connection finished")

def createServerConnection(args, kwargs):

    logging.info('connection stated')

    protocol = None
    try:
        protocol = Protocol(kwargs['clientsocket'])
        protocol.settimeout(10)
        
    except Exception as exp:
        logging.exception('falha na parametrizacao da conexao: {0}'.format(str(exp)))
        return

    while True:
        try:
            idRec, msg = protocol.receiveString()
            if idRec is ProtocolCode.COMMAND:

                # comando_str = msg.replace("'", "\"")
                # comando_dic = json.loads(comando_str)
                # comando = comando_dic['comando']

                logging.info('Comando Recebido:{0}'.format(msg))

                if msg == 'ola 123':
                    protocol.sendString(ProtocolCode.OK, 'echo: {0}'.format(msg))
                else:
                    protocol.sendString(ProtocolCode.OK, 'teste 2')

        except ExceptionZeroErro as exp_erro:
            logging.debug('recevice Erro: {0}'.format(str(exp_erro)))
            protocol.sendString(ProtocolCode.OK,'recived error from server')

        except ExceptionZeroClose as exp_close:
            logging.debug('receive Close: {0}'.format(str(exp_close)))
            break

        except socket.timeout:
            logging.debug('connection timeout..')

        except Exception as exp:
            logging.error('error: {0}'.format(str(exp)))
            break

    logging.info('connection finished')


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',
    )

    #killer = GracefulKiller()
    lista = []

    server = UnixDomainServer(common_side1.uds_target)
    server.settimeout(10)
    logging.debug('server timeout: %s',str(server.gettimeout()))

    t_server = threading.Thread(target=factoryServerConn, name='factory_conn', args=(server.getSocket(), lista, createServerConnection))
    t_server.start()

    t_garbage = threading.Thread(target=garbageT, name='garbage_conn', args=(lista,))
    t_garbage.start()

    cycle = 0
    while True:
        
        logging.info('cycle:%d connections:%d', cycle, len(lista))
        cycle += 1
        time.sleep(1)

        # if killer.kill_now is True:
        #     server.close()
        #     break

    logging.info('server finifing.....')

    t_server.join()
    t_garbage.join()

    logging.info('server finished')