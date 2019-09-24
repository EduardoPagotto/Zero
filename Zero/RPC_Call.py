'''
Created on 20190823
Update on 20190924
@author: Eduardo Pagotto
'''

import json
import threading

from Zero.subsys.ExceptionZero import ExceptionZeroRPC

class RPC_Call(object):

    json_rpc_version = '2.0'
    __serial_lock = threading.Lock()
    __serial = 0

    def __init__(self, nome_metodo, control):
        self.control = control
        self.method = nome_metodo
        self.serial = RPC_Call.__createId()

    @staticmethod
    def __createId():
        with RPC_Call.__serial_lock:
            serial = RPC_Call.__serial
            RPC_Call.__serial += 1

            return serial

    def encode(self,  *args, **kargs):

        keys = {}
        arguments = []
        if args:
            arguments = args[0]
            keys=args[1]

        return json.dumps({'jsonrpc':RPC_Call.json_rpc_version, 'id':self.serial, 'method': self.method, 'params': arguments, 'keys': keys})

    def decode(self, msg):

        # TODO: get exceptions from json
        dados = json.loads(msg)
        if dados['id'] == self.serial:
            if 'error' in dados:
                raise ExceptionZeroRPC(dados['error']['message'], dados['error']['code'])

            return dados['result']
  
        raise ExceptionZeroRPC('Parse error, id {0} should be {1}'.format(dados['id'], self.serial), -32700)

    def __call__(self, *args, **kargs):

        conn = self.control.get_connection()

        msg_in = conn.connection.exchange(self.encode(args, kargs))

        self.control.release_connection(conn)

        return self.decode(msg_in)


def RPC_Result(target, msg):

    dados = json.loads(msg)
    serial = dados['id']
    metodo = dados['method']

    try:
        if len(dados['params']) > 0:
            val = getattr(target, metodo)(*dados['params'])
        else:
            val = getattr(target, metodo)()

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
