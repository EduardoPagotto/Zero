#!/usr/bin/env python3
'''
Created on 20190822
Update on 20190822
@author: Eduardo Pagotto
'''


import logging
import time

import common_side1

import sys
sys.path.append('../Zero')

from Zero.subsys.GracefulKiller import GracefulKiller
from Zero.ServiceObject import ServiceObject

class ServerRPC(ServiceObject):
    def __init__(self):
        device_bus = ''

        self.vivo = True

        super().__init__(device_bus, common_side1.uds_target)


    def is_alive_bitch(self):
        return self.vivo  


def main():

    log = logging.getLogger('Server')
    #logging.getLogger('Zero').setLevel(logging.INFO)

    try:

        killer = GracefulKiller()

        server = ServerRPC()

        while True:
            time.sleep(1)
            if killer.kill_now is True:
                server.stop()  
                break

        server.join()

    except Exception as exp:
        log.Exception('falha %s', str(exp))

if __name__ == '__main__':

    common_side1.enable_log()
    main()
