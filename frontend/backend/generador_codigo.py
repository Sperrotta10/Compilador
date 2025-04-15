class CodeGenerator:
    def __init__(self):
        self.code = []
        self.indentation = 0
        self.class_name = None
        self.java_to_python_types = {
            'int': 'int',
            'float': 'float',
            'double': 'float',
            'boolean': 'bool',
            'char': 'str',
            'String': 'str',
            'string': 'str',
            'void': 'None'
        }

    def generate(self, ast):
        """Generate Python code from the AST."""
        if ast is None:
            return ""
        
        self._generate_node(ast)
        return "\n".join(self.code)

    def _add_line(self, line):
        """Add a line of code with proper indentation."""
        self.code.append("    " * self.indentation + line)

    def _generate_node(self, node):
        """Generate code for a node in the AST."""
        if node is None:
            return
        
        # Process node based on its type
        if node.tipo == "Bloque":
            self._generate_block(node)
        elif node.tipo == "Declaracion":
            self._generate_declaration(node)
        elif node.tipo == "Asignacion":
            self._generate_assignment(node)
        elif node.tipo == "Expresion":
            return self._generate_expression(node)
        elif node.tipo == "If" or node.tipo == "IfElse":
            self._generate_if_statement(node)
        elif node.tipo == "While":
            self._generate_while_statement(node)
        elif node.tipo == "DoWhile":
            self._generate_do_while_statement(node)
        elif node.tipo == "For":
            self._generate_for_statement(node)
        elif node.tipo == "Funcion":
            self._generate_function(node)
        elif node.tipo == "Clase":
            self._generate_class(node)
        elif node.tipo == "TryCatch":
            self._generate_try_catch(node)
        elif node.tipo == "Switch":
            self._generate_switch(node)
        elif node.tipo == "Identificador":
            return node.valor
        elif node.tipo == "Operando":
            return node.valor
        else:
            # Process children for other node types
            if isinstance(node.hijos, list):
                for hijo in node.hijos:
                    if hijo is not None:
                        self._generate_node(hijo)

    def _generate_block(self, node):
        """Generate code for a block of statements."""
        self.indentation += 1
        
        for hijo in node.hijos:
            self._generate_node(hijo)
        
        self.indentation -= 1
        
        # If indentation is 0 after a block, add an empty line for readability
        if self.indentation == 0:
            self._add_line("")

    def _generate_declaration(self, node):
        """Generate code for a variable declaration."""
        tipo_dato = node.valor
        
        # Extract information from the declaration
        modificadores = []
        identificador = None
        valor_inicial = None
        
        for hijo in node.hijos:
            if isinstance(hijo, list) and all(isinstance(item, str) for item in hijo):
                modificadores = hijo
            elif hijo is not None and hasattr(hijo, 'tipo') and hijo.tipo == "Identificador":
                identificador = hijo.valor
            elif hijo is not None and hasattr(hijo, 'tipo') and hijo.tipo in ["Expresion", "Asignacion"]:
                valor_inicial = hijo
        
        # In Python, we don't declare types, just assign values
        if valor_inicial is not None:
            valor_str = self._generate_expression(valor_inicial)
            self._add_line(f"{identificador} = {valor_str}")
        else:
            # Initialize with default values based on type
            if tipo_dato == "int":
                self._add_line(f"{identificador} = 0")
            elif tipo_dato in ["float", "double"]:
                self._add_line(f"{identificador} = 0.0")
            elif tipo_dato == "boolean":
                self._add_line(f"{identificador} = False")
            elif tipo_dato in ["String", "string"]:
                self._add_line(f"{identificador} = \"\"")
            elif tipo_dato == "char":
                self._add_line(f"{identificador} = \"\"")
            else:
                self._add_line(f"{identificador} = None")

    def _generate_assignment(self, node):
        """Generate code for an assignment statement."""
        left_node = node.hijos[0]
        right_node = node.hijos[1]
        
        left_str = self._generate_expression(left_node)
        right_str = self._generate_expression(right_node)
        
        self._add_line(f"{left_str} = {right_str}")

    def _generate_expression(self, node):
        """Generate code for an expression."""
        if node is None:
            return "None"
        
        if node.tipo == "Identificador":
            return node.valor
        
        elif node.tipo == "Operando":
            return node.valor
        
        elif node.tipo == "Número":
            return node.valor
        
        elif node.tipo == "String Literal":
            return node.valor
        
        elif node.tipo == "Literal Booleano":
            return "True" if node.valor.lower() == "true" else "False"
        
        elif node.tipo == "Literal Nulo":
            return "None"
        
        elif node.tipo == "Expresion":
            # For binary operations
            if len(node.hijos) >= 2:
                left_expr = self._generate_expression(node.hijos[0])
                right_expr = self._generate_expression(node.hijos[1])
                
                # Convert Java operators to Python
                operator = node.valor
                if operator == "&&":
                    operator = "and"
                elif operator == "||":
                    operator = "or"
                elif operator == "!":
                    operator = "not "
                
                return f"({left_expr} {operator} {right_expr})"
        
        elif node.tipo == "Asignacion":
            right_expr = self._generate_expression(node.hijos[1])
            return right_expr
        
        return "None"  # Default case

    def _generate_if_statement(self, node):
        """Generate code for an if statement."""
        # Generate the condition
        condition = self._generate_expression(node.hijos[0])
        self._add_line(f"if {condition}:")
        
        # Generate the if block
        self._generate_node(node.hijos[1])
        
        # Generate the else block if present
        if len(node.hijos) >= 3 and node.tipo == "IfElse":
            self._add_line("else:")
            self._generate_node(node.hijos[2])

    def _generate_while_statement(self, node):
        """Generate code for a while statement."""
        # Generate the condition
        condition = self._generate_expression(node.hijos[0])
        self._add_line(f"while {condition}:")
        
        # Generate the loop body
        self._generate_node(node.hijos[1])

    def _generate_do_while_statement(self, node):
        """Generate code for a do-while statement."""
        # Python doesn't have a do-while loop, so we simulate it
        self._add_line("while True:")
        
        # Generate the loop body
        self.indentation += 1
        self._generate_node(node.hijos[0])
        
        # Generate the condition check at the end
        condition = self._generate_expression(node.hijos[1])
        self._add_line(f"if not ({condition}):")
        self._add_line("    break")
        self.indentation -= 1

    def _generate_for_statement(self, node):
        """Generate code for a for statement."""
        # In Java: for (initialization; condition; update) { body }
        # Extract components
        initialization = node.hijos[0]
        condition = node.hijos[1]
        update = node.hijos[2]
        body = node.hijos[3]
        
        # Generate initialization before the loop
        init_code = self._generate_expression(initialization)
        if init_code and init_code != "None":
            self._add_line(init_code)
        
        # Generate the while loop with the condition
        cond_code = self._generate_expression(condition)
        self._add_line(f"while {cond_code}:")
        
        # Generate the loop body
        self.indentation += 1
        self._generate_node(body)
        
        # Add the update at the end of the loop body
        update_code = self._generate_expression(update)
        if update_code and update_code != "None":
            self._add_line(update_code)
        
        self.indentation -= 1

    def _generate_function(self, node):
        """Generate code for a function declaration."""
        tipo_retorno = node.valor
        
        # Extract information from the function declaration
        modificadores = []
        nombre_funcion = None
        parametros = []
        cuerpo = None
        
        if len(node.hijos) >= 4:
            modificadores = node.hijos[0]
            nombre_funcion = node.hijos[1]
            parametros = node.hijos[2]
            cuerpo = node.hijos[3]
        
        # Convert Java method name to Python function name
        if self.class_name and "static" not in modificadores:
            # Instance method, add self parameter
            param_str = "self"
            if parametros:
                param_str += ", " + ", ".join(param_name for _, param_name in parametros)
        else:
            # Static method or function outside class
            param_str = ", ".join(param_name for _, param_name in parametros)
        
        # Generate function definition
        python_return_type = self.java_to_python_types.get(tipo_retorno, "None")
        self._add_line(f"def {nombre_funcion}({param_str}):")
        
        # Generate function body
        if cuerpo is not None:
            self._generate_node(cuerpo)
        else:
            # Empty function body
            self._add_line("    pass")

    def _generate_class(self, node):
        """Generate code for a class declaration."""
        # Extract information from the class declaration
        modificadores = []
        nombre_clase = None
        miembros = []
        
        if len(node.hijos) >= 3:
            modificadores = node.hijos[0]
            nombre_clase = node.hijos[1]
            miembros = node.hijos[2]
        
        # Save the class name for method generation
        self.class_name = nombre_clase
        
        # Generate class definition
        self._add_line(f"class {nombre_clase}:")
        
        # Generate class members
        if isinstance(miembros, list) and miembros:
            for miembro in miembros:
                self._generate_node(miembro)
        else:
            # Empty class
            self._add_line("    pass")
        
        # Reset class name
        self.class_name = None

    def _generate_try_catch(self, node):
        """Generate code for a try-catch statement."""
        # Generate try block
        self._add_line("try:")
        self._generate_node(node.hijos[0])
        
        # Generate except block
        if len(node.hijos) >= 2:
            exception_info = node.hijos[1]
            if isinstance(exception_info, tuple) and len(exception_info) == 2:
                exception_type, exception_name = exception_info
                
                # Map Java exception types to Python
                python_exception = "Exception"  # Default
                if exception_type == "ArithmeticException":
                    python_exception = "ZeroDivisionError"
                elif exception_type == "NullPointerException":
                    python_exception = "AttributeError"
                elif exception_type == "IndexOutOfBoundsException":
                    python_exception = "IndexError"
                
                self._add_line(f"except {python_exception} as {exception_name}:")
                self._generate_node(node.hijos[2])

    def _generate_switch(self, node):
        """Generate code for a switch statement."""
        # Python doesn't have switch, so we use if-elif-else
        
        # Generate the switch expression
        switch_expr = self._generate_expression(node.hijos[0])
        
        # Generate case blocks
        first_case = True
        if len(node.hijos) >= 2:
            casos = node.hijos[1]
            if isinstance(casos, list):
                for caso in casos:
                    if isinstance(caso, tuple) and len(caso) == 2:
                        valor, instrucciones = caso
                        case_value = self._generate_expression(valor)
                        
                        if first_case:
                            self._add_line(f"if {switch_expr} == {case_value}:")
                            first_case = False
                        else:
                            self._add_line(f"elif {switch_expr} == {case_value}:")
                        
                        self._generate_node(instrucciones)
        
        # Generate default block
        if len(node.hijos) >= 3 and node.hijos[2] is not None:
            self._add_line("else:")
            self._generate_node(node.hijos[2])
