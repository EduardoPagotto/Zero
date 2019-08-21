'''
Created on 20190821
Update on 20190821
@author: Eduardo Pagotto
'''

class ExceptionZero(Exception):
    '''Exception gerenciada'''
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class ExceptionZeroClose(ExceptionZero):
    '''Exception gerenciada'''
    def __init__(self, *args, **kwargs):
        ExceptionZero.__init__(self, *args, **kwargs)

class ExceptionZeroErro(ExceptionZero):
    '''Exception gerenciada'''
    def __init__(self, *args, **kwargs):
        ExceptionZero.__init__(self, *args, **kwargs)