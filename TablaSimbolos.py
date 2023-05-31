class TablaSimbolos():
    def __init__(self):
        self.ambitos = list()
        self.namespaces = dict()
        self.clases = list()
        self.metodos = list()
        self.atributos = list()
        self.arbol = Arbol()
        self.clase_actual = None

    def add_namespace(self, namespace):
        self.namespaces[namespace.nombre] = namespace

    def add_class(self, nombre_clase, nombre_padre):
        self.clases.append((nombre_clase, nombre_padre))
        
    def add_method(self, metodo, nombre_clase):
        self.metodos.append((metodo, nombre_clase))
    
    def encuentra_metodo(self, nombre_metodo, nombre_clase):
        for metodo in self.metodos:
            if metodo[0].nombre == nombre_metodo and metodo[1] == nombre_clase:
                return metodo
        return None
    
    def add_attribute(self, attribute, nombre_clase):
        self.atributos.append((attribute, nombre_clase))
    
    def construyeArbol(self, nodo):
        hijos = list()
        for clase in self.clases:
            if clase[1] == nodo.nombre:
                hijos.append(Nodo(clase[0], nodo))
        arboles = list()
        for hijo in hijos:
            arboles.append(self.construyeArbol(hijo))
        arboles.extend(nodo.hijos)
        raiz = Nodo(nodo.nombre, nodo.padre)
        raiz.anhade_hijos(arboles)
        return raiz
    
    def construyeTotal(self):
        self.arbol.raiz = self.construyeArbol(self.arbol.raiz)
        
    
    def enterScope(self):
        diccionario = dict()
        self.ambitos.append(diccionario)
    
    def findSymbol(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito.get(nombre)
        
        return None
    
    def addSymbol(self, nombre, tipo):
        self.ambitos[-1][nombre] = tipo
        
    def checkScope(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return True
        
        return False
    
    def exitScope(self):
        self.ambitos.pop()
    
        
class Nodo:
    def __init__(self, nombre, padre=None):
        self.nombre = nombre
        self.padre = padre
        self.hijos = []

    def anhade_hijo(self, nodo_hijo):
        self.hijos.append(nodo_hijo)

    def anhade_hijos(self, lista_hijos):
        self.hijos = lista_hijos

    def es_descendiente(self, ancestro):
        if self.padre is None:
            return False
        if self.nombre == ancestro or self.padre == ancestro:
            return True
        return self.padre.es_descendiente(ancestro)

    def __str__(self):
        if self.padre is None:
            return self.nombre
        return f"{self.nombre} : {self.padre}"

class Arbol:
    def __init__(self):
        self.raiz = Nodo("Object")
        self.primitivos = ["int", "float", "string", "bool"]

    def es_subtipo(self, clase1, clase2):
        if clase1 in self.primitivos and clase1 == clase2:
            return True
        if self.busca_clase(clase1) is None:
            raise ValueError(f"Class {clase1} not defined.")
        clase1_nodo = self.busca_clase(clase1)
        return clase1_nodo.es_descendiente(clase2)

    def es_primitivo(self, nombre_tipo):
        return nombre_tipo in self.primitivos
    
    def busca_clase(self, nombre_clase):
        return self.busca_clase_aux(nombre_clase, self.raiz)
    
    def busca_clase_aux(self, nombre_clase, nodo):
        if nodo.nombre == nombre_clase:
            return nodo
        for hijo in nodo.hijos:
            result = self.busca_clase_aux(nombre_clase, hijo)
            if result is not None:
                return result
        return None


    def __str__(self):
        return self._str_helper(self.raiz)

    def _str_helper(self, node, indent=0):
        result = "  " * indent + str(node) + "\n"
        for child in node.hijos:
            result += self._str_helper(child, indent + 1)
        return result

# Prueba del arbol
arbol = Arbol()
arbol.raiz.anhade_hijo(Nodo("A"))
arbol.raiz.anhade_hijo(Nodo("B"))
arbol.raiz.anhade_hijo(Nodo("C"))
arbol.raiz.hijos[0].anhade_hijo(Nodo("D", arbol.raiz.hijos[0]))
arbol.raiz.hijos[0].anhade_hijo(Nodo("E", arbol.raiz.hijos[0]))
arbol.raiz.hijos[0].hijos[0].anhade_hijo(Nodo("F", arbol.raiz.hijos[0].hijos[0]))
print(arbol.es_subtipo("E", "A"))
print(arbol)

                