


if __name__ == '__main__':

    lista = [1,2,3,4,5,6,7,8,9]
    #lista = []

    for item in reversed(lista):
        if item in [1,3,5,6,7,9]:
            lista.remove(item)
            del item




    print(str(lista))