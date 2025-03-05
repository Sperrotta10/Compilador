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
        #plt.show()
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


    def parse_declaracion_variable(self, modificadores=None):
        """Regla para una declaración de variable en Java: [modificadores] Tipo Identificador = Valor ;"""

        if modificadores is None:
            modificadores = []  # Si no se proporcionan modificadores, usar una lista vacía

        if self.current_token_index < len(self.tokens):

            token_type, token_value, _, _ = self.tokens[self.current_token_index]

             # Si el token es un modificador, consumirlo y continuar
            while token_type == "Token de Acceso" or token_type == "Palabra Reservada":
                if token_value in ["public", "private", "protected", "static", "final"]:
                    modificadores.append(token_value)
                    self.eat(token_type)  # Consumir el modificador
                else:
                    break  # Salir del bucle si no es un modificador válido
                
                # Actualizar el token actual
                if self.current_token_index < len(self.tokens):
                    token_type, token_value, _, _ = self.tokens[self.current_token_index]
                else:
                    break

            if token_type == "Tipo de dato" or token_value == "void":

                if token_value != "void":
                    tipo_dato = self.eat("Tipo de dato")  # Tipo de dato (int, float, etc.)
                    identificador = self.eat("Identificador")  # Nombre de la variable
                else:
                    tipo_dato = self.eat("Palabra Reservada")  # variable de retorno (void.)
                    identificador = self.eat("Identificador")  # Nombre de la variable

                # Verificar si hay una asignación
                valor = None
                operador_asignacion = None  # Inicializar la variable

                if self.tokens[self.current_token_index][0] == "Operador de Asignación":
                    operador_asignacion = self.eat("Operador de Asignación")  # Operador '='
                    valor = self.parse_expresion()

                self.eat("Delimitador")  # Punto y coma ';'
                
                # Crear el nodo de la declaración de la variable con el operador de asignación y los modificadores
                if operador_asignacion:
                    return ASTNode("Declaracion", tipo_dato, [modificadores, ASTNode("Identificador", identificador, []), operador_asignacion, valor])
                else:
                    return ASTNode("Declaracion", tipo_dato, [modificadores, ASTNode("Identificador", identificador, []), None])  # Sin valor si no hay asignación
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
    

    def parse_declaracion_funcion(self, modificadores=None):
        """Regla para una declaración de función: [modificadores] tipo_retorno nombre_funcion(parámetros) { ... }"""
        if modificadores is None:
            modificadores = []  # Si no se proporcionan modificadores, usar una lista vacía
        
        # Validar combinaciones inválidas de modificadores
        if "abstract" in modificadores and "final" in modificadores:
            raise SyntaxError("Error: Un método no puede ser 'abstract' y 'final' al mismo tiempo.")
        if "abstract" in modificadores and "static" in modificadores:
            raise SyntaxError("Error: Un método no puede ser 'abstract' y 'static' al mismo tiempo.")
        
        # Verificar el tipo de retorno
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Se esperaba un tipo de retorno, pero no hay más tokens.")
        
        tipo_retorno = self.eat("Tipo de dato")  # Consumir el tipo de retorno

        # Verificar el nombre de la función
        nombre_funcion = self.eat("Identificador")  # Consumir el nombre de la función

        print('Hola 0')
        # Verificar el delimitador '('
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "(":
            raise SyntaxError("Se esperaba '(' después del nombre de la función.")
        self.eat("Delimitador")  # Consumir '('

        print('Hola 0.5')
        # Parámetros (pueden ser múltiples, separados por comas)
        parametros = []
        while self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]
            
            # Si encontramos ')', significa que no hay más parámetros
            if token_type == "Delimitador" and token_value == ")":
                break  # Salir del bucle si encontramos ')'
            
            if token_type == "Tipo de dato":
                tipo_parametro = self.eat("Tipo de dato")
                nombre_parametro = self.eat("Identificador")
                parametros.append((tipo_parametro, nombre_parametro))
            
                # Verificar si hay más parámetros
                if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == "Delimitador" and self.tokens[self.current_token_index][1] == ",":
                    self.eat("Delimitador")  # Consumir ','
            else:
                raise SyntaxError(f"Error: Token inesperado '{token_value}' en la lista de parámetros.")

        print("Hola 1")
        # Verificar el delimitador ')'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ")":
            raise SyntaxError("Se esperaba ')' después de los parámetros.")
        self.eat("Delimitador")  # Consumir ')'

        print("Hola 2")
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
        return ASTNode("Funcion", tipo_retorno, [modificadores, nombre_funcion, parametros, instrucciones])
    

    def parse_sentencia_try_catch(self):
        """Regla para una sentencia try-catch: try { ... } catch (TipoExcepcion e) { ... }"""
        
        # Verificar la palabra clave 'try'
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Se esperaba 'try', pero no hay más tokens.")
        
        token_type, token_value, _, _ = self.tokens[self.current_token_index]
        if token_type != "Excepción" or token_value != "try":
            raise SyntaxError(f"Se esperaba 'try', pero se encontró '{token_value}'.")
        self.eat("Excepción")  # Consumir 'try'

        # Verificar el delimitador de apertura del bloque '{'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "{":
            raise SyntaxError("Se esperaba '{' después de 'try'.")
        self.eat("Delimitador")  # Consumir '{'

        # Instrucciones dentro del bloque try
        instrucciones_try = self.parse_instrucciones()

        # Verificar el delimitador de cierre del bloque '}'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "}":
            raise SyntaxError("Se esperaba '}' al final del bloque 'try'.")
        self.eat("Delimitador")  # Consumir '}'

        # Verificar la palabra clave 'catch'
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Se esperaba 'catch', pero no hay más tokens.")
        
        token_type, token_value, _, _ = self.tokens[self.current_token_index]
        if token_type != "Excepción" or token_value != "catch":
            raise SyntaxError(f"Se esperaba 'catch', pero se encontró '{token_value}'.")
        self.eat("Excepción")  # Consumir 'catch'

        # Verificar el delimitador '('
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "(":
            raise SyntaxError("Se esperaba '(' después de 'catch'.")
        self.eat("Delimitador")  # Consumir '('

        # Tipo de excepción
        tipo_excepcion = self.eat("Tipo de dato")  # Consumir el tipo de excepción

        # Nombre de la variable de excepción
        nombre_excepcion = self.eat("Identificador")  # Consumir el nombre de la excepción

        # Verificar el delimitador ')'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ")":
            raise SyntaxError("Se esperaba ')' después de la declaración de la excepción.")
        self.eat("Delimitador")  # Consumir ')'

        # Verificar el delimitador de apertura del bloque '{'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "{":
            raise SyntaxError("Se esperaba '{' después de 'catch'.")
        self.eat("Delimitador")  # Consumir '{'

        # Instrucciones dentro del bloque catch
        instrucciones_catch = self.parse_instrucciones()

        # Verificar el delimitador de cierre del bloque '}'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "}":
            raise SyntaxError("Se esperaba '}' al final del bloque 'catch'.")
        self.eat("Delimitador")  # Consumir '}'

        # Crear el nodo para la sentencia try-catch
        return ASTNode("TryCatch", None, [instrucciones_try, (tipo_excepcion, nombre_excepcion), instrucciones_catch])
    

    def parse_sentencia_switch(self):
        """Regla para una sentencia switch: switch (expresión) { case valor: ... break; default: ... }"""
        
        # Verificar la palabra clave 'switch'
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Se esperaba 'switch', pero no hay más tokens.")
        
        token_type, token_value, _, _ = self.tokens[self.current_token_index]
        if token_type != "Palabra Reservada" or token_value != "switch":
            raise SyntaxError(f"Se esperaba 'switch', pero se encontró '{token_value}'.")
        self.eat("Palabra Reservada")  # Consumir 'switch'

        # Verificar el delimitador '('
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "(":
            raise SyntaxError("Se esperaba '(' después de 'switch'.")
        self.eat("Delimitador")  # Consumir '('

        # Expresión del switch
        expresion = self.parse_expresion()

        # Verificar el delimitador ')'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ")":
            raise SyntaxError("Se esperaba ')' después de la expresión.")
        self.eat("Delimitador")  # Consumir ')'

        # Verificar el delimitador de apertura del bloque '{'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "{":
            raise SyntaxError("Se esperaba '{' después de 'switch'.")
        self.eat("Delimitador")  # Consumir '{'

        # Casos del switch
        casos = []
        default_case = None

        while self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]
            
            # Verificar si es un caso
            if token_type == "Palabra Reservada" and token_value == "case":
                self.eat("Palabra Reservada")  # Consumir 'case'
                
                # Valor del caso
                valor = self.parse_expresion()

                # Verificar el delimitador ':'
                if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ":":
                    raise SyntaxError("Se esperaba ':' después del valor del caso.")
                self.eat("Delimitador")  # Consumir ':'

                # Instrucciones del caso
                instrucciones = self.parse_instrucciones()

                # Verificar la palabra clave 'break'
                if self.tokens[self.current_token_index][0] == "Palabra Reservada" and self.tokens[self.current_token_index][1] == "break":
                    self.eat("Palabra Reservada")  # Consumir 'break'
                    self.eat("Delimitador")  # Consumir ';'

                # Agregar el caso a la lista
                casos.append((valor, instrucciones))
            
            # Verificar si es el caso por defecto
            elif token_type == "Palabra Reservada" and token_value == "default":
                self.eat("Palabra Reservada")  # Consumir 'default'

                # Verificar el delimitador ':'
                if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != ":":
                    raise SyntaxError("Se esperaba ':' después de 'default'.")
                self.eat("Delimitador")  # Consumir ':'

                # Instrucciones del caso por defecto
                default_case = self.parse_instrucciones()
            
            # Verificar el delimitador de cierre del bloque '}'
            elif token_type == "Delimitador" and token_value == "}":
                break  # Salir del bucle
            
            else:
                raise SyntaxError(f"Token inesperado '{token_value}' en el switch.")

        # Verificar el delimitador de cierre del bloque '}'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "}":
            raise SyntaxError("Se esperaba '}' al final del bloque 'switch'.")
        self.eat("Delimitador")  # Consumir '}'

        # Crear el nodo para la sentencia switch
        return ASTNode("Switch", None, [expresion, casos, default_case])
    

    def parse_declaracion_clase(self, modificadores=None):
        """Regla para una declaración de clase: [modificadores] class NombreClase { ... }"""
        if modificadores is None:
            modificadores = []  # Si no se proporcionan modificadores, usar una lista vacía
        
        # Verificar la palabra clave 'class'
        if self.current_token_index >= len(self.tokens):
            raise SyntaxError("Se esperaba 'class', pero no hay más tokens.")
        
        token_type, token_value, _, _ = self.tokens[self.current_token_index]
        if token_type != "Palabra Reservada" or token_value != "class":
            raise SyntaxError(f"Se esperaba 'class', pero se encontró '{token_value}'.")
        self.eat("Palabra Reservada")  # Consumir 'class'

        # Nombre de la clase
        nombre_clase = self.eat("Identificador")  # Consumir el nombre de la clase

        # Verificar el delimitador de apertura del bloque '{'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "{":
            raise SyntaxError("Se esperaba '{' después del nombre de la clase.")
        self.eat("Delimitador")  # Consumir '{'

        # Atributos y métodos de la clase
        miembros = []
        while self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]
            
            # Verificar si es el cierre de bloque '}'
            if token_type == "Delimitador" and token_value == "}":
                break  # Salir del bucle si encontramos '}'
            
            # Verificar si es un atributo (declaración de variable)
            if token_type == "Tipo de dato" or token_type == "Token de Acceso":
                miembros.append(self.parse_declaracion_variable())  # Atributo
            
            # Verificar si es un método (declaración de función)
            elif token_type == "Tipo de dato" or token_type == "Token de Acceso" or (token_type == "Palabra Reservada" and token_value == "void"):
                miembros.append(self.parse_declaracion_funcion())  # Método
            
            # Verificar si es un delimitador ';' (instrucción vacía)
            elif token_type == "Delimitador" and token_value == ";":
                self.eat("Delimitador")  # Consumir ';'
            
            # Token inesperado
            else:
                raise SyntaxError(f"Token inesperado '{token_value}' en la clase. Se esperaba un atributo, método o '}}'.")

        # Verificar el delimitador de cierre del bloque '}'
        if self.tokens[self.current_token_index][0] != "Delimitador" or self.tokens[self.current_token_index][1] != "}":
            raise SyntaxError("Se esperaba '}' al final de la clase.")
        self.eat("Delimitador")  # Consumir '}'

        # Crear el nodo para la declaración de la clase
        return ASTNode("Clase", None, [modificadores, nombre_clase, miembros])


    def parse_modificadores(self):
        """Recolecta los modificadores de acceso y otros modificadores."""
        modificadores = []
        while self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]
            
            # Verificar si es un modificador válido
            if token_type == "Token de Acceso" or token_type == "Palabra Reservada":
                if token_value in ["public", "private", "protected", "static", "final", "abstract"]:
                    modificadores.append(token_value)
                    self.eat(token_type)  # Consumir el modificador
                else:
                    break  # Salir del bucle si no es un modificador válido
            else:
                break  # Salir del bucle si no es un modificador
        
        return modificadores


    def parse_instrucciones(self):
        """Analiza las instrucciones dentro de un bloque."""
        instrucciones = []
        while self.current_token_index < len(self.tokens):
            token_type, token_value, _, _ = self.tokens[self.current_token_index]
            
            # Verifica si es el cierre de bloque
            if token_type == "Delimitador" and token_value == "}":
                break  # Detiene el bucle si encuentra un '}'
            
            # Recolectar modificadores (public, private, protected, static, etc.)
            modificadores = self.parse_modificadores()
            
            # Verificar el tipo de declaración basado en el siguiente token
            if self.current_token_index < len(self.tokens):
                token_type, token_value, _, _ = self.tokens[self.current_token_index]
                
                # 1. Declaración de variable
                if token_type == "Tipo de dato":
                    instrucciones.append(self.parse_declaracion_variable(modificadores))  # Declaración de variable
                
                # 2. Declaración de función
                elif token_type == "Tipo de dato" or (token_type == "Palabra Reservada" and token_value == "void"):
                    instrucciones.append(self.parse_declaracion_funcion(modificadores))  # Declaración de función
                
                # 3. Declaración de clase
                elif token_type == "Palabra Reservada" and token_value == "class":
                    instrucciones.append(self.parse_declaracion_clase(modificadores))  # Declaración de clase
                
                # 4. Sentencia if
                elif token_type == "Condicional" and token_value == "if":
                    instrucciones.append(self.parse_sentencia_if())  # Sentencia if
                
                # 5. Sentencia while
                elif token_type == "Bucle" and token_value == "while":
                    instrucciones.append(self.parse_sentencia_while())  # Sentencia while
                
                # 6. Sentencia do-while
                elif token_type == "Bucle" and token_value == "do":
                    instrucciones.append(self.parse_sentencia_do_while())  # Sentencia do-while
                
                # 7. Sentencia for
                elif token_type == "Bucle" and token_value == "for":
                    instrucciones.append(self.parse_sentencia_for())  # Sentencia for
                
                # 8. Sentencia try-catch
                elif token_type == "Excepción" and token_value == "try":
                    instrucciones.append(self.parse_sentencia_try_catch())  # Sentencia try-catch
                
                # 9. Sentencia switch
                elif token_type == "Palabra Reservada" and token_value == "switch":
                    instrucciones.append(self.parse_sentencia_switch())  # Sentencia switch
                
                # 10. Expresión o asignación
                elif token_type == "Identificador":
                    if self.current_token_index + 1 < len(self.tokens) and self.tokens[self.current_token_index + 1][0] == "Operador de Asignación":
                        instrucciones.append(self.parse_expresion())  # Asignación
                    else:
                        instrucciones.append(self.parse_expresion())  # Expresión
                
                # 11. Delimitador (punto y coma)
                elif token_type == "Delimitador" and token_value == ";":
                    self.eat("Delimitador")  # Consumir ';' (instrucción vacía)
                
                # 12. Token inesperado
                else:
                    raise SyntaxError(f"Token inesperado '{token_type}: {token_value}'")
        
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


"""
"""
tokens = [('Token de Acceso', 'public', 1, 1), ('Palabra Reservada', 'class', 1, 8), ('Identificador', 'MiClase', 1, 14), ('Delimitador', '{', 1, 22), ('Token de Acceso', 'private', 2, 5), ('Tipo de dato', 'int', 2, 13), ('Identificador', 'x', 2, 17), ('Delimitador', ';', 2, 18), ('Token de Acceso', 'public', 4, 5), ('Palabra Reservada', 'void', 4, 12), ('Identificador', 'metodo', 4, 17), ('Delimitador', '(', 4, 23), ('Delimitador', ')', 4, 24), ('Delimitador', '{', 4, 26), ('Identificador', 'x', 5, 9), ('Operador de Asignación', '=', 5, 11), ('Número', '10', 5, 13), ('Delimitador', ';', 5, 15), ('Delimitador', '}', 6, 5), ('Delimitador', '}', 7, 1)]
parsear = Parser(tokens)
parsear.parse()
