'''
Created on 20190822
Update on 20200727
@author: Eduardo Pagotto
'''

from typing import Union, Any

from Zero.transport.SocketFactory import SocketFactoryClient
from Zero.ConnectionControl import ConnectionControl
from Zero.ProxyObject import ProxyObject

class ServiceBus(object):
    def __init__(self, s_address : str, retry : int=3, max_threads : int=5):
        """[Container of Wrapper Client RPC]
        Args:
            s_address (str): [valid's : ( uds://./conexao_peer | tcp://127.0.0.1:5151) ]
            retry (int, optional): [Tentativa de reconexa]. Defaults to 3.
            max_threads (int, optional): [Numero maximo de threads de conexao simultaneas]. Defaults to 5.
        """

        self.factoty_client = SocketFactoryClient(s_address, retry)
        self.max_threads = max_threads
        self.conn_control : Union[ConnectionControl, None] =  None

    def getObject(self) -> ProxyObject:
        """[Get connectd exchange with server RPC]
        Returns:
            ProxyObject: [Proxy conectado com controle de conexao e reentrada]
        """

        if self.conn_control is None:
            self.conn_control = ConnectionControl(self.factoty_client, self.max_threads)

        return ProxyObject(self.conn_control)

    def close_all(self) -> None:
        """[Stop connections to finisher tho client]
        """
        try:
            if self.conn_control is not None:
                self.conn_control.stop()
                self.conn_control.join()
                self.conn_control = None
        except:
            pass

    def __del__(self):
        """[desconecta e encerra conexao]
        """
        self.close_all()
