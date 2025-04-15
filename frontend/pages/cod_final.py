import flet as ft
from backend.generar_codigo2 import PythonCodeGenerator

class CodFinal_page:
    def __init__(self, page, semantico_page):
        self.page = page
        self.semantico_page = semantico_page
        self.ast = semantico_page.ast if hasattr(semantico_page, 'ast') else None
        self.code_generator = PythonCodeGenerator()  # Usamos el visitor
        self.generated_code = ""
        self.generate_code()

        # Agregar FilePicker al inicializar
        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)

    def generate_code(self):
        """Generar código Python usando el visitor sobre el AST."""
        if self.ast:
            if isinstance(self.ast, list):
                for nodo in self.ast:
                    nodo.accept(self.code_generator)
            else:
                self.ast.accept(self.code_generator)
            self.generated_code = self.code_generator.generate(None)  # Retorna el código generado
        else:
            self.generated_code = (
                "# No hay AST disponible para generar código.\n"
                "# Por favor, ejecute primero el análisis sintáctico y semántico."
            )

    def buil_page(self):
        """Construir la interfaz de usuario para mostrar el código generado."""
        # Título
        title = ft.Text("Generación de Código Python", size=24, weight=ft.FontWeight.BOLD, color="black")
        
        # Área de visualización del código
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

        # Botón para copiar
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

        # Botón para guardar
        def save_to_file(e):
            self.file_picker.save_file(
                dialog_title="Guardar como archivo .py",
                file_name="codigo_generado.py",
                allowed_extensions=["py"]
            )

        # Manejador de guardado
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

        # Asignar manejador
        self.file_picker.on_result = on_file_saved
        
        save_button = ft.ElevatedButton(
            "Guardar como .py",
            on_click=save_to_file,
            icon=ft.icons.SAVE
        )

        # Contenedor principal
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