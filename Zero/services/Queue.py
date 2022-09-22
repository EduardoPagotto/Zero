#!/usr/bin/env python3
'''
Created on 20201214
Update on 20220922
@author: Eduardo Pagotto
'''

import logging
import queue
from typing import Any, Dict, Optional

from Zero import ServiceObject, GracefulKiller

class QueueRpc(ServiceObject):
    def __init__(self, s_address : str):
        self.map_queues : Dict[str, queue.Queue] = {}
        super().__init__(s_address, self)

    def create(self, name : str):

        if name in self.map_queues:
            raise Exception('Queue ja existe {0}'.format(name))

        nova : queue.Queue = queue.Queue()
        self.map_queues[name] = nova

    def destroy(self, name):
        try:
            del self.map_queues[name]
        except:
            raise Exception('Queue não existe {0}'.format(name))

    def push(self, name: str, value : Any) -> None:
        try:
            o_queue = self.map_queues[name]
            o_queue.put(value)
        except:
            raise Exception('Queue não existe {0}'.format(name))

    def pop(self, name : str) -> Optional[Any]:

        o_queue : Optional[queue.Queue] = None
        try:
            o_queue = self.map_queues[name]
        except:
            raise Exception('Queue não existe {0}'.format(name))

        try:
            val = o_queue.get_nowait()
            return val
        except queue.Empty:
            pass

        return None

    def qsize(self, name : str) -> int:
        try:
            o_queue = self.map_queues[name]
            return o_queue.qsize()
        except:
            raise Exception('Queue não existe {0}'.format(name))

    def empty(self, name : str) -> bool:
        try:
            o_queue = self.map_queues[name]
            return o_queue.empty()
        except:
            raise Exception('Queue não existe {0}'.format(name))

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    server = QueueRpc('')
    server.loop_blocked(GracefulKiller())
