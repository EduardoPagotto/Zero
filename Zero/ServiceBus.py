'''
Created on 20190822
Update on 20200517
@author: Eduardo Pagotto
'''

#pylint: disable=C0301, C0116, W0703, C0103, C0115

from Zero.ConnectionControl import ConnectionControl
from Zero.ProxyObject import ProxyObject
from Zero.transport.Transport import get_address_from_string

class ServiceBus(object):
    def __init__(self, s_address, retry=3, max_threads=5):
        """[Pre-Conexao dados do peer]
        Arguments:
            s_address {[string]} -- [exemplo validos:( uds://./conexao_peer | tcp://127.0.0.1:5151) ]
        Keyword Arguments:
            retry {int} -- [Tentativa de reconexa] (default: {3})
            max_threads {int} -- [Numero maximo de threads de conexao simultaneas] (default: {5})
        """
        self.address, self.transportKind = get_address_from_string(s_address)
        self.retry = retry
        self.max_threads = max_threads
        self.conn_control = None

    def getObject(self):
        """[ProxyObject conectao ao peer]
        Returns:
            [ProxyObject] -- [Proxy conectado com controle de conexao e reentrada]
        """
        self.conn_control = ConnectionControl(self.transportKind, self.address, self.retry, self.max_threads)
        return ProxyObject(self.conn_control)

    def __del__(self):
        """[desconecta e encerra conexao]
        """
        self.conn_control.stop()
        self.conn_control.join()
