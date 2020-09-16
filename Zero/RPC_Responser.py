'''
Created on 20190824
Update on 20200916
@author: Eduardo Pagotto
'''

import logging
import socket
import json

from Zero.common import __json_rpc_version__ as json_rpc_version
from Zero.transport.Protocol import Protocol, ProtocolCode
from Zero.subsys.ExceptionZero import ExceptionZeroClose, ExceptionZeroErro, ExceptionZeroRPC

# TODO: Criar classe base de conexao peer e fazer RPC_Responser derivada desta
# class ConnectionServerBase(object):
#     def __init__(self, done):
#         self.done = done
#         self.log = logging.getLogger('Zero.RPC')

#         self.protocol = None

#     def load(self, *args, **kargs):
#         dados_conexao = args[1]
#         self.protocol = Protocol(dados_conexao['clientsocket'])
#         self.protocol.settimeout(30)

#         if 'to' in dados_conexao:
#             self.protocol.settimeout(dados_conexao)


class RPC_Responser(object):
    """[Connection thread with server RPC ]
    Args:
        object ([type]): [description]
    """

    def __init__(self, target : object):
        """[summary]
        Args:
            target (object): [Method Name to run in RPC Server]
        """
        self.log = logging.getLogger('Zero.RPC')
        self.target : object= target

    def __call__(self, *args, **kargs):
        """[execute exchange of json's messages with server RPC]
        """
        indice_conexao = args[0]
        dados_conexao = args[1]
        done = dados_conexao['done']

        self.log.info('responser %d open %s', args[0], str(dados_conexao['addr']))

        protocol = None
        try:
            protocol = Protocol(dados_conexao['clientsocket'])
            protocol.settimeout(30)

        except Exception as exp:
            self.log.critical('responser %d fail creating connection: %s', indice_conexao, str(exp))
            return

        count_to = 0

        while True:
            try:
                idRec, msg_in = protocol.receiveString()
                count_to = 0
                if idRec is ProtocolCode.COMMAND:
                    protocol.sendString(ProtocolCode.RESULT, self.rpc_exec_func(msg_in))

            except ExceptionZeroErro as exp_erro:
                self.log.error('responser %d recevice erro: %s',indice_conexao, str(exp_erro))
                protocol.sendString(ProtocolCode.RESULT, 'recived error from server')

            except ExceptionZeroClose as exp_close:
                self.log.warning('responser %d receive: %s',indice_conexao, str(exp_close))
                break

            except socket.timeout:
                count_to += 1
                self.log.warning('responser %d TO count: %d', indice_conexao, count_to)

            except Exception as exp:
                self.log.error('responser %d exception error: %s', indice_conexao, str(exp))
                break

            if done is True:
                protocol.close()
                break

        self.log.info('responser %d close', indice_conexao)

    def rpc_exec_func(self, msg : str) -> str:
        """[Execule methodo local with paramters in json data (msg)]
        Args:
            msg (str): [json Protocol data received (id, method, parameters)]
        Returns:
            str: [Resulto of method in json Protocol]
        """

        dados : dict = json.loads(msg)
        serial : int = dados['id']
        metodo : str = dados['method']

        try:
            val = getattr(self.target, metodo)(*dados['params'], **dados['keys'])
            return json.dumps({'jsonrpc': json_rpc_version, 'result': val, 'id': serial})

        except AttributeError as exp:
            return json.dumps({'jsonrpc': json_rpc_version, 'error': {'code': -32601, 'message': 'Method not found: '+ str(exp)}, 'id': serial})

        except TypeError as exp1:
            return json.dumps({'jsonrpc': json_rpc_version, 'error': {'code': -32602, 'message': 'Invalid params: '+ str(exp1)}, 'id': serial})

        except ExceptionZeroRPC as exp2:
            tot = len(exp2.args)
            if tot == 0:
                return json.dumps({'jsonrpc': json_rpc_version, 'error': {'code': -32000, 'message': 'Server error: Generic Zero RPC Exception'}, 'id': serial})
            elif tot == 1:
                return json.dumps({'jsonrpc': json_rpc_version, 'error': {'code': -32001, 'message': 'Server error: ' + exp2.args[0]}, 'id': serial})
            else:
                return json.dumps({'jsonrpc': json_rpc_version, 'error': {'code': exp2.args[1], 'message': 'Server error: ' + exp2.args[0]}, 'id': serial})

        except Exception as exp3:
            return json.dumps({'jsonrpc': json_rpc_version, 'error': {'code': -32603, 'message': 'Internal error: ' + str(exp3)}, 'id': serial})