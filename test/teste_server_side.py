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

import common_acess

sys.path.append('../Zero')

from Zero.SocketBase import SocketBase
from Zero.UnixDomainSocketServer import UnixDomainServer
from Zero.Protocol import Protocol, ProtocolCode

def remove_conexoes_finalizadas(servidor_ativo):
    '''Remove conxoes ativas da memoria'''
    lista = servidor_ativo.lista_thread_online

    #logging.warning('Threads ONLINE: %d', len(lista))

    lista_remover = []

    for thread in lista:
        if thread.isAlive() is False:

            logging.warning('Thread %s morta id ', thread.getName())

            thread.join()
            lista_remover.append(thread)

    for thread in lista_remover:
        lista.remove(thread)

    if len(lista_remover) is not 0:
        lista_remover.clear()


def createServerConnection(args, kwargs):

    protocol = Protocol()

    try:
        
        protocol.setSocket(kwargs['clientsocket'])
        protocol.ipAddr = kwargs['addr']
    except Exception as exp:
        logging.exception('Falha na paremtrizacao da conexao: {0}'.format(str(exp)))
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
                    protocol.sendString(ProtocolCode.OK, 'Echo: {0}'.format(msg))
                else:
                    protocol.sendString(ProtocolCode.ERRO, 'Comando inesperado')

            elif idRec is ProtocolCode.CLOSE:
                logging.warning('Close Recebido:{0}'.format(msg))
                protocol.close()
                break

        except Exception as exp:
            logging.error('Erro identificado: {0}'.format(str(exp)))
            break

    logging.info('Conexao encerrada')


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',
    )

    servidor = UnixDomainServer(common_acess.uds_target)
    t_server = threading.Thread(target=servidor.loop, args=(createServerConnection,))
    t_server.start()

    ciclo = 0
    while True:
        
        logging.info('Ciclo:%d Conexoes:%d', ciclo, len(servidor.lista_thread_online))
        remove_conexoes_finalizadas(servidor)
        ciclo += 1
        time.sleep(5)