'''
Created on 20190821
Update on 20200517
@author: Eduardo Pagotto
'''

#pylint: disable=C0301, C0116, W0703, C0103, C0115

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

# ref: https://www.jsonrpc.org/specification#error_object
# -32000 to -32099	Server error	Reserved for implementation-defined server-errors.
class ExceptionZeroRPC(ExceptionZero):
    '''Exception gerenciada'''
    def __init__(self, *args, **kwargs):
        ExceptionZero.__init__(self, *args, **kwargs)
