# coding: utf-8
from dataclasses import dataclass, field
from typing import List
from TablaSimbolos import TablaSimbolos


@dataclass
class Nodo:
    linea: int = 0

    def str(self, n):
        return f'{n*" "}#{self.linea}\n'


@dataclass
class Formal(Nodo):
    nombre_variable: str = '_no_set'
    tipo: str = '_no_type'
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_formal\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        return resultado


class Expresion(Nodo):
    cast: str = '_no_type'


@dataclass
class Asignacion(Expresion):
    nombre: str = '_no_set'
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_assign\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class LlamadaMetodoEstatico(Expresion):
    clase: str = '_no_type'
    nombre_metodo: str = '_no_set'
    argumentos: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_static_dispatch\n'
        resultado += f'{(n+2)*" "}{self.clase}\n'
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: _no_type\n'
        return resultado


@dataclass
class LlamadaMetodo(Expresion):
    cuerpo: Expresion = None
    nombre_metodo: str = '_no_set'
    argumentos: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_dispatch\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Condicional(Expresion):
    condicion: Expresion = None
    verdadero: Expresion = None
    falso: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_cond\n'
        resultado += self.condicion.str(n+2)
        resultado += self.verdadero.str(n+2)
        resultado += self.falso.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Bucle(Expresion):
    condicion: Expresion = None
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_loop\n'
        resultado += self.condicion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

@dataclass
class BucleParaCada(Expresion):
    nombre_variable: str = '_no_set'
    tipo: str = '_no_type'
    coleccion: str = '_no_set'
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_for\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n+2)*" "}{self.coleccion}\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

@dataclass
class Retorno(Expresion):
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_return\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

@dataclass
class Bloque(Expresion):
    expresiones: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado = f'{n*" "}_block\n'
        resultado += ''.join([e.str(n+2) for e in self.expresiones])
        resultado += f'{(n)*" "}: {self.cast}\n'
        resultado += '\n'
        return resultado
    
    def Tipo(self, Ambito): # TODO: Implementar
        pass 


@dataclass
class RamaCase(Nodo):
    condicion: Expresion = None
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_branch\n'
        resultado += self.condicion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        return resultado
    
@dataclass
class RamaDefault(Nodo):
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_branch\n'
        resultado += self.cuerpo.str(n+2)
        return resultado


@dataclass
class Switch(Expresion):
    expr: Expresion = None
    casos: List[RamaCase] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_typcase\n'
        resultado += self.expr.str(n+2)
        resultado += ''.join([c.str(n+2) for c in self.casos])
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

@dataclass
class Funcion(Expresion):
    tipo_parametro: str = '_no_type'
    tipo_retorno: str = '_no_type'
    nombre: str = '_no_set'
    parametro: str = '_no_set'
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_def\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo_parametro}\n'
        resultado += f'{(n+2)*" "}{self.tipo_retorno}\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
@dataclass
class Coleccion(Expresion):
    elementos: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_list\n'
        resultado += ''.join([e.str(n+2) for e in self.elementos])
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

@dataclass
class Nueva(Expresion):
    tipo: str = '_no_set'
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_new\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        if self.tipo in [clase[0] for clase in Ambito.clases]:
            self.cast = self.tipo
        else:
            print(f'Error: Tipo {self.tipo} no definido')



@dataclass
class OperacionBinaria(Expresion):
    izquierda: Expresion = None
    derecha: Expresion = None


@dataclass
class Suma(OperacionBinaria):
    operando: str = '+'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_plus\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.izquierda.Tipo(Ambito)
        self.derecha.Tipo(Ambito)
        tipos_validos = ['int', 'float']
        if self.izquierda.cast in tipos_validos and self.izquierda.cast == self.derecha.cast:
            self.cast = self.izquierda.cast
        else:
            print('Error +: Los tipos no coinciden o no son validos')


@dataclass
class Resta(OperacionBinaria):
    operando: str = '-'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_sub\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.izquierda.Tipo(Ambito)
        self.derecha.Tipo(Ambito)
        tipos_validos = ['int', 'float']
        if self.izquierda.cast in tipos_validos and self.izquierda.cast == self.derecha.cast:
            self.cast = self.izquierda.cast
        else:
            print('Error -: Los tipos no coinciden o no son validos')


