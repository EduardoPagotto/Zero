#!/usr/bin/env python3
'''
Created on 20190822
Update on 20190823
@author: Eduardo Pagotto
'''

import functools

# decorador simples em funcao 
def upper_d(func):
    @functools.wraps(func)
    def wrapper(self):
        return func(self).upper()
    return wrapper

# decorador com parametros no methodo de classe em funcao
def p_decorate(func):
   def func_wrapper(*args, **kwargs):
       return "<p>{0}</p>".format(func(*args, **kwargs))
   return func_wrapper

# decorador com parametros no decorador em funcao
def tags(tag_name):
    def tags_decorator(func):
        def func_wrapper(name):
            return "<{0}>{1}</{0}>".format(tag_name, func(name))
        return func_wrapper
    return tags_decorator


class Base(object):
    def __init__(self, name, alias):
        self.name = name
        self.alias = alias

    # decorador em classe, metodo sem parametro
    def _decorator1(func):
        def magic(self) :
            print("start magic")
            print(func(self))
            print("end magic")
        return magic

    # decorador em classe, metodo parametros variaveis
    def wrapper(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            print("inside wrap")
            return func(self, *args, **kwargs)
        return wrap

    # decorado com decorador em classe
    @_decorator1
    def getNome2(self):
        return self.name

    # decorado com decorador em funcao sem parametro
    @upper_d
    def getNome(self):
        return self.name

    # decorado com decorador em funcao com parametros
    @p_decorate
    def getAlias(self, prefixo):
        return prefixo + ' ' + self.alias

class Teste(Base):
    def __init__(self, name, alias):
        super().__init__(name, alias)

# ref: https://stackoverflow.com/questions/1263451/python-decorators-in-classes
# ref: https://dev.to/apcelent/python-decorator-tutorial-with-example-529f
# ref: https://realpython.com/primer-on-python-decorators/#creating-singletons

class adecorator (object):
    def __init__ (self, *args, **kwargs):
        # store arguments passed to the decorator
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        def newf(*args, **kwargs):

            #the 'self' for a method function is passed as args[0]
            slf = args[0]

            # replace and store the attributes
            saved = {}
            for k,v in self.kwargs.items():
                if hasattr(slf, k):
                    saved[k] = getattr(slf,k)
                    setattr(slf, k, v)

            # call the method
            ret = func(*args, **kwargs)

            #put things back
            for k,v in saved.items():
                setattr(slf, k, v)

            return ret
        newf.__doc__ = func.__doc__
        return newf 

class myclass(object):
    def __init__(self):
        self.property = "HELLO"

    @adecorator(property="GOODBYE")
    def method(self):
        print(self.property)


class RPC_CALL(object):
    def __init__(self, nome_metodo):
        self.nome_metodo = nome_metodo

    def __call__(self, *args, **kargs):

        if self.nome_metodo == 'setNames':
            execute = 'comando:{0} parametros:{1}'.format(self.nome_metodo, str(args)) 
            return execute

        raise AttributeError()

        #return "TESTE _Z! {0} -> {1}".format(self.parametro, str(args))


class ProxyObject(object):
    def __init__(self):
        pass

    # chama uma classe como metodo do call
    def __getattr__(self, name):
        return RPC_CALL(name)

    # cria um atributo novo
    def __setattr__(self, name, value):
        self.__dict__[name] = value
       
if __name__ == '__main__':
    
    g = ProxyObject()
    print(g.setNames('nome', 'dados'))
    print(g.teste())


    # b = Base('pagotto','locutus')

    # print(b.getNome())
    # print(b.getAlias('Sr.'))
    # print(b.getNome2())

    # t =Teste('teste','none')
    # print(t.getNome())
    # print(t.getAlias('Coisa'))
    # print(b.getNome2())
