'''
Created on 20190824
Update on 20200917
@author: Eduardo Pagotto
'''

import logging
import socket
import json

import threading

from Zero.common import __json_rpc_version__ as json_rpc_version
from Zero.transport.Protocol import Protocol, ProtocolCode
from Zero.subsys.ExceptionZero import ExceptionZeroClose, ExceptionZeroErro, ExceptionZeroRPC

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
        done = args[2]

        t_name = threading.currentThread().getName()

        self.log.info('%s open %s', t_name, str(args[1]))

        protocol = None
        try:
            protocol = Protocol(args[0])
            protocol.settimeout(30)

        except Exception as exp:
            self.log.critical('%s fail creating connection: %s', t_name, str(exp))
            return

        count_to = 0

        while done is False:
            try:
                idRec, msg_in = protocol.receiveString()
                count_to = 0
                if idRec is ProtocolCode.COMMAND:
                    protocol.sendString(ProtocolCode.RESULT, self.rpc_exec_func(msg_in))

            except ExceptionZeroErro as exp_erro:
                self.log.error('%s recevice erro: %s',t_name, str(exp_erro))
                protocol.sendString(ProtocolCode.RESULT, 'recived error from server')

            except ExceptionZeroClose as exp_close:
                self.log.warning('%s receive: %s',t_name, str(exp_close))
                break

            except socket.timeout:
                count_to += 1
                self.log.warning('%s TO count: %d', t_name, count_to)

            except Exception as exp:
                self.log.error('%s exception error: %s', t_name, str(exp))
                break

        protocol.close()

        self.log.info('%s close', t_name)

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