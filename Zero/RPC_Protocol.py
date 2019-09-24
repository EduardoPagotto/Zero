'''
Created on 20190826
Update on 20190924
@author: Eduardo Pagotto
'''

import json
from Zero.subsys.ExceptionZero import ExceptionZeroRPC

# class RPC_ProtocolResult(object):
#     def __init__(self, target):
#         self.target = target

#     def exec(self, msg):
    
#         dados = json.loads(msg)
#         serial = dados['id']
#         metodo = dados['method']

#         try:
#             if len(dados['params']) > 0:
#                 val = getattr(self.target, metodo)(*dados['params'])
#             else:
#                 val = getattr(self.target, metodo)()

#             return json.dumps({'jsonrpc': __json_rpc_version, 'result': val, 'id': serial})

#         except AttributeError as exp:
#             return json.dumps({'jsonrpc': __json_rpc_version, 'error': {'code': -32601, 'message': 'Method not found: '+ str(exp)}, 'id': serial})

#         except TypeError as exp1:
#             return json.dumps({'jsonrpc': __json_rpc_version, 'error': {'code': -32602, 'message': 'Invalid params: '+ str(exp1)}, 'id': serial})

#         except ExceptionZeroRPC as exp2:
#             tot = len(exp2.args)
#             if tot == 0: 
#                 return json.dumps({'jsonrpc': __json_rpc_version, 'error': {'code': -32000, 'message': 'Server error: Generic Zero RPC Exception'}, 'id': serial})
#             elif tot == 1:
#                 return json.dumps({'jsonrpc': __json_rpc_version, 'error': {'code': -32001, 'message': 'Server error: ' + exp2.args[0]}, 'id': serial})
#             else: 
#                 return json.dumps({'jsonrpc': __json_rpc_version, 'error': {'code': exp2.args[1], 'message': 'Server error: ' + exp2.args[0]}, 'id': serial})

#         except Exception as exp3:
#             return json.dumps({'jsonrpc': __json_rpc_version, 'error': {'code': -32603, 'message': 'Internal error: ' + str(exp3)}, 'id': serial})