class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Stack of scopes, starting with global scope
        self.current_scope = 0
        self.errors = []

    def enter_scope(self):
        """Create a new scope."""
        self.scopes.append({})
        self.current_scope += 1

    def exit_scope(self):
        """Exit the current scope."""
        if self.current_scope > 0:
            self.scopes.pop()
            self.current_scope -= 1

    def declare(self, name, type_info, line=None, column=None, is_initialized=False, is_constant=False):
        """Declare a symbol in the current scope."""
        if name in self.scopes[self.current_scope]:
            self.errors.append(f"Error semántico: Variable '{name}' ya declarada en este ámbito (línea {line}, columna {column})")
            return False
        
        self.scopes[self.current_scope][name] = {
            'type': type_info,
            'line': line,
            'column': column,
            'initialized': is_initialized,
            'constant': is_constant
        }
        return True

    def lookup(self, name):
        """Look up a symbol in all accessible scopes."""
        # Search from current scope up to global scope
        for i in range(self.current_scope, -1, -1):
            if name in self.scopes[i]:
                return self.scopes[i][name]
        return None

    def update(self, name, is_initialized=True):
        """Update a symbol's initialization status."""
        for i in range(self.current_scope, -1, -1):
            if name in self.scopes[i]:
                self.scopes[i][name]['initialized'] = is_initialized
                return True
        return False


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.current_class = None
        self.current_function = None
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

    def analyze(self, ast):
        """Analyze the AST for semantic errors."""
        if ast is None:
            return False
        
        self._analyze_node(ast)
        return len(self.errors) == 0

    def _analyze_node(self, node):
        """Recursively analyze a node in the AST."""
        if node is None:
            return
        
        # Process node based on its type
        if node.tipo == "Bloque":
            self._analyze_block(node)
        elif node.tipo == "Declaracion":
            self._analyze_declaration(node)
        elif node.tipo == "Asignacion":
            self._analyze_assignment(node)
        elif node.tipo == "Expresion":
            self._analyze_expression(node)
        elif node.tipo == "If" or node.tipo == "IfElse":
            self._analyze_if_statement(node)
        elif node.tipo == "While":
            self._analyze_while_statement(node)
        elif node.tipo == "DoWhile":
            self._analyze_do_while_statement(node)
        elif node.tipo == "For":
            self._analyze_for_statement(node)
        elif node.tipo == "Funcion":
            self._analyze_function(node)
        elif node.tipo == "Clase":
            self._analyze_class(node)
        elif node.tipo == "TryCatch":
            self._analyze_try_catch(node)
        elif node.tipo == "Switch":
            self._analyze_switch(node)
        else:
            # Process children for other node types
            if isinstance(node.hijos, list):
                for hijo in node.hijos:
                    if hijo is not None:
                        self._analyze_node(hijo)

    def _analyze_block(self, node):
        """Analyze a block of code."""
        self.symbol_table.enter_scope()
        
        for hijo in node.hijos:
            self._analyze_node(hijo)
        
        self.symbol_table.exit_scope()

    def _analyze_declaration(self, node):
        """Analyze a variable declaration."""
        tipo_dato = node.valor  # Type of the variable
        
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
        
        if identificador is None:
            self.errors.append(f"Error semántico: Declaración sin identificador")
            return
        
        # Check if the type is valid
        if tipo_dato not in self.java_to_python_types and tipo_dato != "void":
            self.errors.append(f"Error semántico: Tipo de dato '{tipo_dato}' no reconocido")
            return
        
        # Check if it's a constant
        is_constant = "final" in modificadores
        
        # Declare the variable in the symbol table
        line = column = None  # In a real implementation, you'd get these from the token
        is_initialized = valor_inicial is not None
        
        self.symbol_table.declare(
            identificador, 
            tipo_dato, 
            line, 
            column, 
            is_initialized, 
            is_constant
        )
        
        # Analyze the initial value if present
        if valor_inicial is not None:
            self._analyze_node(valor_inicial)
            
            # Check type compatibility for initialization
            if hasattr(valor_inicial, 'tipo') and valor_inicial.tipo == "Expresion":
                valor_tipo = self._get_expression_type(valor_inicial)
                if not self._are_types_compatible(tipo_dato, valor_tipo):
                    self.errors.append(
                        f"Error semántico: No se puede asignar valor de tipo '{valor_tipo}' a variable de tipo '{tipo_dato}'"
                    )

    def _analyze_assignment(self, node):
        """Analyze an assignment statement."""
        # The left side should be an identifier
        left_node = None
        right_node = None
        
        if len(node.hijos) >= 2:
            left_node = node.hijos[0]
            right_node = node.hijos[1]
        
        if left_node is None or not hasattr(left_node, 'tipo') or left_node.tipo != "Identificador":
            self.errors.append(f"Error semántico: El lado izquierdo de la asignación debe ser un identificador")
            return
        
        # Check if the variable exists
        var_name = left_node.valor
        var_info = self.symbol_table.lookup(var_name)
        
        if var_info is None:
            self.errors.append(f"Error semántico: Variable '{var_name}' no declarada")
            return
        
        # Check if it's a constant that's already initialized
        if var_info['constant'] and var_info['initialized']:
            self.errors.append(f"Error semántico: No se puede modificar la constante '{var_name}'")
            return
        
        # Analyze the right side
        if right_node is not None:
            self._analyze_node(right_node)
            
            # Check type compatibility
            right_type = self._get_expression_type(right_node)
            if not self._are_types_compatible(var_info['type'], right_type):
                self.errors.append(
                    f"Error semántico: No se puede asignar valor de tipo '{right_type}' a variable de tipo '{var_info['type']}'"
                )
        
        # Mark the variable as initialized
        self.symbol_table.update(var_name)

    def _analyze_expression(self, node):
        """Analyze an expression."""
        # Process all operands in the expression
        if isinstance(node.hijos, list):
            for hijo in node.hijos:
                self._analyze_node(hijo)
        
        # If it's a variable reference, check if it's declared and initialized
        if node.tipo == "Identificador":
            var_name = node.valor
            var_info = self.symbol_table.lookup(var_name)
            
            if var_info is None:
                self.errors.append(f"Error semántico: Variable '{var_name}' no declarada")
            elif not var_info['initialized']:
                self.errors.append(f"Error semántico: Variable '{var_name}' usada antes de ser inicializada")

    def _analyze_if_statement(self, node):
        """Analyze an if statement."""
        # Analyze the condition
        if len(node.hijos) >= 1:
            condition = node.hijos[0]
            self._analyze_node(condition)
            
            # Check if the condition is a boolean expression
            condition_type = self._get_expression_type(condition)
            if condition_type != "boolean" and condition_type is not None:
                self.errors.append(f"Error semántico: La condición del if debe ser de tipo boolean, no '{condition_type}'")
        
        # Analyze the if block
        if len(node.hijos) >= 2:
            self._analyze_node(node.hijos[1])
        
        # Analyze the else block if present
        if len(node.hijos) >= 3 and node.tipo == "IfElse":
            self._analyze_node(node.hijos[2])

    def _analyze_while_statement(self, node):
        """Analyze a while statement."""
        # Analyze the condition
        if len(node.hijos) >= 1:
            condition = node.hijos[0]
            self._analyze_node(condition)
            
            # Check if the condition is a boolean expression
            condition_type = self._get_expression_type(condition)
            if condition_type != "boolean" and condition_type is not None:
                self.errors.append(f"Error semántico: La condición del while debe ser de tipo boolean, no '{condition_type}'")
        
        # Analyze the loop body
        if len(node.hijos) >= 2:
            self._analyze_node(node.hijos[1])

    def _analyze_do_while_statement(self, node):
        """Analyze a do-while statement."""
        # Analyze the loop body
        if len(node.hijos) >= 1:
            self._analyze_node(node.hijos[0])
        
        # Analyze the condition
        if len(node.hijos) >= 2:
            condition = node.hijos[1]
            self._analyze_node(condition)
            
            # Check if the condition is a boolean expression
            condition_type = self._get_expression_type(condition)
            if condition_type != "boolean" and condition_type is not None:
                self.errors.append(f"Error semántico: La condición del do-while debe ser de tipo boolean, no '{condition_type}'")

    def _analyze_for_statement(self, node):
        """Analyze a for statement."""
        self.symbol_table.enter_scope()
        
        # Analyze initialization
        if len(node.hijos) >= 1:
            self._analyze_node(node.hijos[0])
        
        # Analyze condition
        if len(node.hijos) >= 2:
            condition = node.hijos[1]
            self._analyze_node(condition)
            
            # Check if the condition is a boolean expression
            condition_type = self._get_expression_type(condition)
            if condition_type != "boolean" and condition_type is not None:
                self.errors.append(f"Error semántico: La condición del for debe ser de tipo boolean, no '{condition_type}'")
        
        # Analyze update
        if len(node.hijos) >= 3:
            self._analyze_node(node.hijos[2])
        
        # Analyze loop body
        if len(node.hijos) >= 4:
            self._analyze_node(node.hijos[3])
        
        self.symbol_table.exit_scope()

    def _analyze_function(self, node):
        """Analyze a function declaration."""
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
        
        # Save current function for return type checking
        prev_function = self.current_function
        self.current_function = {
            'name': nombre_funcion,
            'return_type': tipo_retorno,
            'has_return': False
        }
        
        # Enter a new scope for the function body
        self.symbol_table.enter_scope()
        
        # Declare parameters in the function scope
        for param_type, param_name in parametros:
            self.symbol_table.declare(param_name, param_type, None, None, True, False)
        
        # Analyze the function body
        if cuerpo is not None:
            self._analyze_node(cuerpo)
        
        # Check if the function has a return statement if needed
        if tipo_retorno != "void" and not self.current_function['has_return']:
            self.errors.append(f"Error semántico: La función '{nombre_funcion}' debe retornar un valor de tipo '{tipo_retorno}'")
        
        # Exit the function scope
        self.symbol_table.exit_scope()
        
        # Restore previous function context
        self.current_function = prev_function

    def _analyze_class(self, node):
        """Analyze a class declaration."""
        # Extract information from the class declaration
        modificadores = []
        nombre_clase = None
        miembros = []
        
        if len(node.hijos) >= 3:
            modificadores = node.hijos[0]
            nombre_clase = node.hijos[1]
            miembros = node.hijos[2]
        
        # Save current class for context
        prev_class = self.current_class
        self.current_class = nombre_clase
        
        # Enter a new scope for the class
        self.symbol_table.enter_scope()
        
        # Analyze class members
        if isinstance(miembros, list):
            for miembro in miembros:
                self._analyze_node(miembro)
        
        # Exit the class scope
        self.symbol_table.exit_scope()
        
        # Restore previous class context
        self.current_class = prev_class

    def _analyze_try_catch(self, node):
        """Analyze a try-catch statement."""
        # Analyze the try block
        if len(node.hijos) >= 1:
            self._analyze_node(node.hijos[0])
        
        # Extract exception information
        if len(node.hijos) >= 2:
            exception_info = node.hijos[1]
            if isinstance(exception_info, tuple) and len(exception_info) == 2:
                exception_type, exception_name = exception_info
                
                # Enter a new scope for the catch block
                self.symbol_table.enter_scope()
                
                # Declare the exception variable
                self.symbol_table.declare(exception_name, exception_type, None, None, True, False)
                
                # Analyze the catch block
                if len(node.hijos) >= 3:
                    self._analyze_node(node.hijos[2])
                
                # Exit the catch scope
                self.symbol_table.exit_scope()

    def _analyze_switch(self, node):
        """Analyze a switch statement."""
        # Analyze the switch expression
        if len(node.hijos) >= 1:
            self._analyze_node(node.hijos[0])
        
        # Analyze case blocks
        if len(node.hijos) >= 2:
            casos = node.hijos[1]
            if isinstance(casos, list):
                for caso in casos:
                    if isinstance(caso, tuple) and len(caso) == 2:
                        valor, instrucciones = caso
                        self._analyze_node(valor)
                        self._analyze_node(instrucciones)
        
        # Analyze default block
        if len(node.hijos) >= 3 and node.hijos[2] is not None:
            self._analyze_node(node.hijos[2])

    def _get_expression_type(self, node):
        """Determine the type of an expression."""
        if node is None:
            return None
        
        if node.tipo == "Identificador":
            var_info = self.symbol_table.lookup(node.valor)
            return var_info['type'] if var_info else None
        
        elif node.tipo == "Número":
            # Determine if it's an integer or float
            if '.' in node.valor:
                return "float"
            else:
                return "int"
        
        elif node.tipo == "String Literal":
            return "String"
        
        elif node.tipo == "Literal Booleano":
            return "boolean"
        
        elif node.tipo == "Expresion":
            # For binary operations, determine the result type
            if len(node.hijos) >= 2:
                left_type = self._get_expression_type(node.hijos[0])
                right_type = self._get_expression_type(node.hijos[1])
                
                # Handle arithmetic operations
                if node.valor in ['+', '-', '*', '/', '%']:
                    if left_type in ["float", "double"] or right_type in ["float", "double"]:
                        return "float"
                    else:
                        return "int"
                
                # Handle relational operations
                elif node.valor in ['==', '!=', '<', '>', '<=', '>=']:
                    return "boolean"
                
                # Handle logical operations
                elif node.valor in ['&&', '||', '!']:
                    return "boolean"
        
        return None

    def _are_types_compatible(self, target_type, source_type):
        """Check if source_type can be assigned to target_type."""
        if target_type is None or source_type is None:
            return True  # Skip type checking if types are unknown
        
        # Same types are always compatible
        if target_type == source_type:
            return True
        
        # Numeric type conversions (widening)
        if target_type == "float" and source_type == "int":
            return True
        if target_type == "double" and source_type in ["int", "float"]:
            return True
        
        # String compatibility
        if target_type in ["String", "string"] and source_type in ["String", "string", "char"]:
            return True
        
        return False

    def get_errors(self):
        """Get all semantic errors."""
        return self.errors + self.symbol_table.errors
