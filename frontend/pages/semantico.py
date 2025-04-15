import flet as ft
from backend.analizador_semantico import SemanticAnalyzer

class Semantico_page:
    def __init__(self, page, sintactico_page):
        self.page = page
        self.sintactico_page = sintactico_page
        # Fix: Get the AST directly from the sintactico_page object
        self.ast = sintactico_page.ast if hasattr(sintactico_page, 'ast') else None
        self.semantic_analyzer = SemanticAnalyzer()
        self.errors = []
        self.analyze()
        # Add debug print to verify AST is received
        print(f"Semantic analyzer initialized with AST: {self.ast is not None}")

    def analyze(self):
        """Perform semantic analysis on the AST."""
        if self.ast:
            print("Starting semantic analysis...")
            success = self.semantic_analyzer.analyze(self.ast)
            self.errors = self.semantic_analyzer.get_errors()
            print(f"Semantic analysis completed. Found {len(self.errors)} errors.")
        else:
            self.errors = ["No hay AST disponible para analizar. Por favor, ejecute primero el análisis sintáctico."]
            print("No AST available for semantic analysis.")

    def buil_page(self):
        """Build the semantic analysis page UI."""
        # Title
        title = ft.Text("Análisis Semántico", size=24, weight=ft.FontWeight.BOLD, color="black")
        
        # Status indicator
        status_text = "Análisis completado sin errores" if not self.errors else f"Se encontraron {len(self.errors)} errores semánticos"
        status_color = ft.colors.GREEN if not self.errors else ft.colors.RED
        status = ft.Text(status_text, color=status_color, size=16)
        
        # Errors list
        errors_container = ft.Container(
            content=ft.Column(
                [ft.Text(error, color=ft.colors.RED) for error in self.errors] if self.errors else 
                [ft.Text("No se encontraron errores semánticos.", color=ft.colors.GREEN)],
                scroll=ft.ScrollMode.AUTO,
                spacing=10
            ),
            padding=10,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=5,
            bgcolor=ft.colors.WHITE,
            width=800,
            height=400,
            margin=ft.margin.only(top=20)
        )
        
        # Button to proceed to code generation
        next_button = ft.ElevatedButton(
            "Continuar a Generación de Código",
            on_click=lambda _: self.page.navigate_to("cod_final"),
            disabled=len(self.errors) > 0
        )
        
        # Main container
        return ft.Container(
            content=ft.Column([
                title,
                status,
                ft.Text("Resultados del análisis semántico:", size=16, weight=ft.FontWeight.BOLD, color="black"),
                errors_container,
                ft.Row([next_button], alignment=ft.MainAxisAlignment.CENTER)
            ]),
            padding=20,
            width=800
        )
