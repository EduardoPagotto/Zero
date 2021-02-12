'''
Created on 20190823
Update on 20210212
@author: Eduardo Pagotto
'''

ADDRESS = 'unix:./uds_test_rpc'
#ADDRESS = 'tcp://127.0.0.1:5151'
TESTE_BUS_NAME = 'com.teste'
IS_ALIVE_INTERFACE = TESTE_BUS_NAME + '.is_alive_bitch'
SET_NOME_INTERFACE = TESTE_BUS_NAME + '.setNome'
GET_NOME_INTERFACE = TESTE_BUS_NAME + '.getNome'
GET_DICIONARIO_INTERFACE = TESTE_BUS_NAME + '.get_dict'