@dataclass
class Multiplicacion(OperacionBinaria):
    operando: str = '*'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_mul\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.izquierda.Tipo(Ambito)
        self.derecha.Tipo(Ambito)
        tipos_validos = ['int', 'float']
        if self.izquierda.cast in tipos_validos and self.izquierda.cast == self.derecha.cast:
            self.cast = self.izquierda.cast
        else:
            print('Error *: Los tipos no coinciden o no son validos')



@dataclass
class Division(OperacionBinaria):
    operando: str = '/'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_divide\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.izquierda.Tipo(Ambito)
        self.derecha.Tipo(Ambito)
        tipos_validos = ['int', 'float']
        if self.izquierda.cast in tipos_validos and self.izquierda.cast == self.derecha.cast:
            self.cast = self.izquierda.cast
        else:
            print('Error /: Los tipos no coinciden o no son validos')


@dataclass
class LeIgual(OperacionBinaria):
    operando: str = '<='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_leq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.izquierda.Tipo(Ambito)
        self.derecha.Tipo(Ambito)
        tipos_validos = ['int', 'float']
        if self.izquierda.cast in tipos_validos and self.izquierda.cast == self.derecha.cast:
            self.cast = 'bool'
        else:
            print('Error <=: Los tipos no coinciden o no son validos')


@dataclass
class Igual(OperacionBinaria):
    operando: str = '=='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_eq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.izquierda.Tipo(Ambito)
        self.derecha.Tipo(Ambito)
        if self.izquierda.cast == self.derecha.cast:
            self.cast = 'bool'
        else:
            print('Error ==: Los tipos no coinciden')

@dataclass
class Distinto(OperacionBinaria):
    operando: str = '!='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_neq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.izquierda.Tipo(Ambito)
        self.derecha.Tipo(Ambito)
        if self.izquierda.cast == self.derecha.cast:
            self.cast = 'bool'
        else:
            print('Error !=: Los tipos no coinciden')

@dataclass
class Not(Expresion):
    expr: Expresion = None
    operador: str = '!'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_comp\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.expr.Tipo(Ambito)
        if self.expr.cast == 'bool':
            self.cast = 'bool'
        else:
            print('Error not: La expresion no es booleana')

@dataclass
class And(OperacionBinaria):
    operando: str = '&&'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_and\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.izquierda.Tipo(Ambito)
        self.derecha.Tipo(Ambito)
        if self.izquierda.cast == 'bool' and self.derecha.cast == 'bool':
            self.cast = 'bool'
        else:
            print('Error and: Los tipos de las expresiones no son booleanos')
    
@dataclass
class Or(OperacionBinaria):
    operando: str = '||'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_or\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self, Ambito):
        self.izquierda.Tipo(Ambito)
        self.derecha.Tipo(Ambito)
        if self.izquierda.cast == 'bool' and self.derecha.cast == 'bool':
            self.cast = 'bool'
        else:
            print('Error or: Los tipos de las expresiones no son booleanos')


@dataclass
class Objeto(Expresion):
    nombre: str = '_no_set'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_object\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        if Ambito.checkScope(self.nombre):
            self.cast = Ambito.findSymbol(self.nombre)
        else:
            print(f'Error: El objeto {self.nombre} no existe en el ambito actual')


@dataclass
class NoExpr(Expresion):
    nombre: str = ''

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_no_expr\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self):
        pass


@dataclass
class Entero(Expresion):
    valor: int = 0

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_int\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.cast = 'int'


@dataclass
class String(Expresion):
    valor: str = '_no_set'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_string\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.cast = 'string'


@dataclass
class Flotante(Expresion):
    valor: float = 0.0

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_float\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.cast = 'float'


@dataclass
class Booleano(Expresion):
    valor: bool = False

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_bool\n'
        resultado += f'{(n+2)*" "}{1 if self.valor else 0}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self, Ambito):
        self.cast = 'bool'

@dataclass
class IterableNodo(Nodo):
    secuencia: List = field(default_factory=List)
    usings: List = field(default_factory=List)


