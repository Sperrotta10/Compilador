import matplotlib.pyplot as plt
import networkx as nx

class ASTNode:
    def __init__(self, tipo, valor=None, hijos=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = hijos or []

    def __str__(self):
        if isinstance(self.hijos, list) and self.hijos:
            hijos_str = ", ".join(str(hijo) for hijo in self.hijos)
            return f"{self.tipo}: {self.valor}, Hijos: [{hijos_str}]"
        elif isinstance(self.hijos, ASTNode):
            return f"{self.tipo}: {self.valor}, Hijo: [{str(self.hijos)}]"
        else:
            return f"{self.tipo}: {self.valor}"

    def graficar(self, parent_id=None, node_count=0, nodes=[], edges=[], level=0):
        node_id = node_count
        nodes.append((node_id, f"{self.tipo}: {str(self.valor)}"))

        if parent_id is not None:
            edges.append((parent_id, node_id))

        node_count += 1

        if not isinstance(self.hijos, list):
            self.hijos = [self.hijos]

        for hijo in self.hijos:
            if isinstance(hijo, ASTNode):
                node_count = hijo.graficar(parent_id=node_id, node_count=node_count, nodes=nodes, edges=edges, level=level + 1)
            else:
                nodes.append((node_count, f"Valor: {hijo}"))
                edges.append((node_id, node_count))
                node_count += 1

        return node_count

    def graficar_mpl(self, output_filename="arbol_sintactico.png"):
        nodes = []
        edges = []
        self.graficar(node_count=0, nodes=nodes, edges=edges)

        G = nx.DiGraph()

        # Añadir los nodos
        for node_id, label in nodes:
            G.add_node(node_id, label=label)

        # Añadir los bordes
        for start, end in edges:
            G.add_edge(start, end)

        pos = self.crear_layout_arbol(G, nodes, edges)

        labels = nx.get_node_attributes(G, 'label')

        plt.figure(figsize=(20, 15))  # Aumentar el tamaño de la figura
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=2000, node_color='lightblue', font_size=7, font_weight='bold', arrows=True)  # Reducir el tamaño de los nodos y la fuente

        plt.title("Árbol Sintáctico Abstracto")
        plt.tight_layout()  # Ajustar los límites del gráfico

        # Guardar la imagen
        plt.savefig(output_filename, format="PNG")
        plt.show()
        print(f"Árbol guardado como imagen: {output_filename}")


    def crear_layout_arbol(self, G, nodes, edges):
        pos = {}
        levels = {}
        for node_id, label in nodes:
            level = self.obtener_nivel(node_id, edges)
            if level not in levels:
                levels[level] = []
            levels[level].append(node_id)

        max_level = max(levels.keys()) if levels else 0
        vertical_spacing = 2  # Aumentar el espaciado vertical
        horizontal_spacing = 4  # Aumentar el espaciado horizontal

        for level in range(max_level + 1):
            if level not in levels:
                continue

            level_width = len(levels[level]) * horizontal_spacing
            x_start = -level_width / 2  # Centrar los nodos en el nivel

            for i, node_id in enumerate(levels[level]):
                x = x_start + i * horizontal_spacing
                y = -level * vertical_spacing
                pos[node_id] = (x, y)

        return pos


    def obtener_nivel(self, node_id, edges):
        parent = self.obtener_padre(node_id, edges)
        if parent is None:
            return 0  # Nodo raíz
        return self.obtener_nivel(parent, edges) + 1

    def obtener_padre(self, node_id, edges):
        for start, end in edges:
            if end == node_id:
                return start
        return None  # Es el nodo raíz




