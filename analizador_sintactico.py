class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
    
    def eat(self, expected_type):
        """Verifica si el token actual es del tipo esperado y avanza al siguiente"""
        if self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]
            if token_type == expected_type:
                self.current_token_index += 1
                return token_value
            else:
                raise SyntaxError(f"Error: Se esperaba '{expected_type}' pero se encontró '{token_value}'")
        else:
            raise SyntaxError(f"Error: Se esperaba '{expected_type}' pero no hay más tokens.")
        
    def parse_expresion(self):
        #Regla: Identificador | Número | Identificador Operador Identificador
        izquierda = self.eat("Identificador") if self.tokens[self.current_token_index][0] == "Identificador" else self.eat("Número")
        if self.tokens[self.current_token_index][0] in ["Operador Aritmético", "Operador Relacional"]:
            operador = self.eat(self.tokens[self.current_token_index][0])
            derecha = self.eat("Identificador") if self.tokens[self.current_token_index][0] == "Identificador" else self.eat("Número")

    def parse_declaracion_variable(self):
        """Regla para una declaración de variable en Java: Tipo Identificador = Valor ;"""
        if self.current_token_index < len(self.tokens):
            token_type, _, _, _ = self.tokens[self.current_token_index]
            if token_type == "Tipo de dato":
                self.eat("Tipo de dato")  # Tipo de dato (int, float, etc.)
                self.eat("Identificador")  # Nombre de la variable
                if self.tokens[self.current_token_index][0] == "Operador de Asignación":
                    self.eat("Operador de Asignación")  # Operador '='
                    valor = self.parse_expresion()
                self.eat("Delimitador")  # Punto y coma ';'
                print("✔ Declaración de variable válida")
            else:
                raise SyntaxError("Error: Se esperaba un tipo de dato al inicio de la declaración.")

    def parse_sentencia_if(self):
        """Regla para una sentencia if: if (condición) { instrucciones }"""
        self.eat("Condicional")  # if
        self.eat("Delimitador")  # (
        self.eat("Identificador")  # Variable en la condición
        self.eat("Operador Relacional")  # Operador de comparación
        self.eat("Número")  # Valor
        self.eat("Delimitador")  # )
        self.eat("Delimitador")  # {
        instrucciones = self.parse_instrucciones()
        self.eat("Delimitador")  # }
        print("✔ Estructura if válida")

    def parse_sentencia_while(self):
        #Regla: while (condición) { instrucciones }
        self.eat("Bucle")  # while
        self.eat("Delimitador")  # (
        condicion = self.parse_expresion()
        self.eat("Delimitador")  # )
        self.eat("Delimitador")  # {
        instrucciones = self.parse_instrucciones()
        self.eat("Delimitador")  # }
        print("✔ Estructura while válida")

    def parse_instrucciones(self):
        """Analiza el código según las reglas definidas"""
        #Regla: Lista de instrucciones dentro de un bloque
        instrucciones = []
        while self.current_token_index < len(self.tokens):
            token_type, _, _, _ = self.tokens[self.current_token_index]
            if token_type == "Tipo de dato":
                instrucciones.append(self.parse_declaracion_variable())
                print("1", instrucciones)
            elif token_type == "Condicional":
                instrucciones.append(self.parse_sentencia_if())
                print("2", instrucciones)
            elif token_type == "Bucle":
                instrucciones.append(self.parse_sentencia_while())
                print("3", instrucciones)
            else:
                raise SyntaxError(f"Token inesperado '{token_type}'")
            
    def parse(self):
        #Inicio del análisis sintáctico
        return self.parse_instrucciones()

    """
    def parse_instrucciones(self):
        #Regla: Lista de instrucciones dentro de un bloque
        instrucciones = []
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] != "}":
            token_type = self.tokens[self.current_token_index][0]
            if token_type == "Tipo de dato":
                instrucciones.append(self.parse_declaracion_variable())
            elif token_type == "Condicional":
                instrucciones.append(self.parse_sentencia_if())
            elif token_type == "Bucle":
                instrucciones.append(self.parse_sentencia_while())
            else:
                raise SyntaxError(f"Token inesperado '{token_type}'")
            print(f"Instrucción procesada: {instrucciones[-1]}")  # Mensaje de depuración
    """

