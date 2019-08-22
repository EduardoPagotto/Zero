'''
Created on 20170119
Update on 20190821
@author: Eduardo Pagotto
'''

import logging

# usado no UnixDomainSocket
uds_target = './uds_socket_teste'

#usado no Network Socket
ip_target = ('127.0.0.1', 4040)

# habilita o log
def enable_log():

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    #return logging.getLogger('TEST')