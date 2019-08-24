# Decorador em função simples

#### Refs: 
- https://www.datacamp.com/community/tutorials/decorators-python (Decorador em função simples)
- https://www.thecodeship.com/patterns/guide-to-python-function-decorators/ (Decorador em Classes)
- https://stackoverflow.com/questions/1263451/python-decorators-in-classes

## Decorador Primitivo
```python
# funcao decoradora
def f_upper_d(func):
    def wrapper():
        return func().upper()
    return wrapper

# funcao a ser decorada
def say_yo():
    return 'what\'s up!!!'

# metodo primitivo
decorate = f_upper_d(say_yo)
result = decorate()

print(result)
```
Saida
```bash
WHATS UP!!!
```

## Decorador Usual
```python
# funcao decoradora
def f_upper_d(func):
    def wrapper():
        return func().upper()
    return wrapper

# decoração usual funcao say_yo
@f_upper_d
def say_yo():
    return 'what\'s up!!!'

@f_upper_d
def say_hi():
    return 'hello there'

print(say_yo())
print(say_hi())

```
Saida
```bash
HELLO THERE
WHATS UP!!!
```
## Decoração multipla
```python
# funcao decoradora 1
def f_upper_d(func):
    def wrapper():
        return func().upper()
    return wrapper

# funcao decoradora 2
def f_split_string_d(function):
    def wrapper():
        return function().split()
    return wrapper

# chamada encadeada (ordem é importante)
@f_split_string_d
@f_upper_d
def say_hi():
    return 'hello there'

@f_upper_d
def say_yo():
    return 'whats up!!!'

print(say_hi())
print(say_yo())
```
Saida
```bash
['HELLO', 'THERE']
WHATS UP!!!
```
## Decoração com argumentos
```python
# função decoradora com argumentos
def decorator_with_arguments(function):
    def wrapper_accepting_arguments(arg1, arg2):
        print("My arguments are: {0}, {1}".format(arg1,arg2))
        function(arg1, arg2)
    return wrapper_accepting_arguments

# função decirada
@decorator_with_arguments
def cities(city_one, city_two):
    print("Cities I love are {0} and {1}".format(city_one, city_two))

# teste
print(cities('londres','atlanta'))
        
```
Saida
```bash
My arguments are: londres, atlanta
Cities I love are londres and atlanta
None
```

## Decoração em função com argumentos variaveis
```python
# decorador permite função decorada aceitar numero variavel de argumentos
def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    def a_wrapper_accepting_arbitrary_arguments(*args,**kwargs):
        print('The positional arguments are', args)
        print('The keyword arguments are', kwargs)
        function_to_decorate(*args, **kwargs)
    return a_wrapper_accepting_arbitrary_arguments

# função decorada sem argumentos
@a_decorator_passing_arbitrary_arguments
def funcao_sem():
    print('nao tenho')

# função decorada com varios argumentos
@a_decorator_passing_arbitrary_arguments
def funcao_com(nome, idade, sexo, altura):
    print('nome: {0} idade {1}'.format(nome, idade))

funcao_sem()
funcao_com('jose', 50, sexo=False, altura=1.70)
```
Saida
```bash
The positional arguments are ()
The keyword arguments are {}
nao tenho
The positional arguments are ('jose', 50)
The keyword arguments are {'sexo': False, 'altura': 1.7}
nome: jose idade 50
```

## Decoração em função com argumentos variaveis
```python
# decorador com argumentos e funcção com argumentos
def decorator_maker_with_arguments(decorator_arg1, decorator_arg2, decorator_arg3):
    def decorator(func):
        def wrapper(function_arg1, function_arg2, function_arg3) :
            "This is the wrapper function"
            print("The wrapper can access all the variables\n"
                "\t- from the decorator maker: {0} {1} {2}\n"
                "\t- from the function call: {3} {4} {5}\n"
                "and pass them to the decorated function"
                .format(decorator_arg1, decorator_arg2,decorator_arg3,
                        function_arg1, function_arg2,function_arg3))
            return func(function_arg1, function_arg2,function_arg3)

        return wrapper

    return decorator

pandas = "Pandas"

# decorada passando argumentos no decorador e na função
@decorator_maker_with_arguments(pandas, "Numpy", "Scikit-learn")
def decorated_function_with_arguments(function_arg1, function_arg2,function_arg3):
    print("This is the decorated function and it only knows about its arguments: {0}"
        " {1}" " {2}".format(function_arg1, function_arg2,function_arg3))

# saida
decorated_function_with_arguments(pandas, "Science", "Tools")

```
Saida
```bash
The wrapper can access all the variables
        - from the decorator maker: Pandas Numpy Scikit-learn
        - from the function call: Pandas Science Tools
and pass them to the decorated function
This is the decorated function and it only knows about its arguments: Pandas Science Tools
```

## Questores de Debug
```python
from functools import wraps

def tags(tag_name):
    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(name):
            return "<{0}>{1}</{0}>".format(tag_name, func(name))
        return func_wrapper
    return tags_decorator

@tags("p")
def get_text(name):
    """returns some text"""
    return "Hello "+name

print(get_text.__name__) # get_text
print(get_text.__doc__) # returns some text
print(get_text.__module__) # __main__
```

# Decorador em Classes

## Decorador como metodo fora de classe

```python
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

if __name__ == '__main__':
    
    b = Base('pagotto','locutus')
    print(b.getNome())
    print(b.getAlias('Sr.'))
    print(b.getNome2())

    t =Teste('teste','none')
    print(t.getNome())
    print(t.getAlias('Coisa'))
    print(b.getNome2())
```
Saida
```bash
PAGOTTO
<p>Sr. locutus</p>
start magic
pagotto
end magic
None
TESTE
<p>Coisa none</p>
start magic
pagotto
end magic
None
```