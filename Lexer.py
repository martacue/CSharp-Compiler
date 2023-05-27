# coding: utf-8

from sly import Lexer
import os
import re
import sys

class ComentarioBloque(Lexer):
    tokens = {}
        
    @_(r'\*\/')
    def CERRAR_COMENTARIO(self, t):
        self.begin(CSharpLexer)
    
    @_(r"\n")
    def SALTO_LINEA(self, t):
        self.lineno += 1

    @_(r'\/\*')
    def ERROR(self, t):
        print("eror comment")
        self.begin(CSharpLexer)
        return t
    
    @_(r'.')
    def COMENTARIO(self, t):
        pass
        

class CadenaTexto(Lexer):
    tokens = {}
    _caracteres = ""
    @_(r'"')
    def STR_CONST(self, t):
        t.value = self._caracteres
        t.value = f'"{t.value}"' # Anhadir comillas dobles al inicio y al final
        self._caracteres = ""
        self.begin(CSharpLexer)
        return t
    
    @_(r'.')
    def caracter(self, t):
        self._caracteres += t.value
    

class CSharpLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID, RETURN,
              ELSE, IF, CASE, CLASS, MODIFIER, USING, STATIC, NAMESPACE,
              VOID, NEW, IN, DEFAULT, CASE, BREAK, SWITCH,
              WHILE, FOREACH, FLOAT_CONST, STR_CONST, ASSIGN, FUNCT, ARROW,
              EQUALS, DIFFERENT, LE, AND, OR}
    
    FLOAT_CONST = r'\d+\.\d+'
    INT_CONST = r'\d+'
    
    @_(r'true|false')
    def BOOL_CONST(self, t):
        if t.value[0] == 't':
            t.value = True
        else:
            t.value = False
        return t
    
    EQUALS = r'=='
    DIFFERENT = r'!='
    LE = r'<='
    AND = r'&&'
    OR = r'\|\|'
    ARROW = r'=>'
    ASSIGN = r'='
    ignore = '\t '
    literals = {':',';', '(', ')', '{','}','+','<','>', '-','~','*','@','_',',','.','=','/','"','\\', '?', '!'}
    
    ELSE = r'\belse\b'
    IF = r'\bif\b'
    CLASS = r'\bclass\b'
    NEW = r'\bnew\b'
    WHILE = r'\bwhile\b'
    USING = r'\busing\b'
    VOID = r'\bvoid\b'
    NAMESPACE = r'\bnamespace\b'
    IN = r'\bin\b'
    FOREACH = r'\bforeach\b'
    STATIC = r'\bstatic\b'
    MODIFIER = r'\bpublic\b|\bprivate\b|\bprotected\b'
    RETURN = r'\breturn\b'
    SWITCH = r'\bswitch\b'
    CASE = r'\bcase\b'
    DEFAULT = r'\bdefault\b'
    BREAK = r'\bbreak\b'
    FUNCT = r'\bFunct\b'
    TYPEID = r'int\[\]|float\[\]|string\[\]|int|float|string|[A-Z][\w_]*'
    OBJECTID = r'[a-z][\w_]*' 
    
    @_(r'"')
    def COMILLA(self, t):
        self.begin(CadenaTexto)
        
    @_(r'\/\/.*')
    def COMENTARIO_LINEA(self, t):
        pass
    
    @_(r'\/\*')
    def COMENTARIO_BLOQUE(self, t):
        self.begin(ComentarioBloque)
        
    @_(r'\n')
    def SALTO_LINEA(self, t):
        self.lineno += 1
    
    @_(r'\r\n')
    def SALTO_LINEA(self, t):
        self.lineno += 1 
        
    @_(r'\s+')
    def ESPACIO(self, t):
        pass
    
    def ERROR(self, t):
        self.begin(CSharpLexer)
        return t
    
        

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                          for i in ['0', '1']
                          for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]


    def salida(self, texto):
        list_strings = []
        lexer = CSharpLexer()
        for token in lexer.tokenize(texto):
            result = f'#{token.lineno} {token.type} '
            if token.type == 'OBJECTID':
                result += f"{token.value}"
            elif token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'TYPEID':
                result += f"{str(token.value)}"
            elif token.type == 'MODIFIER':
                result += f"{token.value}"
            elif token.type in self.literals:
                result = f'#{token.lineno} \'{token.type}\''
            elif token.type == 'STR_CONST':
                result += token.value
            elif token.type == 'INT_CONST':
                result += str(token.value)
            elif token.type == 'FLOAT_CONST':
                result += str(token.value)
            elif token.type == 'ERROR':
                result = f'#{token.lineno} {token.type} {token.value}'
            else:
                result = f'#{token.lineno} {token.type}'

            list_strings.append(result)
        return list_strings
    

a = "suma(3,4);"
o = CSharpLexer()
print(o.salida(a))