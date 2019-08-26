#!/usr/bin/env python3
'''
Created on 20190822
Update on 20190826
@author: Eduardo Pagotto
'''

import sys
import time
import logging

import common_rpc as rpc

sys.path.append('../Zero')

from Zero.ServiceBus import ServiceBus
from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose

def main():

    try:
        log = logging.getLogger('Client')
        bus = ServiceBus()
        
        ponta = bus.getObject(rpc.BUS_PATH)

        valor = ponta.setNome('Jose')
        logging.debug('RPC retorno: %s', valor)

        valor = ponta.getNome()
        logging.debug('RPC retorno: %s', valor)

        #valor = ponta.sendTesteComando('texto',10, False, nome='eduardo', idade=50, peso=70.5, sexo=True)
        #logging.debug('RPC retorno: %s', valor)
        
    except Exception as exp:
        log.exception('Falha {0}'.format(str(exp)))

    log.info('App desconectado')


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    main()
