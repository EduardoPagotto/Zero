#!/usr/bin/env python3
'''
Created on 20220917
Update on 20220922
@author: Eduardo Pagotto
'''

import logging

from pathlib import Path
from threading import Lock
from typing import Optional, Tuple

from datetime import datetime, timedelta, timezone
from tinydb import TinyDB, Query

from Zero import ServiceObject, Protocol, ExceptionZeroRPC, ExceptionZeroErro

mutex = Lock()

class ServerZSF(ServiceObject):

    count_file : int = 0

    def __init__(self, s_address : str, path_db : str, path_storage : str):
        super().__init__(s_address, self)
        self.logLocal = logging.getLogger('Zero.ServerZSF')
 
        self.delta = timedelta(days=1, hours=0, minutes=0)

        self.directory = Path(path_db)
        if self.directory.exists() is False:
            self.directory.mkdir(parents=True)

        self.db = TinyDB(f"{str(self.directory)}/master.json")

        self.storage = Path(path_storage)
        if self.storage.exists() is False:
            self.storage.mkdir(parents=True)

        self.ticktack = 0
        self.tot_in = 0
        self.tot_out = 0

    def service_call(self):

        if (self.ticktack % 12) == 0:

            now = datetime.now(tz=timezone.utc)
            limit = (now - self.delta).timestamp()

            with mutex:
                q = Query()
                itens = self.db.search(q.last < limit)
                for val in itens:

                    file = Path(val['internal'])
                    file.unlink(missing_ok=True)

                    self.logLocal.debug(f"Remove ID:{val.doc_id} file: {val['internal']}")
                    self.db.remove(doc_ids=[val.doc_id])
                    self.tot_out += 1

            self.logLocal.debug(f'Tick-Tack [{int(self.ticktack / 12)} / {self.tot_in} / {self.tot_out} ]' )

        self.ticktack += 1

    # extra data received from client in raw mode between in-out json protocol
    # attention tho suffix '_Xfer' that add protocolo parameter inside of RPC_Responser
    def save_Xfer(self, path_file: str, opt: dict, protocolo : Protocol) -> Tuple[bool, str ,int]:

        id : int = 0
        now = datetime.now(tz=timezone.utc)
        ts = now.timestamp() 
        data_file = {'pathfile': path_file,
                     'opt' : opt,
                     'created': ts,
                     'last': ts,
                     'internal' : 'Invalid'}

        list_ext = path_file.split('.')

        kind = 'bin'
        if len(list_ext) > 1:
            kind = list_ext[-1]

        path1 : Path = Path(str(self.storage) + '/' + now.strftime('%Y%m%d/%H/%M'))
        if path1.exists() is False:
            path1.mkdir(parents=True)

        ServerZSF.count_file += 1
        final : str = str(path1) + '/file{:04d}.{}'.format(ServerZSF.count_file, kind)
        data_file['internal'] = final

        with mutex:
            id = self.db.insert(data_file)
         
        try:
            protocolo.receiveFile(final)
            self.logLocal.debug(f'new ID: {id} File:{str(final)}')
            self.tot_in += 1
            #protocolo.sendErro('Arquivo nao existe')
            
        except Exception as exp:
            with mutex:
                self.db.remove(doc_ids=[id])

            return False, str(exp.args[0]), -1
            
        return True, 'ok', id

    # extra data sended to cliente in raw mode between in-out json protocol
    # attention tho suffix '_Xfer' that add protocolo parameter inside of RPC_Responser
    def load_Xfer(self, id : int, protocolo : Protocol) -> Tuple [bool, str]:
        try:

            param : Optional[dict] = None
            with mutex:
                param = self.db.get(doc_id=id)
                if (param is not None) and (param['last'] != 0):
                    #now = datetime.now(tz=timezone.utc).timestamp() 
                    #ts = now.timestamp() 
                    self.db.update({'last': datetime.now(tz=timezone.utc).timestamp()}, doc_ids=[id])
                else:
                    protocolo.sendErro('Arquivo nao existe')
                    return False, 'Arquivo nao existe'

            protocolo.sendFile(param['internal'])

        except ExceptionZeroErro as exp:
            return False, str(exp.args[0])
            
        return True, 'ok' 

    def info_file(self, id : int) -> Optional[dict]:
        with mutex:
            #return self.db.get(doc_id=id)

            data = self.db.get(doc_id=id)
            if data:
                del data['internal']
                if data['last'] == 0:
                    return None

            return data

    def keep_file(self, id : int)-> Tuple [bool, str] :

        now = datetime.now(tz=timezone.utc)
        with mutex:
            self.db.update({'last': now.timestamp()}, doc_ids=[id])

        return True, 'ok'

    def remove_file(self, id : int)-> Tuple [bool, str] :

        with mutex:
            self.db.update({'last': 0}, doc_ids=[id]) # set to delete now

        return True, 'ok'

    def set_server_expire(self, days : int, hours : int, minute : int):
        with mutex:
            self.delta = timedelta(days=days, hours=hours, minutes=minute)