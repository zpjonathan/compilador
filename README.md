Proyecto Final de Compiladores — Fase 1: Análisis Léxico
Integrantes
Ovidio Jonathan Zacapa Patriz
Keyli Marce
Descripción

Analizador léxico (scanner) escrito en Python que lee un archivo de código fuente, reconoce los tokens del lenguaje y reporta los errores léxicos con su línea y columna exactas. Usa únicamente el módulo estándar re (sin PLY, ANTLR ni Flex).

Estructura
main.py            # Punto de entrada (lee el archivo por sys.argv e imprime la salida)
lexer.py           # Lógica del analizador léxico (clase Lexer, Token, LexicalError)
tests/
  caso_valido.txt  # Código correcto, sin errores léxicos
  caso_error.txt   # Código con errores léxicos intencionales
README.md
Ejecución

Requiere Python 3.8 o superior. Desde la carpeta del proyecto, usar estos comandos para ejecutar y ver los casos de prueba:

bash
python main.py tests/caso_valido.txt
python main.py tests/caso_error.txt
Componentes reconocidos
Categoría	Tipos de token	Ejemplos
Palabras reservadas	PR_INT, PR_FLOAT, PR_VOID, PR_IF, PR_ELSE, PR_WHILE, PR_RETURN, PR_TRUE, PR_FALSE	int, if, while
Identificadores	ID	limite, _x1
Literales	INT_LITERAL, FLOAT_LITERAL, STRING_LITERAL	100, 3.14, "hola"
Operadores relacionales	OP_REL	==  !=  <  >  <=  >=
Operador de asignación	OP_ASSIGN	=
Operadores aritméticos	OP_ARITH	+  -  *  /
Delimitadores	DELIM_LPAREN, DELIM_RPAREN, DELIM_LBRACE, DELIM_RBRACE, DELIM_COMMA, DELIM_SEMICOLON	( ) { } , ;

Se ignoran espacios, tabulaciones, saltos de línea y comentarios (// ... y /* ... */), pero se procesan internamente para mantener correcto el conteo de líneas y columnas.

Errores léxicos detectados
Carácter no reconocido ($, @, #, ! suelto, . suelto, etc.).
Cadena sin cerrar ("hola): la comilla sin cerrar llega hasta el final de la línea.
Comentario multilínea sin cerrar (/* ...).

El programa no se detiene ante un error: lo imprime y continúa con el resto del archivo. Los tokens y los errores se muestran mezclados, en el mismo orden en que aparecen en el código.

Decisiones de diseño
Orden de los patrones: Python usa el primer patrón que coincide, por eso los comentarios van antes que los operadores, FLOAT antes que INT, y las palabras reservadas antes que ID.
Palabras reservadas: se definen en KEYWORD_MAP y el patrón KEYWORD se genera a partir de él, así hay un solo lugar donde agregar nuevas.
Posiciones: se calculan con el índice de inicio de la línea actual; los comentarios multilínea actualizan ese índice según los saltos de línea que contienen.
Ejemplo de salida

Fragmento real de python main.py tests/caso_error.txt:

[TOKEN] Tipo: ID           | Lexema: 'x'        | Posición: [Línea 5, Col 5]
[ERROR LÉXICO] Carácter no reconocido '$' en Posición: [Línea 5, Col 7]
[TOKEN] Tipo: ID           | Lexema: 'y'        | Posición: [Línea 5, Col 9]
[ERROR LÉXICO] Cadena sin cerrar '"hola;   // ERROR 2: string sin cerrar' en Posición: [Línea 6, Col 16]
[ERROR LÉXICO] Carácter no reconocido '@' en Posición: [Línea 7, Col 13]