"""
MÓDULO: lexer.py
PROYECTO FINAL: COMPILADORES - FASE 1
"""
 
import re
from typing import List, Tuple, NamedTuple
 
# ==============================================================================
# 1. ESTRUCTURAS DE DATOS
# ==============================================================================
 
class Token(NamedTuple):
    """Estructura para representar un Token detectado."""
    type: str
    value: str
    line: int
    column: int
 
class LexicalError(NamedTuple):
    """Estructura para representar un error léxico detectado."""
    message: str
    char: str
    line: int
    column: int
 
# ==============================================================================
# 2. CLASE PRINCIPAL DEL ANALIZADOR LÉXICO
# ==============================================================================
 
class Lexer:
    """
    Analizador Léxico (Scanner).
    Transforma una cadena de código fuente en una lista de Tokens y Errores Léxicos.
    """
 
    # Palabras reservadas -> tipo de token. El patrón KEYWORD se genera a partir de este mapa,
    # así hay un solo lugar donde agregar o quitar palabras.
    KEYWORD_MAP = {
        'int':    'PR_INT',
        'float':  'PR_FLOAT',
        'if':     'PR_IF',
        'else':   'PR_ELSE',
        'while':  'PR_WHILE',
        'return': 'PR_RETURN',
        'void':   'PR_VOID',
        'true':   'PR_TRUE',
        'false':  'PR_FALSE',
    }
 
    # Python usa el PRIMER patrón que coincide, por eso el orden importa.
    TOKEN_SPECIFICATION = [
        # --- ELEMENTOS A IGNORAR / ESPACIOS ---
        ('NEWLINE',        r'\n'),
        ('SKIP',           r'[ \t\r]+'),
 
        # --- COMENTARIOS (antes de los operadores para que '//' y '/*' no sean '/') ---
        ('COMMENT_SINGLE', r'//[^\n]*'),
        ('COMMENT_MULTI',  r'/\*[\s\S]*?\*/'),
        ('UNTERMINATED_COMMENT', r'/\*[\s\S]*'),   # '/*' sin su '*/'
 
        # --- LITERALES ---
        ('FLOAT_LITERAL',  r'\d+\.\d+'),
        ('INT_LITERAL',    r'\d+'),
        ('STRING_LITERAL', r'"[^"\n]*"'),
        ('UNTERMINATED_STRING', r'"[^"\n]*'),      # comilla sin cerrar: llega hasta el fin de la línea
 
        # --- PALABRAS RESERVADAS E IDENTIFICADORES ---
        ('KEYWORD',        r'\b(?:' + '|'.join(KEYWORD_MAP) + r')\b'),
        ('ID',             r'[a-zA-Z_][a-zA-Z_0-9]*'),
 
        # --- OPERADORES Y DELIMITADORES ---
        ('OP_REL',         r'==|!=|<=|>=|<|>'),
        ('OP_ASSIGN',      r'='),
        ('OP_ARITH',       r'\+|-|\*|/'),
        ('DELIM_LPAREN',   r'\('),
        ('DELIM_RPAREN',   r'\)'),
        ('DELIM_LBRACE',   r'\{'),
        ('DELIM_RBRACE',   r'\}'),
        ('DELIM_COMMA',    r','),
        ('DELIM_SEMICOLON',r';'),
 
        # --- CAPTURA DE ERRORES ---
        ('MISMATCH',       r'.'),
    ]
 
    def __init__(self, code: str):
        self.code = code
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.TOKEN_SPECIFICATION)
        self.regex = re.compile(tok_regex)
 
    def tokenize(self) -> Tuple[List[Token], List[LexicalError]]:
        """
        Procesa el código fuente completo y retorna una tupla con:
        - Lista de Tokens válidos
        - Lista de Errores Léxicos encontrados
        El análisis nunca se detiene ante un error: lo registra y continúa.
        """
        tokens: List[Token] = []
        errors: List[LexicalError] = []
 
        line_num = 1
        line_start = 0   # índice del texto donde empieza la línea actual
 
        for mo in self.regex.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()
            position = mo.start()
            col_num = position - line_start + 1
 
            if kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
 
            elif kind in ('SKIP', 'COMMENT_SINGLE'):
                continue
 
            elif kind in ('COMMENT_MULTI', 'UNTERMINATED_COMMENT'):
                if kind == 'UNTERMINATED_COMMENT':
                    errors.append(LexicalError("Comentario multilínea sin cerrar '/*'", '/*', line_num, col_num))
                # El comentario puede abarcar varias líneas: hay que actualizar la línea actual
                # y el inicio de la línea (justo después del ÚLTIMO salto de línea del comentario).
                newlines = value.count('\n')
                if newlines > 0:
                    line_num += newlines
                    line_start = position + value.rfind('\n') + 1
 
            elif kind == 'KEYWORD':
                tokens.append(Token(self.KEYWORD_MAP[value], value, line_num, col_num))
 
            elif kind == 'UNTERMINATED_STRING':
                # No se toca el contador de líneas: el salto de línea que sigue lo cuenta NEWLINE.
                errors.append(LexicalError(f"Cadena sin cerrar '{value}'", value, line_num, col_num))
 
            elif kind == 'MISMATCH':
                errors.append(LexicalError(f"Carácter no reconocido '{value}'", value, line_num, col_num))
 
            else:
                tokens.append(Token(kind, value, line_num, col_num))
 
        return tokens, errors
 