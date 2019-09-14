'''
Created on 20190822
Update on 20190914
@author: Eduardo Pagotto
'''

from Zero.ConnectionControl import ConnectionControl
from Zero.ProxyObject import ProxyObject

class ServiceBus(object):
    def __init__(self):
        self.conn_control = None
        
    def getObject(self, object_path):
        self.conn_control = ConnectionControl(object_path, 3)
        return ProxyObject(self.conn_control)

    def __del__(self):
        self.conn_control.stop()
        self.conn_control.join()
       