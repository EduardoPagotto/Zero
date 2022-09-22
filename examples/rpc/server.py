#!/usr/bin/env python3
'''
Created on 20190822
Update on 20220921
@author: Eduardo Pagotto
'''

import logging
import common as rpc

from Zero import ServiceObject
from Zero import ExceptionZeroRPC
from Zero import GracefulKiller
from Zero import Protocol
from Zero import ExceptionZeroErro

class ServerRPC(ServiceObject):
    def __init__(self):
        self.vivo = True
        self.nome = 'NOVO'
        self.logLocal = logging.getLogger('Server')
        super().__init__(rpc.ADDRESS, self)

    def teste_target(self, entrada):
        self.logLocal.debug('ESTOU CHEGANDO JEANY!!!!')

        if entrada == 0:
            raise Exception('teste 0 ...')
        elif entrada == 1:
            raise ExceptionZeroRPC()
        elif entrada == 2:
            raise ExceptionZeroRPC('teste 2 ...')
        elif entrada == 3:
            raise ExceptionZeroRPC('teste 3 ...', -32099)

        return False

    #@ServiceObject.rpc_call(identicador=rpc.IS_ALIVE_INTERFACE, input=(), output=('b',))
    def is_alive_bitch(self):
        return self.vivo

    #@ServiceObject.rpc_call(rpc.SET_NOME_INTERFACE, input=('s',), output=())
    def setNome(self, nome):
        self.nome = nome

    #@ServiceObject.rpc_call(rpc.GET_NOME_INTERFACE, input=(''), output=('s',))
    def getNome(self):
        return self.nome

    #@ServiceObject.rpc_call(rpc.GET_DICIONARIO_INTERFACE, input=('d',), output=('d'))
    def get_dict(self, dicionario):
        dicionario['novo'] = 'ola'
        return dicionario

    def testeA(self, *args, **kargs):
        self.logLocal.info('args: %s; kargs: %s', str(args), str(kargs))

    # extra data received from client in raw mode between in-out json protocol
    # attention tho suffix '_Xfer' that add protocolo parameter inside of RPC_Responser
    def save_Xfer(self, data : dict, protocolo : Protocol):
        try:
            self.logLocal.info(f'Data: {str(data)}')
            protocolo.receiveFile('./teste22.tar.gz')
            #protocolo.sendErro('Arquivo nao existe')
            
        except ExceptionZeroErro as exp:
            return False, str(exp.args[0])
            
        return True, "0010333030403400" 
        
    # extra data sended to cliente in raw mode between in-out json protocol
    # attention tho suffix '_Xfer' that add protocolo parameter inside of RPC_Responser
    def load_Xfer(self, msg : str, protocolo : Protocol):
        try:
            self.logLocal.info(f'Msg: {msg}')
            protocolo.sendFile('./teste22.tar.gz')
            #protocolo.sendErro('Arquivo nao existe')

        except ExceptionZeroErro as exp:
            return False, str(exp.args[0])
            
        return True, "0010333030403400" 


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    server = ServerRPC()
    server.loop_blocked(GracefulKiller())
