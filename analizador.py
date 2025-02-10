import re

# Definimos los patrones de tokens
TOKEN_PATTERNS = [
    ("Comentario", r"//.*|/\*[\s\S]*?\*/"),
    ("Tipo de dato", r"\b(int|float|double|boolean|char|string|String)\b"),
    ("Condicional", r"\b(if|else)\b"),
    ("Bucle", r"\b(for|while)\b"),
    ("Excepción", r"\b(try|catch|throw)\b"),
    ("Token de Acceso", r"\b(public|private|protected)\b"),
    ("Estructura de Datos", r"\b(array|list|set)\b"),
    ("Imprimir", r"\b(System.out.print|System.out.println|System.out.printf)\b"),
    ("String Literal", r'"([^"\\]*(\\.[^"\\]*)*)"'),
    ("Número", r"\b\d+(\.\d+)?\b"),
    ("Palabra Reservada", r"\b(class|public|private|protected|static|void|if|else|while|for|return|try|catch|throw)\b"),
    ("Identificador", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("Operador Artimético", r"[+\-*/%]"),
    ("Operador de Asignación", r"="),
    ("Operador Compuesto", r"(\+=|-=|\*=|/=)"),
    ("Operador Lógico", r"(&&|\|\||!)"),
    ("Operador Relacional", r"(==|!=|<|>|<=|>=)"),
    ("Delimitador", r"[;{}(),]"),
    ("Corchete Abierto", r"\["),
    ("Corchete Cerrado", r"\]"),
    ("Salto de Linea", r"\n"),
    ("WHITESPACE", r"[ \t]+"),
    ("ERROR", r".")  # Captura cualquier carácter inesperado
]

TOKEN_REGEX = [(name, re.compile(pattern)) for name, pattern in TOKEN_PATTERNS] #Se compilan las expresiones regulares una sola vez antes del bucle

#Función para análisis del código
def lexer(code):
    tokens = []
    position = 0

    while position < len(code):
        match = None
        for token_type, regex in TOKEN_REGEX:
            match = regex.match(code, position)

            if match:
                value = match.group(0)
                if token_type != "WHITESPACE":  # Ignorar espacios
                    tokens.append((token_type, value))
                position = match.end()
                break

        if not match:
            raise SyntaxError(f"Unexpected character {position}: {code[position]}")
    print(tokens)
    return tokens


