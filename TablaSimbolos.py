class TablaSimbolos():
    def __init__(self):
        self.ambitos = list()
        self.namespaces = list()
        self.clases = list()
        self.metodos = list()
        self.atributos = list()
        
    def addClass(self, nombreClase, padre):
        pass
        
    def addMethod(self,nombreMetodo,nombreClase,formales,tipo):
        pass
    
    def addAttribute(self, attribute):
        pass
    
    def construyeArbol(self, nodo):
        pass
        
    
    def enterScope(self):
        diccionario = dict()
        self.ambitos.append(diccionario)
    
    def findSymbol(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito.get(nombre)
        
        return None
    
    def addSymbol(self, nombre, tipo):
        self.ambitos[-1][nombre] = tipo #PREGUNTAR: guardar el valor?
        
    def checkScope(self, nombre):
        for ambito in reversed(self.Ambitos):
            if nombre in ambito:
                return True
        
        return False
    
    def exitScope(self):
        self.ambitos.pop()
    
        
class Arbol():
    def __init__(self, nombreClase, padre):
        self.listahijos = list()
        self.padre = padre
        self.nombreClase = nombreClase

                