class Programa(IterableNodo):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{" "*n}_program\n'
        resultado += ''.join([c.str(n+2) for c in self.usings])
        resultado += ''.join([c.str(n+2) for c in self.secuencia])
        return resultado
    
    def Tipo(self):
        Ambito = TablaSimbolos()
        for namespace in self.secuencia:
            Ambito.add_namespace(namespace)
            for clase in namespace.clases:
                Ambito.add_class(clase.nombre, clase.padre)
                for metodo in clase.metodos:
                    Ambito.add_method(metodo, clase.nombre)
                for atributo in clase.atributos:
                    Ambito.add_attribute(atributo, clase.nombre)
            
            # agrega los metodos y atributos de la clase padre que no esten en la clase hija
            for clase in namespace.clases:
                if clase.padre != 'Object':
                    copia_metodos = Ambito.metodos.copy()
                    for metodo in copia_metodos:
                        if metodo[1] == clase.padre and metodo[0].nombre not in [metodo.nombre for metodo in clase.metodos]:
                            Ambito.add_method(metodo[0], clase.nombre)
                    copia_atributos = Ambito.atributos.copy()
                    for atributo in copia_atributos:
                        if atributo[1] == clase.padre:
                            Ambito.add_attribute(atributo[0], clase.nombre)
        Ambito.construyeTotal()
        for namespace in self.secuencia:
            namespace.Tipo(Ambito)
                    



@dataclass
class Using(Nodo):
    nombre: str = '_no_set'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_using\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        return resultado
    
@dataclass
class Namespace(Nodo):
    nombre: str = '_no_set'
    clases: List = field(default_factory=List)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_namespace\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += ''.join([c.str(n+2) for c in self.clases])
        return resultado
    
    def Tipo(self, Ambito):
        for clase in self.clases:
            clase.Tipo(Ambito)

@dataclass
class Caracteristica(Nodo):
    nombre: str = '_no_set'
    tipo: str = '_no_set'
    cuerpo: Expresion = None
    modificador: str = '_no_set'


@dataclass
class Metodo(Caracteristica):
    formales: List[Formal] = field(default_factory=list)
    estatico: bool = False

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_method\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.modificador}\n'
        resultado += f'{(n+2)*" "}{"_static" if self.estatico else "_no_static"}\n'
        resultado += ''.join([c.str(n+2) for c in self.formales])
        resultado += f'{(n + 2) * " "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)

        return resultado
    
    def Tipo(self, Ambito):
        Ambito.enterScope()
        for formal in self.formales:
            Ambito.addSymbol(formal.nombre_variable, formal.tipo)      
        
        self.cuerpo.Tipo(Ambito)
        if self.cuerpo.cast != self.tipo:
            #error
            print("Error Metodo")
        Ambito.exitScope()

@dataclass
class Atributo(Caracteristica):

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_attr\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.modificador}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
    
    def Tipo(self, Ambito):
        self.cuerpo.Tipo(Ambito)
        if self.cuerpo.cast == self.tipo:
            Ambito.addSymbol(self.nombre, self.tipo)
        else:
            print("Error Atributo")

@dataclass
class Clase(Nodo):
    nombre: str = '_no_set'
    padre: str = '_no_set'
    nombre_fichero: str = '_no_set'
    atributos: List[Atributo] = field(default_factory=list)
    metodos: List[Metodo] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_class\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.padre}\n'
        resultado += f'{(n+2)*" "}"{self.nombre_fichero}"\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.atributos])
        resultado += ''.join([c.str(n+2) for c in self.metodos])
        resultado += '\n'
        resultado += f'{(n+2)*" "})\n'
        return resultado

    def Tipo(self, Ambito):
        Ambito.enterScope()
        for atributo in self.atributos:
            atributo.Tipo(Ambito)
        # anhadir al ambito los atributos del padre que no esten redefinidos
        for atributo in [atributo[0] for atributo in Ambito.atributos if atributo[1] == self.nombre and 
                         atributo[0].nombre not in [atributo.nombre for atributo in self.atributos]]:
            Ambito.addSymbol(atributo.nombre, atributo.tipo)
        for metodo in self.metodos:
            metodo.Tipo(Ambito)
        Ambito.exitScope()
        