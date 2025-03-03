class ASTNode:
    def __init__(self, tipo, valor=None, hijos=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = hijos or []

    def __str__(self):
        # Representación legible del nodo
        if self.hijos:
            hijos_str = ", ".join(str(hijo) for hijo in self.hijos)
            return f"{self.tipo}: {self.valor}, Hijos: [{hijos_str}]"
        else:
            return f"{self.tipo}: {self.valor}"

    def __repr__(self):
        return self.__str__()


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
        """Regla: Identificador | Número | Identificador Operador Identificador"""
        token_type, token_value, _, _ = self.tokens[self.current_token_index]

        if token_type == "Identificador":
            izquierda = self.eat("Identificador")
        elif token_type == "Número":
            izquierda = self.eat("Número")
        else:
            raise SyntaxError(f"Error en expresión: token inesperado '{token_type}'")
        
        # Manejo de asignación
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == "Operador de Asignación":
            self.eat("Operador de Asignación")
            derecha = self.parse_expresion()  # Llamamos de nuevo a parse_expresion() para procesar la parte derecha
            return ASTNode("Asignacion", None, [ASTNode("Identificador", izquierda, []), derecha])
        
        # Manejo de Operadores aritméticos o relacionales
        if self.tokens[self.current_token_index][0] in ["Operador Aritmético", "Operador Relacional"]:
            operador = self.eat(self.tokens[self.current_token_index][0])
            derecha = self.eat("Identificador") if self.tokens[self.current_token_index][0] == "Identificador" else self.eat("Número")
            return ASTNode("Expresion", operador, [ASTNode("Operando", izquierda, []), ASTNode("Operando", derecha, [])])
        
        return ASTNode("Expresion", izquierda, [])


    def parse_declaracion_variable(self):
        """Regla para una declaración de variable en Java: Tipo Identificador = Valor ;"""
        if self.current_token_index < len(self.tokens):
            token_type, _, _, _ = self.tokens[self.current_token_index]
            if token_type == "Tipo de dato":
                tipo_dato = self.eat("Tipo de dato")  # Tipo de dato (int, float, etc.)
                identificador = self.eat("Identificador")  # Nombre de la variable
                if self.tokens[self.current_token_index][0] == "Operador de Asignación":
                    self.eat("Operador de Asignación")  # Operador '='
                    valor = self.parse_expresion()
                self.eat("Delimitador")  # Punto y coma ';'
                
                # Crear el nodo de la declaración de la variable
                return ASTNode("Declaracion", tipo_dato, [ASTNode("Identificador", identificador, []), valor])
            else:
                raise SyntaxError("Error: Se esperaba un tipo de dato al inicio de la declaración.")
        else:
            raise SyntaxError("Error: No se encontraron más tokens para procesar.")

    def parse_sentencia_if(self):
        """Regla para una sentencia if: if (condición) { instrucciones }"""
        self.eat("Condicional")  # if
        self.eat("Delimitador")  # (
        condicion = self.parse_expresion()  # Condición de la sentencia if
        self.eat("Delimitador")  # )
        self.eat("Delimitador")  # {
        instrucciones = self.parse_instrucciones()  # Instrucciones dentro del bloque if
        self.eat("Delimitador")  # }
        
        # Crear el nodo de la sentencia if
        return ASTNode("Sentencia If", None, [condicion, instrucciones])

    def parse_sentencia_while(self):
        """Regla para una sentencia while: while (condición) { instrucciones }"""
        self.eat("Bucle")  # while
        self.eat("Delimitador")  # (
        condicion = self.parse_expresion()  # Condición del while
        self.eat("Delimitador")  # )
        self.eat("Delimitador")  # {
        instrucciones = self.parse_instrucciones()  # Instrucciones dentro del bloque while
        self.eat("Delimitador")  # }
        
        # Crear el nodo del bucle while
        return ASTNode("Sentencia While", None, [condicion, instrucciones])

    def parse_instrucciones(self):
        """Analiza el código según las reglas definidas"""
        instrucciones = []
        while self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]
            print(token_type)
            
            # Primero se verifican las sentencias como declaraciones o condicionales
            if token_type == "Tipo de dato":
                instrucciones.append(self.parse_declaracion_variable())  # Declaración de variable
            elif token_type == "Condicional":
                instrucciones.append(self.parse_sentencia_if())  # Sentencia if
            elif token_type == "Bucle":
                instrucciones.append(self.parse_sentencia_while())  # Sentencia while
            elif token_type == "Identificador":  # Esto debería ser parte de una expresión o asignación
                # Asegurarse de no confundir asignación con expresión
                if self.tokens[self.current_token_index + 1][0] == "Operador de Asignación":
                    # Si el siguiente token es un operador de asignación, procesamos la asignación
                    instrucciones.append(self.parse_expresion())  # Aquí puede ir la lógica de asignación
                else:
                    # Si no es asignación, se trata como una expresión
                    instrucciones.append(self.parse_expresion())  
            elif token_type == "Delimitador":
                # Si encontramos un delimitador, simplemente avanzamos al siguiente token
                # Para manejar el caso cuando llegamos al final de una instrucción
                self.eat("Delimitador")
            else:
                raise SyntaxError(f"Token inesperado '{token_type}'")
        
        # Crear el nodo para el bloque de instrucciones
        return ASTNode("Bloque", None, instrucciones)



            
    def parse(self):
        """Inicia el análisis sintáctico"""
        ast = self.parse_instrucciones()

        print("AST Generado:", ast)
        
        # Comprobamos si hemos procesado todos los tokens
        if self.current_token_index < len(self.tokens):
            raise SyntaxError(f"Token inesperado '{self.tokens[self.current_token_index][1]}' al final del código.")
        
        return ast  # Retornar el árbol de sintaxis abstracta


tokens = [('Tipo de dato', 'int', 1, 1), ('Identificador', 'x', 1, 5), ('Operador de Asignación', '=', 1, 7), ('Número', '5', 1, 9), ('Delimitador', ';', 1, 10), ('Condicional', 'if', 2, 1), ('Delimitador', '(', 2, 4), ('Identificador', 'x', 2, 5), ('Operador Relacional', '>', 2, 7), ('Número', '3', 2, 9), ('Delimitador', ')', 2, 10), ('Delimitador', '{', 2, 12), ('Identificador', 'x', 3, 5), ('Operador de Asignación', '=', 3, 7), ('Identificador', 'x', 3, 9), ('Operador Aritmético', '+', 3, 11), ('Número', '1', 3, 13), ('Delimitador', ';', 3, 14), ('Delimitador', '}', 4, 1), ('Bucle', 'while', 5, 1), ('Delimitador', '(', 5, 7), ('Identificador', 'x', 5, 8), ('Operador Relacional', '<', 5, 10), ('Número', '10', 5, 12), ('Delimitador', ')', 5, 14), ('Delimitador', '{', 5, 16), ('Identificador', 'x', 6, 5), ('Operador de Asignación', '=', 6, 7), ('Identificador', 'x', 6, 9), ('Operador Aritmético', '+', 6, 11), ('Número', '2', 6, 13), ('Delimitador', ';', 6, 14), ('Delimitador', '}', 7, 1)]
parsear = Parser(tokens)
resultado = parsear.parse()
print(resultado)

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