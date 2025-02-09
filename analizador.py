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
    
    return tokens

# Ejemplo de código fuente simple
code = """
public class EjemploPatterns {
    public static void main(String[] args) {
        // Variables
        String nombre = "Juan";
        int edad = 30;
        double salario = 2500.75;

        // Imprimir mensaje con printf
        System.out.printf("Nombre: %s | Edad: %d | Salario: %.2f%n", nombre, edad, salario);

        // Condicional
        if (edad > 18) {
            System.out.println("Mayor de edad");
        } else {
            System.out.println("Menor de edad");
        }

        // Bucle for
        for (int i = 0; i < 3; i++) {
            System.out.println("Contador: " + i);
        }

        // Comentarios
        // Este es un comentario de una sola línea
        /* Este es un comentario
           de múltiples líneas */
    }
}



"""
print(lexer(code))