"""

class ASTNode:
    #Clase base para todos los nodos del AST
    def __init__(self, tipo, valor=None, hijos=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = hijos if hijos is not None else []

    def __repr__(self):
        return f"{self.tipo}({self.valor}) -> {self.hijos}"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def eat(self, expected_type):
        #Verifica el token actual y avanza al siguiente
        if self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]
            if token_type == expected_type:
                self.current_token_index += 1
                return token_value
            else:
                raise SyntaxError(f"Se esperaba '{expected_type}', pero se encontró '{token_value}'")
        else:
            raise SyntaxError(f"Se esperaba '{expected_type}', pero no hay más tokens.")

    def parse_declaracion_variable(self):
        #Regla: Tipo Identificador = Expresión;
        tipo = self.eat("Tipo de dato")  # Tipo de dato (int, float, etc.)
        nombre = self.eat("Identificador")  # Nombre de la variable
        valor = None
        if self.tokens[self.current_token_index][0] == "Operador de Asignación":
            self.eat("Operador de Asignación")  # Operador '='
            valor = self.parse_expresion()
        self.eat("Delimitador")  # Punto y coma ;
        print("✔ Declaración de variable válida")
        return ASTNode("Declaracion", f"{tipo} {nombre}", [valor])

    def parse_expresion(self):
        #Regla: Identificador | Número | Identificador Operador Identificador
        izquierda = self.eat("Identificador") if self.tokens[self.current_token_index][0] == "Identificador" else self.eat("Número")
        if self.tokens[self.current_token_index][0] in ["Operador Aritmético", "Operador Relacional"]:
            operador = self.eat(self.tokens[self.current_token_index][0])
            derecha = self.eat("Identificador") if self.tokens[self.current_token_index][0] == "Identificador" else self.eat("Número")
            return ASTNode("Expresion", operador, [izquierda, derecha])
        return ASTNode("Expresion", izquierda)

    def parse_sentencia_if(self):
        #Regla: if (condición) { instrucciones }
        self.eat("Condicional")  # if
        self.eat("Delimitador")  # (
        condicion = self.parse_expresion()
        self.eat("Delimitador")  # )
        self.eat("Delimitador")  # {
        instrucciones = self.parse_instrucciones()
        self.eat("Delimitador")  # }
        print("✔ Estructura if válida")
        return ASTNode("If", None, [condicion, instrucciones])

    def parse_sentencia_while(self):
        #Regla: while (condición) { instrucciones }
        self.eat("Bucle")  # while
        self.eat("Delimitador")  # (
        condicion = self.parse_expresion()
        self.eat("Delimitador")  # )
        self.eat("Delimitador")  # {
        instrucciones = self.parse_instrucciones()
        self.eat("Delimitador")  # }
        print("✔ Estructura while válida")
        return ASTNode("While", None, [condicion, instrucciones])

    def parse_instrucciones(self):
        #Regla: Lista de instrucciones dentro de un bloque
        instrucciones = []
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] != "}":
            token_type = self.tokens[self.current_token_index][0]
            if token_type == "Tipo de dato":
                instrucciones.append(self.parse_declaracion_variable())
            elif token_type == "Condicional":
                instrucciones.append(self.parse_sentencia_if())
            elif token_type == "Bucle":
                instrucciones.append(self.parse_sentencia_while())
            else:
                raise SyntaxError(f"Token inesperado '{token_type}'")
            print(f"Instrucción procesada: {instrucciones[-1]}")  # Mensaje de depuración
        return ASTNode("Bloque", None, instrucciones)

    def parse(self):
        #Inicio del análisis sintáctico
        return self.parse_instrucciones()


def print_ast(node, level=0):
    #Función para imprimir el AST de forma jerárquica
    indent = "  " * level
    print(f"{indent}- {node.tipo}: {node.valor if node.valor else ''}")
    for child in node.hijos:
        if isinstance(child, ASTNode):
            print_ast(child, level + 1)
        else:
            print(f"{indent}  - {child}")

"""