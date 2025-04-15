import flet as ft
from backend.generador_codigo import CodeGenerator

class CodFinal_page:
    def __init__(self, page, semantico_page):
        self.page = page
        self.semantico_page = semantico_page
        self.ast = semantico_page.ast if hasattr(semantico_page, 'ast') else None
        self.code_generator = CodeGenerator()
        self.generated_code = ""
        self.generate_code()

        # Agregar FilePicker al inicializar
        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)

    def generate_code(self):
        """Generate Python code from the AST."""
        if self.ast:
            self.generated_code = self.code_generator.generate(self.ast)
        else:
            self.generated_code = "# No hay AST disponible para generar código.\n# Por favor, ejecute primero el análisis sintáctico y semántico."

    def buil_page(self):
        """Build the code generation page UI."""
        # Title
        title = ft.Text("Generación de Código Python", size=24, weight=ft.FontWeight.BOLD, color="black")
        
        # Code display
        code_display = ft.TextField(
            value=self.generated_code,
            multiline=True,
            min_lines=20,
            max_lines=30,
            read_only=True,
            width=800,
            border_color=ft.colors.GREY_400,
            bgcolor=ft.colors.WHITE,
            color="black"
        )

        # Copy button
        def copy_to_clipboard(e):
            self.page.set_clipboard(self.generated_code)
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("✅ Código copiado al portapapeles"),
                open=True,
                duration=2000
            )
            self.page.update()
        
        copy_button = ft.ElevatedButton(
            "Copiar Código",
            on_click=copy_to_clipboard,
            icon=ft.icons.COPY
        )

        # Save button usando FilePicker
        def save_to_file(e):
            # Llamamos al método para mostrar el cuadro de diálogo de guardar
            self.file_picker.save_file(
                dialog_title="Guardar como archivo .py",
                file_name="codigo_generado.py",
                allowed_extensions=["py"]
            )

        # Función para manejar el resultado después de la selección de archivo
        def on_file_saved(result):
            if result.path:
                try:
                    with open(result.path, "w", encoding="utf-8") as f:
                        f.write(self.generated_code)
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text("✅ Código guardado exitosamente"),
                        open=True,
                        duration=2000
                    )
                    self.page.update()
                except Exception as ex:
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"❌ Error al guardar archivo: {ex}"),
                        open=True,
                        duration=2000
                    )
                    self.page.update()

        # Asignar el manejador de resultados
        self.file_picker.on_result = on_file_saved
        
        save_button = ft.ElevatedButton(
            "Guardar como .py",
            on_click=save_to_file,
            icon=ft.icons.SAVE
        )

        # Main container
        return ft.Container(
            content=ft.Column([
                title,
                ft.Text("Código Python generado:", size=16, weight=ft.FontWeight.BOLD, color="black"),
                code_display,
                ft.Row([copy_button, save_button], alignment=ft.MainAxisAlignment.CENTER)
            ]),
            padding=20,
            width=800
        )
