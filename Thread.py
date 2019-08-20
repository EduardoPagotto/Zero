#!/usr/bin/env python3
'''
Created on 20170119
Update on 20181001
@author: Eduardo Pagotto
'''

#pylint: disable=C0301
#pylint: disable=C0103
#pylint: disable=W0703

import threading
import logging

class ThreadSafeValue(object):
    """[ThreadSafe variavel]
    Arguments:
        objet {[type]} -- [description]
    Returns:
        [type] -- [description]
    """

    def __init__(self, value):
        """[Inicializa value e mutex]
        Arguments:
            value {[type]} -- [description]
        """
        self.__mutex = threading.Lock()
        self.__value = value

    def __str__(self):
        """[retorna string do value]
        Returns:
            [string] -- [value]
        """
        with self.__mutex:
            return str(self.__value)

    def inc(self):
        with self.__mutex:
            self.__value += 1
            return self.__value

    def dec(self):
        with self.__mutex:
            self.__value -= 1
            return self.__value

    def acc(self, valor):
        with self.__mutex:
            self.__value += valor
            return self.__value

    def sub(self, valor):
        with self.__mutex:
            self.__value -= valor
            return self.__value

    def set_value(self, value):
        """[Grava value]
        Arguments:
            value {[type]} -- [description]
        """
        with self.__mutex:
            self.__value = value

    def get_value(self):
        """[retorna value]
        Returns:
            [type] -- [description]
        """
        with self.__mutex:
            return self.__value

class Thread(threading.Thread):
    """[Wrapper de classe Thread]
    Arguments:
        threading {[type]} -- [description]
    Raises:
        NotImplementedError -- [description]
    Returns:
        [type] -- [description]
    """

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        """[Contructor da classe de thread customizada]
        Keyword Arguments:
            group {[type]} -- [description] (default: {None})
            target {[type]} -- [description] (default: {None})
            name {[type]} -- [description] (default: {None})
            args {tuple} -- [description] (default: {()})
            kwargs {[type]} -- [description] (default: {None})
        """

        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        self._encerra_t = False
        self.__done = False
        return

    def stop(self):
        """[Sinaliza o encerramento da thread]
        """
        self._encerra_t = True
        logging.debug('Stop executado')

    def execute(self):
        """[Entrypoind de execucao da classe]
        Raises:
            NotImplementedError -- [description]
        """
        raise NotImplementedError('subclasses must override execute()!')

    def run(self):
        """[Executa]
        """
        logging.debug('Thread %s iniciada ', self.getName())
        self.execute()
        logging.debug('Thread %s finalizada ', self.getName())
        self.__done = True
        return

    @property
    def is_done(self):
        """[etorna True se thread Finalizou a tarefa]
        Returns:
            [bool] -- [True se finalizada]
        """
        return self.__done

# def createThreadCon(args=(), kwargs=None):
#     '''Cria funcao '''

#     global contador_conexao_num
#     contador_conexao_num += 1

#     nova = TesteThread(args=args, kwargs=kwargs, group=None, name='TConexao_{0}'.format(contador_conexao_num))
#     return nova


# contador_conexao_num = 0

# class TesteThread(NeoThread):
#     '''Wrapper de Thred'''
#     def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
#         NeoThread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs)
#         #self.args = args
#         #self.kwargs = kwargs
#         #return

#     def execute(self):
#         contador = 0

#         desv = random.randint(0, 50) + 10
#         logging.info('execute %s......:%d', self.getName(), desv)
#         while contador < desv:
#             #logging.info('Teste %s......:(%d/%d)', self.getName(), contador, desv)
#             contador += 1
#             time.sleep(1)

#         return

# if __name__ == '__main__':

#     configure_logging('log/testez1.log')
#     logging.info('Ativado Teste')

#     lista = []
#     tot = len(lista)

#     contador = 0
#     while contador is not 100:
#         thread = createThreadCon(args=(tot,), kwargs={})
#         lista.append(thread)
#         thread.start()
#         contador += 1

#     while len(lista) is not 0:
#         logging.warning('Threads ONLINE: %d', len(lista))
#         lista_remover = []

#         for thread in lista:
#             if thread.isAlive() is False:
#                 logging.warning('Thread %s morta id ', thread.getName())
#                 thread.join()
#                 lista_remover.append(thread)

#         for thread in lista_remover:
#             lista.remove(thread)

#         if len(lista_remover) is not 0:
#             lista_remover.clear()

#         time.sleep(1)

#     logging.warning('ENCERRADO')

