# Importamos la clase ASTNode del analizador sintáctico
from backend.analizador_sintactico import ASTNode

class PythonCodeGenerator:
    def __init__(self):
        self.code = []
        self.indent_level = 0
        self.current_class = None
        self.java_to_python_types = {
            "int": "int",
            "float": "float",
            "double": "float",
            "boolean": "bool",
            "String": "str",
            "char": "str",
            "void": "None"
        }
        self.java_to_python_operators = {
            "&&": "and",
            "||": "or",
            "!": "not",
            "==": "==",
            "!=": "!=",
            "<": "<",
            ">": ">",
            "<=": "<=",
            ">=": ">=",
            "+": "+",
            "-": "-",
            "*": "*",
            "/": "/",
            "%": "%"
        }

    def _add_line(self, line):
        """Añade una línea de código con la indentación correcta."""
        self.code.append("    " * self.indent_level + line)

    def _add_comment(self, comment):
        """Añade un comentario con la indentación correcta."""
        self._add_line(f"# {comment}")

    def generate(self, node):
        """Genera el código Python completo a partir del AST."""
        if node is None:
            return "\n".join(self.code)
        
        # Si es una lista de nodos, visitamos cada uno
        if isinstance(node, list):
            for n in node:
                if n:
                    n.accept(self)
        else:
            # Si es un solo nodo, lo visitamos
            if node:
                node.accept(self)
        
        return "\n".join(self.code)

    # Métodos de visita para cada tipo de nodo
    # Estos métodos serán llamados por el método accept de ASTNode

    def visit_Bloque(self, node):
        """Visita un bloque de instrucciones."""
        for instruccion in node.hijos:
            if instruccion:
                instruccion.accept(self)

    def visit_Declaracion(self, node):
        """Visita una declaración de variable."""
        tipo = node.valor
        modificadores = []
        identificador = None
        valor_inicial = None
        
        # Extraer modificadores, identificador y valor inicial
        for hijo in node.hijos:
            if isinstance(hijo, list) and all(isinstance(mod, str) for mod in hijo):
                modificadores = hijo
            elif isinstance(hijo, ASTNode) and hijo.tipo == "Identificador":
                identificador = hijo.valor
            elif isinstance(hijo, ASTNode) and hijo.tipo == "Expresion":
                valor_inicial = hijo
            elif isinstance(hijo, str) and hijo == "=":
                # Es el operador de asignación
                pass
        
        # Generar código para la declaración
        if identificador:
            # Si hay un valor inicial, generamos la asignación
            if valor_inicial:
                valor_str = self._generate_expression(valor_inicial)
                self._add_line(f"{identificador} = {valor_str}")
            else:
                # Inicialización por defecto según el tipo
                default_value = self._get_default_value(tipo)
                self._add_line(f"{identificador} = {default_value}")
        
        # Si es una declaración de clase, añadimos un comentario
        if "class" in modificadores:
            self._add_comment(f"Declaración de clase {identificador}")

    def _get_default_value(self, tipo):
        """Retorna el valor por defecto para un tipo de dato Java."""
        defaults = {
            "int": "0",
            "float": "0.0",
            "double": "0.0",
            "boolean": "False",
            "String": '""',
            "char": '""'
        }
        return defaults.get(tipo, "None")

    def _generate_expression(self, node):
        """Genera código para una expresión."""
        if node.tipo == "Expresion":
            # Si es una expresión con operador
            if len(node.hijos) >= 2:
                operador = node.valor
                izquierda = node.hijos[0]
                derecha = node.hijos[1] if len(node.hijos) > 1 else None
                
                izq_str = self._generate_expression(izquierda) if isinstance(izquierda, ASTNode) else str(izquierda)
                der_str = self._generate_expression(derecha) if isinstance(derecha, ASTNode) and derecha else ""
                
                # Convertir operadores Java a Python
                py_operador = self.java_to_python_operators.get(operador, operador)
                
                if der_str:
                    return f"({izq_str} {py_operador} {der_str})"
                else:
                    return f"{py_operador}{izq_str}"
            else:
                # Si es una expresión simple (un valor)
                return str(node.valor)
        elif node.tipo == "Identificador" or node.tipo == "Operando":
            return str(node.valor)
        elif node.tipo == "Valor":
            return str(node.valor)
        else:
            # Para otros tipos de nodos
            return str(node.valor) if hasattr(node, 'valor') and node.valor is not None else ""

    def visit_Asignacion(self, node):
        """Visita una asignación."""
        identificador = None
        expresion = None
        
        # Extraer identificador y expresión
        if len(node.hijos) >= 2:
            if isinstance(node.hijos[0], ASTNode) and node.hijos[0].tipo == "Identificador":
                identificador = node.hijos[0].valor
            
            if isinstance(node.hijos[1], ASTNode):
                expresion = node.hijos[1]
        
        if identificador and expresion:
            valor_str = self._generate_expression(expresion)
            self._add_line(f"{identificador} = {valor_str}")

    def visit_If(self, node):
        """Visita una sentencia if."""
        condicion = None
        cuerpo_if = None
        cuerpo_else = None
        
        # Extraer condición y cuerpos
        if len(node.hijos) >= 2:
            condicion = node.hijos[0]
            cuerpo_if = node.hijos[1]
            if len(node.hijos) > 2:
                cuerpo_else = node.hijos[2]
        
        if condicion and cuerpo_if:
            condicion_str = self._generate_expression(condicion)
            self._add_line(f"if {condicion_str}:")
            
            # Visitar el cuerpo del if
            self.indent_level += 1
            cuerpo_if.accept(self)
            self.indent_level -= 1
            
            # Si hay un else
            if cuerpo_else:
                self._add_line("else:")
                self.indent_level += 1
                cuerpo_else.accept(self)
                self.indent_level -= 1

    def visit_IfElse(self, node):
        """Visita una sentencia if-else."""
        condicion = node.valor
        cuerpo_if = None
        cuerpo_else = None
        
        # Extraer cuerpos
        if len(node.hijos) >= 2:
            cuerpo_if = node.hijos[0]
            cuerpo_else = node.hijos[1]
        
        condicion_str = self._generate_expression(condicion)
        self._add_line(f"if {condicion_str}:")
        
        # Visitar el cuerpo del if
        self.indent_level += 1
        cuerpo_if.accept(self)
        self.indent_level -= 1
        
        # Visitar el cuerpo del else
        self._add_line("else:")
        self.indent_level += 1
        cuerpo_else.accept(self)
        self.indent_level -= 1

    def visit_While(self, node):
        """Visita una sentencia while."""
        condicion = None
        cuerpo = None
        
        # Extraer condición y cuerpo
        if len(node.hijos) >= 2:
            condicion = node.hijos[0]
            cuerpo = node.hijos[1]
        
        if condicion and cuerpo:
            condicion_str = self._generate_expression(condicion)
            self._add_line(f"while {condicion_str}:")
            
            # Visitar el cuerpo del while
            self.indent_level += 1
            cuerpo.accept(self)
            self.indent_level -= 1

    def visit_DoWhile(self, node):
        """Visita una sentencia do-while."""
        cuerpo = None
        condicion = None
        
        # Extraer cuerpo y condición
        if len(node.hijos) >= 2:
            cuerpo = node.hijos[0]
            condicion = node.hijos[1]
        
        if cuerpo and condicion:
            # En Python no hay do-while, así que lo simulamos
            self._add_line("# Simulación de do-while")
            self._add_line("while True:")
            
            # Visitar el cuerpo del do-while
            self.indent_level += 1
            cuerpo.accept(self)
            
            # Añadir la condición de salida
            condicion_str = self._generate_expression(condicion)
            self._add_line(f"if not ({condicion_str}):")
            self.indent_level += 1
            self._add_line("break")
            self.indent_level -= 2

    def visit_For(self, node):
        """Visita una sentencia for."""
        inicializacion = None
        condicion = None
        actualizacion = None
        cuerpo = None
        
        # Extraer inicialización, condición, actualización y cuerpo
        if len(node.hijos) >= 4:
            inicializacion = node.hijos[0]
            condicion = node.hijos[1]
            actualizacion = node.hijos[2]
            cuerpo = node.hijos[3]
        
        if inicializacion and condicion and actualizacion and cuerpo:
            # En Java: for (inicializacion; condicion; actualizacion) { cuerpo }
            # En Python: inicializacion; while condicion: cuerpo; actualizacion
            
            # Inicialización
            if inicializacion.tipo == "Expresion":
                init_str = self._generate_expression(inicializacion)
                self._add_line(f"{init_str}")
            else:
                inicializacion.accept(self)
            
            # Condición y bucle
            condicion_str = self._generate_expression(condicion)
            self._add_line(f"while {condicion_str}:")
            
            # Cuerpo
            self.indent_level += 1
            cuerpo.accept(self)
            
            # Actualización
            if actualizacion.tipo == "Expresion":
                update_str = self._generate_expression(actualizacion)
                self._add_line(f"{update_str}")
            else:
                actualizacion.accept(self)
            
            self.indent_level -= 1

    def visit_Funcion(self, node):
        """Visita una declaración de función."""
        tipo_retorno = node.valor
        modificadores = []
        nombre_funcion = None
        parametros = []
        cuerpo = None
        
        # Extraer modificadores, nombre, parámetros y cuerpo
        if len(node.hijos) >= 4:
            modificadores = node.hijos[0]
            nombre_funcion = node.hijos[1]
            parametros = node.hijos[2]
            cuerpo = node.hijos[3]
        
        if nombre_funcion and cuerpo:
            # Generar la definición de la función
            params_str = ", ".join([f"{param[1]}" for param in parametros]) if parametros else ""
            
            # Si estamos dentro de una clase, añadimos 'self' como primer parámetro
            if self.current_class and "static" not in modificadores:
                params_str = f"self{', ' + params_str if params_str else ''}"
            
            self._add_line(f"def {nombre_funcion}({params_str}):")
            
            # Visitar el cuerpo de la función
            self.indent_level += 1
            cuerpo.accept(self)
            
            # Si la función tiene un tipo de retorno que no es void, añadimos un return por defecto
            if tipo_retorno != "void" and not self._has_return(cuerpo):
                default_return = self._get_default_value(tipo_retorno)
                self._add_line(f"return {default_return}")
            
            self.indent_level -= 1
            self._add_line("")  # Línea en blanco después de la función

    def _has_return(self, node):
        """Verifica si un nodo contiene una sentencia return."""
        # Esta es una implementación simplificada
        # En una implementación real, deberíamos recorrer todo el árbol
        return False

    def visit_Clase(self, node):
        """Visita una declaración de clase."""
        modificadores = []
        nombre_clase = None
        miembros = []
        
        # Extraer modificadores, nombre y miembros
        if len(node.hijos) >= 3:
            modificadores = node.hijos[0]
            nombre_clase = node.hijos[1]
            miembros = node.hijos[2]
        
        if nombre_clase:
            # Guardar la clase actual
            old_class = self.current_class
            self.current_class = nombre_clase
            
            # Generar la definición de la clase
            self._add_line(f"class {nombre_clase}:")
            
            # Si no hay miembros, añadimos un pass
            if not miembros:
                self.indent_level += 1
                self._add_line("pass")
                self.indent_level -= 1
            else:
                # Visitar los miembros de la clase
                self.indent_level += 1
                
                # Añadir el constructor __init__ si no existe
                if not self._has_constructor(miembros):
                    self._add_line("def __init__(self):")
                    self.indent_level += 1
                    self._add_line("pass")
                    self.indent_level -= 1
                    self._add_line("")
                
                # Visitar cada miembro
                for miembro in miembros:
                    miembro.accept(self)
                
                self.indent_level -= 1
            
            # Restaurar la clase anterior
            self.current_class = old_class
            self._add_line("")  # Línea en blanco después de la clase

    def _has_constructor(self, miembros):
        """Verifica si hay un constructor en los miembros de la clase."""
        # Esta es una implementación simplificada
        # En una implementación real, deberíamos buscar un método con el mismo nombre que la clase
        return False

    def visit_TryCatch(self, node):
        """Visita una sentencia try-catch."""
        bloque_try = None
        excepcion = None
        bloque_catch = None
        
        # Extraer bloques try y catch, y la excepción
        if len(node.hijos) >= 3:
            bloque_try = node.hijos[0]
            excepcion = node.hijos[1]
            bloque_catch = node.hijos[2]
        
        if bloque_try and excepcion and bloque_catch:
            # Generar el bloque try
            self._add_line("try:")
            self.indent_level += 1
            bloque_try.accept(self)
            self.indent_level -= 1
            
            # Generar el bloque except
            tipo_excepcion, nombre_excepcion = excepcion
            # Mapear tipos de excepción de Java a Python
            py_excepcion = self._map_exception_type(tipo_excepcion)
            
            self._add_line(f"except {py_excepcion} as {nombre_excepcion}:")
            self.indent_level += 1
            bloque_catch.accept(self)
            self.indent_level -= 1

    def _map_exception_type(self, java_exception):
        """Mapea un tipo de excepción de Java a su equivalente en Python."""
        exception_map = {
            "Exception": "Exception",
            "RuntimeException": "RuntimeError",
            "IOException": "IOError",
            "FileNotFoundException": "FileNotFoundError",
            "NullPointerException": "AttributeError",
            "IndexOutOfBoundsException": "IndexError",
            "ArithmeticException": "ArithmeticError",
            "IllegalArgumentException": "ValueError"
        }
        return exception_map.get(java_exception, "Exception")

    def visit_Switch(self, node):
        """Visita una sentencia switch."""
        expresion = None
        casos = []
        caso_default = None
        
        # Extraer expresión, casos y caso por defecto
        if len(node.hijos) >= 3:
            expresion = node.hijos[0]
            casos = node.hijos[1]
            caso_default = node.hijos[2]
        
        if expresion:
            # En Python no hay switch, así que lo simulamos con if-elif-else
            expr_str = self._generate_expression(expresion)
            
            # Generar los casos
            first_case = True
            for valor, instrucciones in casos:
                valor_str = self._generate_expression(valor)
                if first_case:
                    self._add_line(f"if {expr_str} == {valor_str}:")
                    first_case = False
                else:
                    self._add_line(f"elif {expr_str} == {valor_str}:")
                
                self.indent_level += 1
                instrucciones.accept(self)
                self.indent_level -= 1
            
            # Generar el caso por defecto
            if caso_default:
                self._add_line("else:")
                self.indent_level += 1
                caso_default.accept(self)
                self.indent_level -= 1

    # Métodos de visita genéricos para cada tipo de nodo en el AST
    # Estos métodos serán llamados por el método accept de ASTNode

    def visit_Expresion(self, node):
        """Visita una expresión y genera el código correspondiente."""
        expr_str = self._generate_expression(node)
        self._add_line(expr_str)

    def visit_Identificador(self, node):
        """Visita un identificador."""
        # Normalmente no necesitamos hacer nada aquí, ya que los identificadores
        # se manejan dentro de otras estructuras
        pass

    def visit_Operando(self, node):
        """Visita un operando."""
        # Similar a los identificadores, normalmente se manejan dentro de expresiones
        pass

    def visit_Valor(self, node):
        """Visita un valor literal."""
        # Similar a los identificadores, normalmente se manejan dentro de expresiones
        pass

    def visit_Print(self, node):
        """Visita una sentencia System.out.println o System.out.print."""
        tipo = node.valor  # 'System.out.println' o 'System.out.print'
        argumentos = node.hijos

        if tipo == "System.out.println":
            newline = True
        elif tipo == "System.out.print":
            newline = False
        else:
            newline = True  # Por seguridad

        # Verificar si hay concatenación de strings con otros tipos
        contenido = []
        for arg in argumentos:
            if isinstance(arg, ASTNode):
                contenido.append(self._generate_expression(arg))
            else:
                contenido.append(str(arg))

        # Si hay operaciones de concatenación con +, convertimos a formato de print con comas
        # para evitar errores de tipo en Python
        if any("+" in c for c in contenido):
            # Intentamos detectar concatenaciones de string con variables
            # y las convertimos a formato de print con comas
            new_content = []
            for item in contenido:
                if "+" in item and not (item.startswith('"') and item.endswith('"')):
                    # Dividir por + y procesar cada parte
                    parts = item.replace("(", "").replace(")", "").split("+")
                    for i, part in enumerate(parts):
                        part = part.strip()
                        if part.startswith('"') and part.endswith('"'):
                            # Es un string literal
                            new_content.append(part)
                        else:
                            # Es una variable o expresión
                            new_content.append(part)
                else:
                    new_content.append(item)
            
            # Usar comas para separar los argumentos en print
            joined_content = ", ".join(new_content)
        else:
            # No hay concatenación con +, usamos el formato original
            joined_content = " + ".join(contenido)

        if newline:
            self._add_line(f"print({joined_content})")
        else:
            self._add_line(f"print({joined_content}, end='')")

    def visit_Break(self, node):
        self._add_line("break")

    def visit_Switch(self, node):
        """Visita una sentencia switch."""
        expresion = node.hijos[0]
        self._add_line("# Simulación de switch con if-elif-else en Python")

        expr_str = self._generate_expression(expresion)

        first_case = True
        for child in node.hijos[1:]:
            if child.tipo == "Case":
                valor = child.hijos[0]
                instrucciones = child.hijos[1]

                valor_str = self._generate_expression(valor)
                if first_case:
                    self._add_line(f"if {expr_str} == {valor_str}:")
                    first_case = False
                else:
                    self._add_line(f"elif {expr_str} == {valor_str}:")

                self.indent_level += 1
                instrucciones.accept(self)
                self.indent_level -= 1

            elif child.tipo == "Default":
                self._add_line("else:")
                self.indent_level += 1
                child.hijos[0].accept(self)  # Instrucciones del default
                self.indent_level -= 1

    def visit_ExpresionUnaria(self, node):
        operador = node.valor  # operador++_post o ++, --, etc.
        hijo = node.hijos[0].accept(self)  # Genera el código del operando

        if operador == "++":
            return f"{hijo} = {hijo} + 1"
        elif operador == "--":
            return f"{hijo} = {hijo} - 1"
        elif operador == "++_post":
            return f"{hijo}++;"
        elif operador == "--_post":
            return f"{hijo}--;"
        else:
            raise Exception(f"Operador unario desconocido: {operador}")

    # Método genérico para manejar cualquier tipo de nodo no reconocido
    def visit_ASTNode(self, node):
        """Método genérico para visitar un nodo AST no reconocido."""
        self._add_comment(f"Nodo no manejado específicamente: {node.tipo}")
        
        # Si el nodo tiene hijos, los visitamos
        if hasattr(node, 'hijos') and node.hijos:
            for hijo in node.hijos:
                if isinstance(hijo, ASTNode):
                    hijo.accept(self)
