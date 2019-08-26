'''
Created on 20190826
Update on 20190826
@author: Eduardo Pagotto
'''

import json

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
        dados = json.loads(msg)

        if dados['id'] == self.serial:
            if 'error' in dados:
                self.__error = dados['error']
                raise Exception('Erro code:%d, msg:%s', dados['error']['code'], dados['error']['message'])

            retorno = dados['result']
        else:
            raise Exception('Id recebido invalido')

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
                val = getattr(self.target, metodo)(dados['params'])
            else:
                val = getattr(self.target, metodo)()

            return json.dumps({'jsonrpc': self.vesion, 'result':val, 'id':dados['id']})

        except Exception as exp:

            code = -1
            msg = str(exp)

            return {'jsonrpc': self.vesion, 'error': {'code': code, 'message': msg}, 'id': self.serial}
