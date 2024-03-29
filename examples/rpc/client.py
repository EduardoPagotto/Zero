#!/usr/bin/env python3
'''
Created on 20190822
Update on 20220921
@author: Eduardo Pagotto
'''

import time
import logging

import common as rpc
from Zero import ServiceBus
from Zero import ExceptionZeroRPC
from Zero import ExceptionZeroErro
from Zero import Protocol

# class RPC_Client(ServiceBus):
#     def __init__(self, s_address: str, retry: int = 3, max_threads: int = 5):
#         super().__init__(s_address, retry, max_threads)

#     def command(self):
#         return self.getObject()

# Hook to extra comnication with raw data between json protocol
def call_backTeste(name : str, conn : Protocol):

    if name == 'save_Xfer':
        try:
            #conn.sendFile('./teste.tar.gz')
            conn.sendErro('Operacao Ilegal')  

        except ExceptionZeroErro as exp:
            print(' Erro: ' + str(exp))

    elif name == 'load_Xfer':
        try:
            conn.receiveFile('./testeReceive.tar.gz')
            #conn.sendErro('Operacao Ilegal') 

        except ExceptionZeroErro as exp:
            print(' Erro: ' + str(exp))

    else:
        pass


def main():
    try:
        log = logging.getLogger('Client')
        bus = ServiceBus(rpc.ADDRESS)

        ponta = bus.getObject(None)

        ## used to extra communication whit raw data
        # ponta = bus.getObject(call_backTeste)
        #ponta.save_Xfer({'id':1, 'file':''})
        #ponta.load_Xfer('./testeReceive.tar.gz')

        ponta.testeA('primeiro', 'segundo', val1='val1', val2='teste2', val3='DDD')

        valor = ponta.getNome()
        log.debug('Nome Atual: %s', valor)

        time.sleep(5)

        if valor == 'Jose':
            ponta.setNome('Maria')
        else:
            ponta.setNome('Jose')


        log.debug('RPC retorno: %s', ponta.is_alive_bitch())

        valor = ponta.teste_target(4)
        log.debug('RPC retorno: %s', valor)

        dados = {'nome':'pagotto', 'idade':50, 'sexo':True, 'opt':{'val1':'teste1', 'lista':['um', 'dois']}}
        retorno = ponta.get_dict(dados)
        log.debug('RPC retorno:%s', str(retorno))

        log.debug('esperar 80 segundos para proxima consulta')
        time.sleep(80)
        valor = ponta.getNome()
        log.debug('Nome Atual: %s', valor)
        time.sleep(40)
        valor = ponta.getNome()
        log.debug('Nome Atual: %s', valor)

        #valor = ponta.sendTesteComando('texto',10, False, nome='eduardo', idade=50, peso=70.5, sexo=True)
        #log.debug('RPC retorno: %s', valor)

    except ExceptionZeroRPC as exp:
        log.error('ERRO: {0}'.format(str(exp)))

    except Exception as exp:
        log.error('Falha: {0}'.format(str(exp)))

    bus.close_all()

    log.info('App desconectado')


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    main()
