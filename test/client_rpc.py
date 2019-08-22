#!/usr/bin/env python3
'''
Created on 20190822
Update on 20190822
@author: Eduardo Pagotto
'''

import sys
import os
import time
import threading
import logging

import common_side1

sys.path.append('../Zero')

from Zero.ServiceBus import ServiceBus
from Zero.subsys.ExceptionZero import ExceptionZero, ExceptionZeroClose

def main():

    try:
        log = logging.getLogger('Client')
        bus = ServiceBus()
        
        ponta = bus.getObject(common_side1.uds_target)

        log.info('Recebido: %s', ponta.exchange('ZZZZ teste 123....'))
        time.sleep(10)
        
        log.info('Recebido: %s', ponta.exchange('ZZZZ teste 123....'))
        time.sleep(10)
        
        log.info('Recebido: %s', ponta.exchange('ZZZZ teste 123....'))
        time.sleep(10)
    
    except Exception as exp:
        log.exception('Falha {0}'.format(str(exp)))

    log.info('App desconectado')


if __name__ == '__main__':

    common_side1.enable_log()

    main()