class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
    
    def eat(self, expected_type):
        """Verifica si el token actual es del tipo esperado y avanza al siguiente"""
        if self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]

            # Imprimir el token actual para ver qué está siendo procesado
            print(f"Procesando token {self.current_token_index}: {token_type}, {token_value}")

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
            operador_asignacion = self.eat("Operador de Asignación")
            derecha = self.parse_expresion()  # Llamamos de nuevo a parse_expresion() para procesar la parte derecha
            return ASTNode("Asignacion", operador_asignacion, [ASTNode("Identificador", izquierda, []), derecha])
        
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
                    operador_asignacion = self.eat("Operador de Asignación")  # Operador '='
                    valor = self.parse_expresion()
                self.eat("Delimitador")  # Punto y coma ';'
                
                # Crear el nodo de la declaración de la variable con el operador de asignación
                if operador_asignacion:
                    return ASTNode("Declaracion", tipo_dato, [ASTNode("Identificador", identificador, []), operador_asignacion, valor])
                else:
                    return ASTNode("Declaracion", tipo_dato, [ASTNode("Identificador", identificador, []), None])  # Sin valor si no hay asignación
            else:
                raise SyntaxError("Error: Se esperaba un tipo de dato al inicio de la declaración.")
        else:
            raise SyntaxError("Error: No se encontraron más tokens para procesar.")

    def parse_sentencia_if(self):
        """Analiza una sentencia 'if' con su bloque de instrucciones y opcionales 'else' o 'else if'."""
        
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Se esperaba 'if', pero no hay más tokens.")
        
        token_type, token_value, _, _ = self.tokens[self.current_token_index]
        if token_type != "Condicional" or token_value != "if":
            raise SyntaxError(f"Se esperaba 'if', pero se encontró '{token_value}'.")
        
        self.eat("Condicional")  # Consumimos el 'if'

        # 1. Verificamos el paréntesis de apertura '('
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "(":
            raise SyntaxError("Se esperaba '(' después de 'if'.")
        self.eat("Delimitador")  # Consumimos '('

        # 2. Expresión condicional dentro del 'if'
        expresion = self.parse_expresion()

        # 3. Verificamos el paréntesis de cierre ')'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ")":
            raise SyntaxError("Se esperaba ')' después de la expresión condicional.")
        self.eat("Delimitador")  # Consumimos ')'

        # 4. Verificamos el delimitador de apertura de bloque '{'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "{":
            raise SyntaxError("Se esperaba '{' después de ')'.")
        self.eat("Delimitador")  # Consumimos '{'

        # 5. Instrucciones dentro del bloque 'if'
        instrucciones = self.parse_instrucciones()  # Parseamos las instrucciones dentro del bloque

        # 6. Verificamos el delimitador de cierre de bloque '}'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "}":
            raise SyntaxError("Se esperaba '}' al final del bloque 'if'.")
        self.eat("Delimitador")  # Consumimos '}'

        # 7. Opcional: Verificamos la existencia de un 'else'
        if self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]
            
            if token_type == "Condicional" and token_value == "else":
                self.eat("Condicional")  # Consumimos 'else'
                
                # Verificamos el delimitador de apertura de bloque '{'
                if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "{":
                    raise SyntaxError("Se esperaba '{' después de 'else'.")
                self.eat("Delimitador")  # Consumimos '{'
                
                instrucciones_else = self.parse_instrucciones()  # Parseamos las instrucciones del 'else'
                
                # Verificamos el delimitador de cierre de bloque '}'
                if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "}":
                    raise SyntaxError("Se esperaba '}' al final del bloque 'else'.")
                self.eat("Delimitador")  # Consumimos '}'
                
                return ASTNode("IfElse", expresion, [instrucciones, instrucciones_else])

            # Opcional: Verificamos el caso de 'else if'
            elif token_type == "Condicional" and token_value == "else if":
                return self.parse_sentencia_if()  # Recurre y analiza el 'else if' como un nuevo 'if'
        
        return ASTNode("If", None, [expresion, instrucciones])


    def parse_sentencia_while(self):
        """Regla para una sentencia while: while (condición) { instrucciones }"""
        
        # Verificar si hay más tokens antes de acceder al siguiente
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Se esperaba 'while', pero no hay más tokens.")
        
        # Verificar la palabra clave 'while'
        token_type, token_value, _, _ = self.tokens[self.current_token_index]
        if token_type != "Bucle" or token_value != "while":
            raise SyntaxError(f"Se esperaba 'while', pero se encontró '{token_value}'.")
        self.eat("Bucle")  # Consumir 'while'

        # Verificar el delimitador '('
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "(":
            raise SyntaxError("Se esperaba '(' después de 'while'.")
        self.eat("Delimitador")  # Consumir '('

        # Condición del while
        condicion = self.parse_expresion()

        # Verificar el delimitador ')'
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ")":
            raise SyntaxError("Se esperaba ')' después de la condición.")
        self.eat("Delimitador")  # Consumir ')'

        # Verificar el delimitador de apertura del bloque '{'
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "{":
            raise SyntaxError("Se esperaba '{' después de ')'.")
        self.eat("Delimitador")  # Consumir '{'

        # Instrucciones dentro del bloque while
        instrucciones = self.parse_instrucciones()

        # Verificar el delimitador de cierre del bloque '}'
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "}":
            raise SyntaxError("Se esperaba '}' al final del bloque 'while'.")
        self.eat("Delimitador")  # Consumir '}'

        # Crear el nodo para el bucle while
        return ASTNode("While", None, [condicion, instrucciones])
    

    def parse_sentencia_do_while(self):
        """Regla para una sentencia do-while: do { instrucciones } while (condición);"""
        
        # Verificar la palabra clave 'do'
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Se esperaba 'do', pero no hay más tokens.")
        
        token_type, token_value, _, _ = self.tokens[self.current_token_index]
        if token_type != "Bucle" or token_value != "do":
            raise SyntaxError(f"Se esperaba 'do', pero se encontró '{token_value}'.")
        self.eat("Bucle")  # Consumir 'do'

        # Verificar el delimitador de apertura del bloque '{'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "{":
            raise SyntaxError("Se esperaba '{' después de 'do'.")
        self.eat("Delimitador")  # Consumir '{'

        # Instrucciones dentro del bloque do
        instrucciones = self.parse_instrucciones()

        # Verificar el delimitador de cierre del bloque '}'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "}":
            raise SyntaxError("Se esperaba '}' al final del bloque 'do'.")
        self.eat("Delimitador")  # Consumir '}'

        # Verificar la palabra clave 'while'
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Se esperaba 'while', pero no hay más tokens.")
        
        token_type, token_value, _, _ = self.tokens[self.current_token_index]
        if token_type != "Bucle" or token_value != "while":
            raise SyntaxError(f"Se esperaba 'while', pero se encontró '{token_value}'.")
        self.eat("Bucle")  # Consumir 'while'

        # Verificar el delimitador '('
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "(":
            raise SyntaxError("Se esperaba '(' después de 'while'.")
        self.eat("Delimitador")  # Consumir '('

        # Condición del while
        condicion = self.parse_expresion()

        # Verificar el delimitador ')'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ")":
            raise SyntaxError("Se esperaba ')' después de la condición.")
        self.eat("Delimitador")  # Consumir ')'

        # Verificar el delimitador ';'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ";":
            raise SyntaxError("Se esperaba ';' al final de 'do-while'.")
        self.eat("Delimitador")  # Consumir ';'

        # Crear el nodo para el bucle do-while
        return ASTNode("DoWhile", None, [instrucciones, condicion])
    
    def parse_sentencia_for(self):
        """Regla para una sentencia for: for (inicialización; condición; actualización) { ... }"""
        
        # Verificar la palabra clave 'for'
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Se esperaba 'for', pero no hay más tokens.")
        
        token_type, token_value, _, _ = self.tokens[self.current_token_index]
        if token_type != "Bucle" or token_value != "for":
            raise SyntaxError(f"Se esperaba 'for', pero se encontró '{token_value}'.")
        self.eat("Bucle")  # Consumir 'for'

        # Verificar el delimitador '('
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "(":
            raise SyntaxError("Se esperaba '(' después de 'for'.")
        self.eat("Delimitador")  # Consumir '('

        # Inicialización (puede ser una declaración de variable o una expresión)
        inicializacion = self.parse_expresion()

        # Verificar el delimitador ';'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ";":
            raise SyntaxError("Se esperaba ';' después de la inicialización.")
        self.eat("Delimitador")  # Consumir ';'

        # Condición
        condicion = self.parse_expresion()

        # Verificar el delimitador ';'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ";":
            raise SyntaxError("Se esperaba ';' después de la condición.")
        self.eat("Delimitador")  # Consumir ';'

        # Actualización
        actualizacion = self.parse_expresion()

        # Verificar el delimitador ')'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ")":
            raise SyntaxError("Se esperaba ')' después de la actualización.")
        self.eat("Delimitador")  # Consumir ')'

        # Verificar el delimitador de apertura del bloque '{'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "{":
            raise SyntaxError("Se esperaba '{' después de 'for'.")
        self.eat("Delimitador")  # Consumir '{'

        # Instrucciones dentro del bloque for
        instrucciones = self.parse_instrucciones()

        # Verificar el delimitador de cierre del bloque '}'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "}":
            raise SyntaxError("Se esperaba '}' al final del bloque 'for'.")
        self.eat("Delimitador")  # Consumir '}'

        # Crear el nodo para el bucle for
        return ASTNode("For", None, [inicializacion, condicion, actualizacion, instrucciones])
    

    def parse_declaracion_funcion(self):
        """Regla para una declaración de función: tipo_retorno nombre_funcion(parámetros) { ... }"""
        
        # Verificar el tipo de retorno
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Se esperaba un tipo de retorno, pero no hay más tokens.")
        
        tipo_retorno = self.eat("Tipo de dato")  # Consumir el tipo de retorno

        # Verificar el nombre de la función
        nombre_funcion = self.eat("Identificador")  # Consumir el nombre de la función

        # Verificar el delimitador '('
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "(":
            raise SyntaxError("Se esperaba '(' después del nombre de la función.")
        self.eat("Delimitador")  # Consumir '('

        # Parámetros (pueden ser múltiples, separados por comas)
        parametros = []
        while self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]
            
            if token_type == "Tipo de dato":
                tipo_parametro = self.eat("Tipo de dato")
                nombre_parametro = self.eat("Identificador")
                parametros.append((tipo_parametro, nombre_parametro))
            
            # Verificar si hay más parámetros
            if self.tokens[self.current_token_index][0] == "Delimitador" and self.tokens[self.current_token_index][1] == ",":
                self.eat("Delimitador")  # Consumir ','
            else:
                break

        # Verificar el delimitador ')'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ")":
            raise SyntaxError("Se esperaba ')' después de los parámetros.")
        self.eat("Delimitador")  # Consumir ')'

        # Verificar el delimitador de apertura del bloque '{'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "{":
            raise SyntaxError("Se esperaba '{' después de la declaración de la función.")
        self.eat("Delimitador")  # Consumir '{'

        # Instrucciones dentro del bloque de la función
        instrucciones = self.parse_instrucciones()

        # Verificar el delimitador de cierre del bloque '}'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "}":
            raise SyntaxError("Se esperaba '}' al final del bloque de la función.")
        self.eat("Delimitador")  # Consumir '}'

        # Crear el nodo para la declaración de la función
        return ASTNode("Funcion", tipo_retorno, [nombre_funcion, parametros, instrucciones])


    def parse_instrucciones(self):
        """Analiza las instrucciones dentro del bloque."""
        instrucciones = []
        while self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]
            
            # Verifica si es el cierre de bloque
            if token_type == "Delimitador" and token_value == "}":
                break  # Detiene el bucle si encuentra un '}'
            
            # Primero se verifican las sentencias como declaraciones o condicionales
            if token_type == "Tipo de dato":
                instrucciones.append(self.parse_declaracion_variable())  # Declaración de variable
            elif token_type == "Condicional":
                instrucciones.append(self.parse_sentencia_if())  # Sentencia if
            elif token_type == "Bucle":
                instrucciones.append(self.parse_sentencia_while())  # Sentencia while
            elif token_type == "Identificador":  # Esto debería ser parte de una expresión o asignación
                if self.tokens[self.current_token_index + 1][0] == "Operador de Asignación":
                    instrucciones.append(self.parse_expresion())  # Lógica de asignación
                else:
                    instrucciones.append(self.parse_expresion())  # Lógica de expresión
            elif token_type == "Delimitador" and token_value != "}":
                self.eat("Delimitador")  # Avanza si no es el final del bloque
            else:
                raise SyntaxError(f"Token inesperado '{token_type}'")
        
        # Crear el nodo para el bloque de instrucciones
        return ASTNode("Bloque", None, instrucciones)

            
    def parse(self):
        """Inicia el análisis sintáctico"""
        try:
            ast = self.parse_instrucciones()

            print("AST Generado:", ast)

            # Comprobamos si hemos procesado todos los tokens
            if self.current_token_index < len(self.tokens):
                raise SyntaxError(f"Token inesperado '{self.tokens[self.current_token_index][1]}' al final del código.")

            
            # Graficamos el árbol después de generarlo
            ast.graficar_mpl()

            return ast  # Retornar el árbol de sintaxis abstracta

        except SyntaxError as e:
            print(f"Error de sintaxis: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")


