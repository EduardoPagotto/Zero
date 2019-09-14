'''
Created on 20190823
Update on 20190914
@author: Eduardo Pagotto
'''

from Zero.RPC_Protocol import RPC_ProtocolMethod

class RPC_Call(object):
    def __init__(self, nome_metodo, control):
        self.control = control
        self.rpc = RPC_ProtocolMethod(nome_metodo)

    def __call__(self, *args, **kargs):

        conn = self.control.get_connection()

        msg_in = conn.connection.exchange(self.rpc.encode(args, kargs))

        self.control.release_connection(conn)

        return self.rpc.decode(msg_in)
