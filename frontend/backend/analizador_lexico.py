import re

# Definimos los patrones de tokens
TOKEN_PATTERNS = [
    ("Comentario", r"//.*|/\*[\s\S]*?\*/"),
    ("Tipo de dato", r"\b(int|float|double|boolean|char|string|String|long|short|byte)\b"),
    ("Condicional", r"\b(if|else)\b"),
    ("Bucle", r"\b(for|while|do)\b"),
    ("Excepción", r"\b(try|catch|throw|finally)\b"),
    ("Token de Acceso", r"\b(public|private|protected|static|final|abstract)\b"),
    ("Estructura de Datos", r"\b(array|list|set|map|queue|stack)\b"),
    ("Imprimir", r"\b(System.out.print|System.out.println|System.out.printf)\b"),
    ("String Literal", r'"([^"\\]*(\\.[^"\\]*)*)"'),
    ("Número", r"\b\d+(\.\d+)?(e[+-]?\d+)?\b"),  # Incluye notación científica
    ("Palabra Reservada", r"\b(class|void|return|new|this|super|instanceof|switch|case|default|break|continue)\b"),
    ("Identificador", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("Operador Aritmético", r"[+\-*/%]"),
    ("Operador de Asignación", r"="),
    ("Operador Compuesto", r"(\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=|>>>=)"),
    ("Operador Lógico", r"(&&|\|\||!)"),
    ("Operador Relacional", r"(==|!=|<|>|<=|>=)"),
    ("Operador de Incremento/Decremento", r"(\+\+|--)"),
    ("Operador de Bits", r"(&|\||\^|~|<<|>>|>>>)"),
    ("Delimitador", r"[;{}(),:]"),
    ("Corchete Abierto", r"\["),
    ("Corchete Cerrado", r"\]"),
    ("Salto de Linea", r"\n"),
    ("WHITESPACE", r"[ \t]+"),
    ("Literal Booleano", r"\b(true|false)\b"),
    ("Literal Nulo", r"\b(null)\b"),
    ("ERROR", r".")  # Captura cualquier carácter inesperado
]

TOKEN_REGEX = [(name, re.compile(pattern)) for name, pattern in TOKEN_PATTERNS] #Se compilan las expresiones regulares una sola vez antes del bucle

#Función para análisis del código
def lexer(code):
    tokens = []
    position = 0
    line = 1  # Iniciar en la línea 1
    column = 1  # Iniciar en la columna 1

    while position < len(code):
        match = None
        for token_type, regex in TOKEN_REGEX:
            match = regex.match(code, position)
            
            if match:

                value = match.group(0)
                token_length = len(value)  # Longitud del token encontrado

                if token_type != "WHITESPACE" and token_type != "Salto de Linea" and token_type != "Comentario":  # Ignorar espacios
                    tokens.append((token_type, value, line, column))

                # Actualizar la posición, línea y columna
                position = match.end()
                # Contar saltos de línea en el token
                newlines = value.count("\n")
                if newlines > 0:
                    line += newlines
                    column = len(value.split("\n")[-1]) + 1  # Columna después del salto
                else:
                    column += token_length
                break

        if not match:
            # Carácter inválido encontrado
            invalid_char = code[position]
            raise SyntaxError(
                f"Invalid character '{invalid_char}' at line {line}, column {column}. "
                f"Expected a valid Java token."
            )
        
    print(tokens)
    return tokens


