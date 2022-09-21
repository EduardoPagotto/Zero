'''
Created on 20170119
Update on 20200718
@author: Eduardo Pagotto
'''

import logging

# Usado UnixDomainSocket
#ADDRESS = 'unix:./uds_test_rpc' 

# Usado Network Socket
ADDRESS = 'tcp://127.0.0.1:5151'


# habilita o log
def enable_log():

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    #return logging.getLogger('TEST')
