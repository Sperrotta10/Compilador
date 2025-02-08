import re

# Definimos los patrones de tokens
TOKEN_PATTERNS = [
    ("CONDITIONAL", r"\b(if|else)\b"),
    ("LOOP", r"\b(for|while)\b"),
    ("DATA_TYPE", r"\b(int|float|double|boolean|char|string)\b"),
    ("NUMBER", r"\b\d+(\.\d+)?\b"),
    ("COMMENT", r"(//.*|/\*[\s\S]*?\*/)"),
    ("ERROR", r"[^a-zA-Z0-9_\s\+\-\*/=<>!{}()\[\];,.]"),
    ("ARITHMETIC_OPERATOR", r"[+\-*/%]"),
    ("ASSIGNMENT_OPERATOR", r"="), 
    ("LOGICAL_OPERATOR", r"(&&|\|\||!)"),
    ("RELATIONAL_OPERATOR", r"(==|!=|<|>|<=|>=)"),
    ("DATA_STRUCTURE", r"\b(array|list|set)\b"),
    ("DELIMITER", r"[;{}(),]"),
    ("EXCEPTION", r"\b(try|catch|throw)\b"),
    ("ACCESS_TOKEN", r"\b(public|private|protected)\b"),
    ("COMPOUND_OPERATOR", r"(\+=|-=|\*=|/=)"),
    ("NEWLINE", r"\n"),
    ("WHITESPACE", r"[ \t]+"),
    ("KEYWORD", r"\b(if|else|while|for|return|class|public|private|static|void)\b"),
    ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
]

def lexer(code):
    tokens = []
    position = 0

    while position < len(code):
        match = None
        for token_type, pattern in TOKEN_PATTERNS:
            regex = re.compile(pattern)
            match = regex.match(code, position)

            if match:
                value = match.group(0)
                if token_type != "WHITESPACE" and token_type != "COMMENT":  # Ignorar espacios
                    tokens.append((token_type, value))
                position = match.end()
                break

        if not match:
            raise SyntaxError(f"Unexpected character {position}: {code[position]}")
    
    return tokens

# Ejemplo de código fuente simple
code = """
class PruebaJava { 

    public static void main() { 
        
        int x = 10;
        for(int i = 0; i < 10; i++) {
            // Esto es un comentario
            x += i;
        }
    } 
}

"""
print(lexer(code))
