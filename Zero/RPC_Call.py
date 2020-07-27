'''
Created on 20190823
Update on 20200725
@author: Eduardo Pagotto
'''

import json
import threading

from Zero.ConnectionControl import ConnectionControl
from Zero.subsys.ExceptionZero import ExceptionZeroRPC

class RPC_Call(object):
    """[Midlleware json Protocol]
    Args:
        object ([type]): [description]
    Raises:
        ExceptionZeroRPC: [Raised exception on Server of RPC]
        ExceptionZeroRPC: [FATAL!!! invalid ID]
    Returns:
        [type]: [description]
    """

    json_rpc_version : str = '2.0'
    __serial_lock : threading.Lock = threading.Lock()
    __serial : int = 0

    def __init__(self, nome_metodo : str, control : ConnectionControl):
        """[Constructor json message builder]
        Args:
            nome_metodo (str): [method name do send to Server of RPC]
            control (ConnectionControl): [Valid Connection with Server RPC]
        """

        self.serial : int = RPC_Call.__createId()
        self.method : str = nome_metodo
        self.control : ConnectionControl = control

    @staticmethod
    def __createId() -> int:
        """[Identicatos Json Protocol]
        Returns:
            int: [description]
        """
        with RPC_Call.__serial_lock:
            serial = RPC_Call.__serial
            RPC_Call.__serial += 1

            return serial

    def encode(self, *args, **kargs) -> str:
        """[encode json Protocol]
        Returns:
            str: [json with data encoded]
        """

        keys = {}
        arguments = []
        if args:
            arguments = args[0]
            keys = args[1]

        return json.dumps({'jsonrpc':RPC_Call.json_rpc_version, 'id':self.serial, 'method': self.method, 'params': arguments, 'keys': keys})

    def decode(self, msg : str) -> dict:
        """[decode json Protocol]
        Args:
            msg (str): [text with json]
        Raises:
            ExceptionZeroRPC: [Raised exception on Server of RPC]
            ExceptionZeroRPC: [FATAL!!! invalid ID]
        Returns:
            dict: [description]
        """

        # TODO: get exceptions from json
        dados = json.loads(msg)
        if dados['id'] == self.serial:
            if 'error' in dados:
                raise ExceptionZeroRPC(dados['error']['message'], dados['error']['code'])

            return dados['result']

        raise ExceptionZeroRPC('Parse error, id {0} should be {1}'.format(dados['id'], self.serial), -32700)

    def __call__(self, *args, **kargs) -> dict:
        """[Execut RPC on server and get result]
        Returns:
            (dict): [Result of RPC call]
        """

        conn = self.control.get_connection()

        msg_in = conn.connection.exchange(self.encode(args, kargs))

        self.control.release_connection(conn)

        return self.decode(msg_in)


def RPC_Result(target : object, msg : str) -> str:
    """[Translate json data in <->out]
    Args:
        target (object): [self of class Derived from ServiceObject]
        msg (str): [json Protocol data received (in)]
    Returns:
        str: [json Protocol data out]
    """

    dados : dict = json.loads(msg)
    serial : int = dados['id']
    metodo : str = dados['method']

    try:
        val = getattr(target, metodo)(*dados['params'], **dados['keys'])
        return json.dumps({'jsonrpc': RPC_Call.json_rpc_version, 'result': val, 'id': serial})

    except AttributeError as exp:
        return json.dumps({'jsonrpc': RPC_Call.json_rpc_version, 'error': {'code': -32601, 'message': 'Method not found: '+ str(exp)}, 'id': serial})

    except TypeError as exp1:
        return json.dumps({'jsonrpc': RPC_Call.json_rpc_version, 'error': {'code': -32602, 'message': 'Invalid params: '+ str(exp1)}, 'id': serial})

    except ExceptionZeroRPC as exp2:
        tot = len(exp2.args)
        if tot == 0:
            return json.dumps({'jsonrpc': RPC_Call.json_rpc_version, 'error': {'code': -32000, 'message': 'Server error: Generic Zero RPC Exception'}, 'id': serial})
        elif tot == 1:
            return json.dumps({'jsonrpc': RPC_Call.json_rpc_version, 'error': {'code': -32001, 'message': 'Server error: ' + exp2.args[0]}, 'id': serial})
        else:
            return json.dumps({'jsonrpc': RPC_Call.json_rpc_version, 'error': {'code': exp2.args[1], 'message': 'Server error: ' + exp2.args[0]}, 'id': serial})

    except Exception as exp3:
        return json.dumps({'jsonrpc': RPC_Call.json_rpc_version, 'error': {'code': -32603, 'message': 'Internal error: ' + str(exp3)}, 'id': serial})