tokens = [('Tipo de dato', 'int', 1, 1), ('Identificador', 'x', 1, 5), ('Operador de Asignación', '=', 1, 7), ('Número', '5', 1, 9), ('Delimitador', ';', 1, 10), ('Condicional', 'if', 2, 1), ('Delimitador', '(', 2, 4), ('Identificador', 'x', 2, 5), ('Operador Relacional', '>', 2, 7), ('Número', '3', 2, 9), ('Delimitador', ')', 2, 10), ('Delimitador', '{', 2, 12), ('Identificador', 'x', 3, 5), ('Operador de Asignación', '=', 3, 7), ('Identificador', 'x', 3, 9), ('Operador Aritmético', '+', 3, 11), ('Número', '1', 3, 13), ('Delimitador', ';', 3, 14), ('Delimitador', '}', 4, 1), ('Bucle', 'while', 5, 1), ('Delimitador', '(', 5, 7), ('Identificador', 'x', 5, 8), ('Operador Relacional', '<', 5, 10), ('Número', '10', 5, 12), ('Delimitador', ')', 5, 14), ('Delimitador', '{', 5, 16), ('Identificador', 'x', 6, 5), ('Operador de Asignación', '=', 6, 7), ('Identificador', 'x', 6, 9), ('Operador Aritmético', '+', 6, 11), ('Número', '2', 6, 13), ('Delimitador', ';', 6, 14), ('Delimitador', '}', 7, 1)]
parsear = Parser(tokens)
parsear.parse()