
"""
MÓDULO: main.py
PROYECTO FINAL: COMPILADORES - FASE 1
Punto de entrada del programa: python main.py <archivo.txt>
"""
 
import sys
from lexer import Lexer
 
 
def formatear_token(tok) -> str:
    lexema = f"'{tok.value}'"
    return (f"[TOKEN] Tipo: {tok.type:<12} | Lexema: {lexema:<10} | "
            f"Posición: [Línea {tok.line}, Col {tok.column}]")
 
 
def formatear_error(err) -> str:
    return f"[ERROR LÉXICO] {err.message} en Posición: [Línea {err.line}, Col {err.column}]"
 
 
def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.txt>")
        sys.exit(1)
 
    filepath = sys.argv[1]
 
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"ERROR: Archivo '{filepath}' no encontrado.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"ERROR: '{filepath}' no está guardado en UTF-8. Guárdalo de nuevo con esa codificación.")
        sys.exit(1)
    except OSError as e:
        print(f"ERROR: No se pudo leer el archivo: {e}")
        sys.exit(1)
 
    tokens, errors = Lexer(code).tokenize()
 
    # Tokens y errores se imprimen mezclados, en el mismo orden en que aparecen en el código.
    salida = [(t.line, t.column, formatear_token(t)) for t in tokens]
    salida += [(e.line, e.column, formatear_error(e)) for e in errors]
    for _, _, texto in sorted(salida, key=lambda s: (s[0], s[1])):
        print(texto)
 
 
if __name__ == '__main__':
    main()
 
