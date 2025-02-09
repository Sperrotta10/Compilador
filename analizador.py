import re

# Definimos los patrones de tokens
TOKEN_PATTERNS = [
    ("COMMENT", r"//.*|/\*[\s\S]*?\*/"),
    ("KEYWORD", r"\b(class|public|private|protected|static|void|if|else|while|for|return|try|catch|throw)\b"),
    ("DATA_TYPE", r"\b(int|float|double|boolean|char|string)\b"),
    ("CONDITIONAL", r"\b(if|else)\b"),
    ("LOOP", r"\b(for|while)\b"),
    ("EXCEPTION", r"\b(try|catch|throw)\b"),
    ("ACCESS_TOKEN", r"\b(public|private|protected)\b"),
    ("DATA_STRUCTURE", r"\b(array|list|set)\b"),
    ("PRINT_STATEMENT", r"\b(System.out.print|System.out.println|System.out.printf)\b"),
    ("STRING_LITERAL", r'"([^"\\]*(\\.[^"\\]*)*)"'),
    ("NUMBER", r"\b\d+(\.\d+)?\b"),
    ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("ARITHMETIC_OPERATOR", r"[+\-*/%]"),
    ("ASSIGNMENT_OPERATOR", r"="),
    ("COMPOUND_OPERATOR", r"(\+=|-=|\*=|/=)"),
    ("LOGICAL_OPERATOR", r"(&&|\|\||!)"),
    ("RELATIONAL_OPERATOR", r"(==|!=|<|>|<=|>=)"),
    ("DELIMITER", r"[;{}(),]"),
    ("NEWLINE", r"\n"),
    ("WHITESPACE", r"[ \t]+"),
    ("ERROR", r".")  # Captura cualquier carácter inesperado
]

TOKEN_REGEX = [(name, re.compile(pattern)) for name, pattern in TOKEN_PATTERNS] #Se compilan las expresiones regulares una sola vez antes del bucle


def lexer(ruta_archivo):
    with open(ruta_archivo, 'r') as file:
        code = file.read()  # Leemos el contenido del archivo

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
    
    return tokens

# Llamamos a la función pasando la ruta del archivo Java
ruta_archivo = 'Pruebas/Prueba_1.java'  

print(lexer(ruta_archivo))
