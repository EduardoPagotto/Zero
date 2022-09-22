#!/usr/bin/env python3
'''
Created on 20220917
Update on 20220921
@author: Eduardo Pagotto
'''

import logging
from typing import Tuple

from Zero import ServiceBus, Protocol, ExceptionZeroErro

class ClientZSF(ServiceBus):
    def __init__(self, s_address: str, retry: int = 3, max_threads: int = 5):
        super().__init__(s_address, retry, max_threads)
        #self.last_buffer : bytes = None
        self.last_pathfile : str = ''

    # Hook to extra comunication with raw data between json protocol
    def cb_file(self, name : str, conn : Protocol):

        if name == 'save_Xfer':
            try:
                conn.sendFile(self.last_pathfile)  

            except ExceptionZeroErro as exp:
                print(' Erro: ' + str(exp)) # FIXME: log ???

        elif name == 'load_Xfer':
            try:
                conn.receiveFile(self.last_pathfile)
                
            except ExceptionZeroErro as exp:
                print(' Erro: ' + str(exp)) # FIXME: log ???


    def __rpc(self):
        return self.getObject(self.cb_file)

    ''' Salva um novo arquivo e inicia seu ciclo '''
    def upload_file(self, path_file: str, opt: dict = {}) -> Tuple[bool, str ,int]:
    
        self.last_pathfile = path_file
        return self.__rpc().save_Xfer(path_file, opt)

    ''' Carrega um arquivo existente '''
    def download_file(self, id : int, pathfile : str) -> Tuple [bool, str]:
        self.last_pathfile = pathfile
        return self.__rpc().load_Xfer(id)

    ''' Retorna os dados do arquivo '''
    def info(self, id : int) -> dict:
        return self.__rpc().info_file(id)

    ''' Mantem ele por mais um ciclo '''
    def keep(self, id : int)-> Tuple [bool, str] :
        return self.__rpc().keep_file(id)

    ''' Remove arquivo existente '''
    def remove(self, id : int)-> Tuple [bool, str] :
        return self.__rpc().remove_file(id)

    def set_server_expire(self, days : int, hours : int, minute : int):
        self.__rpc().set_server_expire(days, hours, minute)