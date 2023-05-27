# coding: utf-8

from Lexer import CSharpLexer
from sly import Parser
import sys
import os
from Clases import *


class CSharpParser(Parser):
    nombre_fichero = ''
    tokens = CSharpLexer.tokens
    debugfile = "salida.out"
    errores = []
    precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'DIFFERENT'),
    ('nonassoc', 'LE'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', '!')
    )

    @_('namespace_declarations')
    def program(self, p):
        return Programa(linea=p.lineno, usings=[], secuencia=p.namespace_declarations)

    @_('using_directives namespace_declarations')
    def program(self, p):
        return Programa(linea=p.lineno, usings=p.using_directives, secuencia=p.namespace_declarations)

    @_('USING TYPEID')
    def using_directive(self, p):
        return Using(linea=p.lineno, nombre=p.TYPEID)
    
    @_('using_directive using_directives')
    def using_directives(self, p):
        return p.using_directives + [p.using_directive]
    
    @_('using_directive ";"')
    def using_directives(self, p):
        return [p.using_directive]
    
    @_('NAMESPACE TYPEID "{" clases "}"')
    def namespace_declaration(self, p):
        return Namespace(linea=p.lineno, nombre=p.TYPEID, clases=p.clases)
    
    @_('namespace_declarations namespace_declaration')
    def namespace_declarations(self, p):
        return p.namespace_declarations + [p.namespace_declaration]
    
    @_('namespace_declaration')
    def namespace_declarations(self, p):
        return [p.namespace_declaration]
    
    @_('CLASS TYPEID "{" atributos metodos "}"')
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID, padre="Object", atributos=p.atributos, metodos=p.metodos, 
                     nombre_fichero=self.nombre_fichero)
    
    @_('CLASS error "{" atributos metodos "}"')
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.error, padre="Object", atributos=p.atributos, metodos=p.metodos, 
                     nombre_fichero=self.nombre_fichero)
    
    @_('CLASS TYPEID ":" TYPEID "{" atributos metodos "}"')
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID0, padre=p.TYPEID1 ,atributos=p.atributos, metodos=p.metodos, 
                     nombre_fichero=self.nombre_fichero)
    
    @_('CLASS TYPEID "{" atributos "}"')
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID, padre="Object", atributos=p.atributos, metodos=[], 
                     nombre_fichero=self.nombre_fichero)

    @_('CLASS TYPEID ":" TYPEID "{" atributos "}"')
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID0, padre=p.TYPEID1 ,atributos=p.atributos, metodos=[], 
                     nombre_fichero=self.nombre_fichero)

    @_('CLASS TYPEID ":" error "{" atributos "}"')
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID, padre=p.error ,atributos=p.atributos, metodos=[], 
                     nombre_fichero=self.nombre_fichero)
    
    @_('CLASS TYPEID "{" metodos "}"')
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID, padre="Object", atributos=[], metodos=p.metodos, 
                     nombre_fichero=self.nombre_fichero)
    
    @_('CLASS TYPEID ":" TYPEID "{" metodos "}"')
    def clase(self, p):
        return Clase(linea=p.lineno, nombre=p.TYPEID0, padre=p.TYPEID1 ,atributos=[], metodos=p.metodos, 
                     nombre_fichero=self.nombre_fichero)
    
    @_('clases clase')
    def clases(self, p):
        return p.clases + [p.clase]
    
    @_('clase')
    def clases(self, p):
        return [p.clase]
    
    @_('MODIFIER TYPEID OBJECTID ";"')
    def atributo(self, p):
        return Atributo(linea=p.lineno, nombre=p.OBJECTID, modificador=p.MODIFIER, tipo=p.TYPEID, cuerpo=NoExpr())
    
    @_('MODIFIER TYPEID OBJECTID ASSIGN expr ";"')
    def atributo(self, p):
        return Atributo(linea=p.lineno, nombre=p.OBJECTID, modificador=p.MODIFIER, tipo=p.TYPEID, cuerpo=p.expr)
    
    @_('atributos atributo')
    def atributos(self, p):
        return p.atributos + [p.atributo]
    
    @_('atributo')
    def atributos(self, p):
        return [p.atributo]
    
    @_('MODIFIER TYPEID OBJECTID "(" ")" "{" expr "}"')
    def metodo(self, p):
        return Metodo(linea=p.lineno, nombre=p.OBJECTID, modificador=p.MODIFIER, tipo=p.TYPEID, formales=[], 
                      estatico=False, cuerpo=p.expr)
    
    @_('MODIFIER STATIC TYPEID OBJECTID "(" ")" "{" expr "}"')
    def metodo(self, p):
        return Metodo(linea=p.lineno, nombre=p.OBJECTID, modificador=p.MODIFIER, tipo=p.TYPEID, formales=[], 
                      estatico=True, cuerpo=p.expr)
    
    @_('MODIFIER TYPEID OBJECTID "(" formales ")" "{" expr "}"')
    def metodo(self, p):
        return Metodo(linea=p.lineno, nombre=p.OBJECTID, modificador=p.MODIFIER, tipo=p.TYPEID, formales=p.formales, 
                      estatico=False, cuerpo=p.expr)
    
    @_('MODIFIER STATIC TYPEID OBJECTID "(" formales ")" "{" expr "}"')
    def metodo(self, p):
        return Metodo(linea=p.lineno, nombre=p.OBJECTID, modificador=p.MODIFIER, tipo=p.TYPEID, formales=p.formales, 
                      estatico=True, cuerpo=p.expr)
    
    @_('MODIFIER VOID OBJECTID "(" ")" "{" expr "}"')
    def metodo(self, p):
        return Metodo(linea=p.lineno, nombre=p.OBJECTID, modificador=p.MODIFIER, tipo=p.VOID, formales=[], 
                      estatico=False, cuerpo=p.expr)
    
    @_('MODIFIER STATIC VOID OBJECTID "(" ")" "{" expr "}"')
    def metodo(self, p):
        return Metodo(linea=p.lineno, nombre=p.OBJECTID, modificador=p.MODIFIER, tipo=p.VOID, formales=[], 
                      estatico=True, cuerpo=p.expr)
    
    @_('MODIFIER TYPEID VOID "(" formales ")" "{" expr "}"')
    def metodo(self, p):
        return Metodo(linea=p.lineno, nombre=p.OBJECTID, modificador=p.MODIFIER, tipo=p.VOID, formales=p.formales, 
                      estatico=False, cuerpo=p.expr)
    
    @_('MODIFIER STATIC VOID OBJECTID "(" formales ")" "{" expr "}"')
    def metodo(self, p):
        return Metodo(linea=p.lineno, nombre=p.OBJECTID, modificador=p.MODIFIER, tipo=p.VOID, formales=p.formales, 
                      estatico=True, cuerpo=p.expr)
    
    @_('metodos metodo')
    def metodos(self, p):
        return p.metodos + [p.metodo]
    
    @_('metodo')
    def metodos(self, p):
        return [p.metodo]
    
    @_('TYPEID OBJECTID')
    def formal(self, p):
        return Formal(linea=p.lineno, nombre_variable=p.OBJECTID, tipo=p.TYPEID)
    
    @_('formales "," formal')
    def formales(self, p):
        return p.formales + [p.formal]

    @_('formales error formal')
    def formales(self, p):
        return p.formales + [p.error, p.formal]
    
    @_('formal')
    def formales(self, p):
        return [p.formal]
    
    @_('OBJECTID ASSIGN expr ";"')
    def expr(self, p):
        return Asignacion(linea=p.lineno, nombre=p.OBJECTID, cuerpo=p.expr)
    
    @_('TYPEID OBJECTID ASSIGN expr ";"')
    def expr(self, p):
        return NuevaVariable(linea=p.lineno, nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.expr)
    
    @_('OBJECTID "(" ")" ";"')
    def expr(self, p):
        return LlamadaMetodo(linea=p.lineno, nombre_metodo=p.OBJECTID, argumentos=[],
                             cuerpo=Objeto(nombre="self"))
    
    @_('expr "." OBJECTID "(" ")" ";"')
    def expr(self, p):
        return LlamadaMetodo(linea=p.lineno, nombre_metodo=p.OBJECTID, argumentos=[],
                             cuerpo=p.expr)

    @_('OBJECTID "(" exprApoyo1 ")" ";"')
    def expr(self, p):
        return LlamadaMetodo(linea=p.lineno, nombre_metodo=p.OBJECTID, argumentos=p.exprApoyo1,
                             cuerpo=Objeto(nombre="self"))
    
    @_('OBJECTID "(" exprApoyo1 ")"')
    def expr(self, p):
        return LlamadaMetodo(linea=p.lineno, nombre_metodo=p.OBJECTID, argumentos=p.exprApoyo1,
                             cuerpo=Objeto(nombre="self"))
    @_('expr "." OBJECTID "(" exprApoyo1 ")" ";"')
    def expr(self, p):
        return LlamadaMetodo(linea=p.lineno, nombre_metodo=p.OBJECTID, argumentos=p.exprApoyo1,
                             cuerpo=p.expr)
    
    @_('TYPEID "." OBJECTID "(" ")" ";"')
    def expr(self, p):
        return LlamadaMetodoEstatico(linea=p.lineno, clase=p.TYPEID ,nombre_metodo=p.OBJECTID, argumentos=[])
    
    @_('TYPEID "." OBJECTID "(" exprApoyo1 ")" ";"')
    def expr(self, p):
        return LlamadaMetodoEstatico(linea=p.lineno, clase=p.TYPEID ,nombre_metodo=p.OBJECTID, argumentos=p.exprApoyo1)
    
    @_('RETURN expr ";"')
    def expr(self, p):
        return Retorno(linea=p.lineno, cuerpo=p.expr)
    
    @_('IF "(" expr ")" "{" expr "}" ELSE "{" expr "}"')
    def expr(self, p):
        return Condicional(linea=p.lineno, condicion=p.expr0, verdadero=p.expr1, falso=p.expr2)
    
    @_('WHILE "(" expr ")" "{" expr "}"')
    def expr(self, p):
        return Bucle(linea=p.lineno, condicion=p.expr0, cuerpo=p.expr1)
    
    @_('FOREACH "(" TYPEID OBJECTID IN OBJECTID ")" "{" expr "}"')
    def expr(self, p):
        return BucleParaCada(linea=p.lineno, tipo=p.TYPEID, nombre_variable=p.OBJECTID0, 
                             coleccion=p.OBJECTID1, cuerpo=p.expr)
    
    @_('SWITCH "(" expr ")" "{" cases "}"')
    def expr(self, p):
        return Switch(linea=p.lineno, expr=p.expr, casos=p.cases)
    
    @_('CASE expr ":" expr BREAK ";"')
    def case(self, p):
        return RamaCase(linea=p.lineno, condicion=p.expr0, cuerpo=p.expr1)
    
    @_('DEFAULT ":" expr BREAK ";"')
    def case(self, p):
        return RamaDefault(linea=p.lineno, condicion=NoExpr() ,cuerpo=p.expr)
    
    @_('cases case')
    def cases(self, p):
        return p.cases + [p.case]
    
    @_('case')
    def cases(self, p):
        return [p.case]
    
    @_('FUNCT "<" TYPEID "," TYPEID ">" OBJECTID ASSIGN OBJECTID ARROW expr ";"')
    def expr(self, p):
        return Funcion(linea=p.lineno, tipo_parametro=p.TYPEID0, tipo_retorno=p.TYPEID1, nombre=p.OBJECTID0, 
                       parametro=p.OBJECTID1, cuerpo=p.expr)
    
    @_('"{" exprApoyo3 "}"')
    def expr(self, p):
        return Coleccion(linea=p.lineno, elementos=p.exprApoyo3)

    @_('expr "," expr')
    def exprApoyo3(self, p):
        return [p.expr0, p.expr1]
    
    @_('exprApoyo3 "," expr')
    def exprApoyo3(self, p):
        return p.exprApoyo3 + [p.expr]
    
    @_('NEW TYPEID "(" ")"')
    def expr(self, p):
        return Nueva(linea=p.lineno, tipo=p.TYPEID)
    
    @_('expr "+" expr')
    def expr(self, p):
        return Suma(linea=p.lineno, izquierda=p.expr0, derecha=p.expr1)
    
    @_('expr "-" expr')
    def expr(self, p):
        return Resta(linea=p.lineno, izquierda=p.expr0, derecha=p.expr1)
    
    @_('expr "*" expr')
    def expr(self, p):
        return Multiplicacion(linea=p.lineno, izquierda=p.expr0, derecha=p.expr1)
    
    @_('expr "/" expr')
    def expr(self, p):
        return Division(linea=p.lineno, izquierda=p.expr0, derecha=p.expr1)
    
    @_('"!" expr')
    def expr(self, p):
        return Not(linea=p.lineno, expr=p.expr)
    
    @_('expr EQUALS expr')
    def expr(self, p):
        return Igual(linea=p.lineno, izquierda=p.expr0, derecha=p.expr1)
    
    @_('expr DIFFERENT expr')
    def expr(self, p):
        return Distinto(linea=p.lineno, izquierda=p.expr0, derecha=p.expr1)
    
    @_('expr LE expr')
    def expr(self, p):
        return LeIgual(linea=p.lineno, izquierda=p.expr0, derecha=p.expr1)
    
    @_('expr AND expr')
    def expr(self, p):
        return And(linea=p.lineno, izquierda=p.expr0, derecha=p.expr1)
    
    @_('expr OR expr')
    def expr(self, p):
        return Or(linea=p.lineno, izquierda=p.expr0, derecha=p.expr1)
    
    @_('OBJECTID')
    def expr(self, p):
        return Objeto(linea=p.lineno, nombre=p.OBJECTID)
    
    @_('INT_CONST')
    def expr(self, p):
        return Entero(linea=p.lineno, valor=p.INT_CONST)
    
    @_('FLOAT_CONST')
    def expr(self, p):
        return Flotante(linea=p.lineno, valor=p.FLOAT_CONST)
    
    @_('STR_CONST')
    def expr(self, p):
        return String(linea=p.lineno, valor=p.STR_CONST)
    
    @_('BOOL_CONST')
    def expr(self, p):
        return Booleano(linea=p.lineno, valor=p.BOOL_CONST)

    @_('expr expr')
    def exprApoyo2(self, p):
        return [p.expr0] + [p.expr1]
    
    @_('exprApoyo2 expr')
    def exprApoyo2(self, p):
        return p.exprApoyo2 + [p.expr]
    
    @_('exprApoyo2')
    def expr(self, p):
        return Bloque(linea=p.lineno, expresiones=p.exprApoyo2)
    
    @_('exprApoyo1 "," expr')
    def exprApoyo1(self, p):
        return p.exprApoyo1 + [p.expr]
    
    @_('expr')
    def exprApoyo1(self, p):
        return [p.expr]

    def error(self, token):
        if token is not None:
            if token.type in ['TYPEID', 'OBJECTID', 'INT_CONST']:
                self.errores.append(f'"{self.nombre_fichero}", line {token.lineno}: syntax error at or near {token.type} = {token.value}')
            elif token.type in ['CASE', 'DARROW', 'IF', 'ELSE', 'LE']:
                self.errores.append(f'"{self.nombre_fichero}", line {token.lineno}: syntax error at or near {token.type}')
            else:
                self.errores.append(f'"{self.nombre_fichero}", line {token.lineno}: syntax error at or near \'{token.value}\'')
        else:
            self.errores.append(f'"{self.nombre_fichero}", line 0: syntax error at or near EOF')
