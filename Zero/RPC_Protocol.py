'''
Created on 20190826
Update on 20190912
@author: Eduardo Pagotto
'''

import json
from Zero.subsys.ExceptionZero import ExceptionZeroRPC

class RPC_Protocol(object):
    def __init__(self):
        self.vesion = '2.0'
        self.serial = 0
        self.__error = None    

    def getError(self):
        return self.__error

class RPC_ProtocolMethod(RPC_Protocol):
    __serial = 0
    def __init__(self, method):
        super().__init__()
        self.method = method

    def decode(self, msg):
        retorno = None

        # TODO: get exceptions from json
        dados = json.loads(msg)

        if dados['id'] == self.serial:
            if 'error' in dados:
                self.__error = dados['error']
                raise ExceptionZeroRPC(dados['error']['message'], dados['error']['code'])

            retorno = dados['result']
        else:
            raise ExceptionZeroRPC('Parse error: id recived invalid', -32700)

        return retorno

    def encode(self, *args, **kargs):
        keys = {}
        arguments = []
        if args:
            arguments = args[0]
            keys=args[1]

        self.serial = RPC_ProtocolMethod.__serial
        RPC_ProtocolMethod.__serial += 1

        return json.dumps({'jsonrpc':self.vesion, 'id':self.serial, 'method': self.method, 'params': arguments, 'keys': keys})


class RPC_ProtocolResult(RPC_Protocol):
    def __init__(self, target):
        super().__init__()
        self.target = target

    def exec(self, msg):
    
        dados = json.loads(msg)
        self.serial = dados['id']
        metodo = dados['method']

        try:
            if len(dados['params']) > 0:
                val = getattr(self.target, metodo)(*dados['params'])
            else:
                val = getattr(self.target, metodo)()

            return json.dumps({'jsonrpc': self.vesion, 'result': val, 'id': self.serial})

        except AttributeError as exp:
            return json.dumps({'jsonrpc': self.vesion, 'error': {'code': -32601, 'message': 'Method not found: '+ str(exp)}, 'id': self.serial})

        except TypeError as exp1:
            return json.dumps({'jsonrpc': self.vesion, 'error': {'code': -32602, 'message': 'Invalid params: '+ str(exp1)}, 'id': self.serial})

        except ExceptionZeroRPC as exp2:
            tot = len(exp2.args)
            if tot == 0: 
                return json.dumps({'jsonrpc': self.vesion, 'error': {'code': -32000, 'message': 'Server error: Generic Zero RPC Exception'}, 'id': self.serial})
            elif tot == 1:
                return json.dumps({'jsonrpc': self.vesion, 'error': {'code': -32001, 'message': 'Server error: ' + exp2.args[0]}, 'id': self.serial})
            else: 
                return json.dumps({'jsonrpc': self.vesion, 'error': {'code': exp2.args[1], 'message': 'Server error: ' + exp2.args[0]}, 'id': self.serial})

        except Exception as exp3:
            return json.dumps({'jsonrpc': self.vesion, 'error': {'code': -32603, 'message': 'Internal error: ' + str(exp3)}, 'id': self.serial})