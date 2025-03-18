import flet as ft
from backend.analizador_lexico import lexer


class Lexico_page():
    def __init__(self, page, code=""):
        self.page = page
        self.code = code  # Guardar el contenido del archivo
        self.tokens = []
        self.table = ft.Column()  # Control para la tabla

    def update_code(self, code):
        self.code = code
        self.tokens = lexer(self.code)  # Obtener los tokens

    def update_table(self):
        self.table.controls.clear()  # Limpiar la tabla
        
        # Encabezado de la tabla
        table_controls = [
            ft.Text("Análisis Léxico:", weight=ft.FontWeight.BOLD, color="black"),
            ft.Row(
                controls=[
                    ft.Text("Tipos de Tokens", width=200,weight=ft.FontWeight.BOLD, color="black"),
                    ft.Text("Valores", width=200,weight=ft.FontWeight.BOLD, color="black"),
                    ft.Text("Posiciones (Línea, Columna)",weight=ft.FontWeight.BOLD, width=200, color="black"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(thickness=1, color="black"),
        ]

        # Agregar los tokens obtenidos
        if self.tokens:
            for token_type, value, line, column in self.tokens:
                table_controls.append(
                    ft.Row(
                        controls=[
                            ft.Text(token_type, width=200, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Text(value, width=200, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Text(f"({line}, {column})", width=200, weight=ft.FontWeight.BOLD, color="black"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                )
        else:
            table_controls.append(ft.Text("No se encontraron tokens", color="red"))

        # Actualizar la tabla y refrescar la página
        self.table.controls.extend(table_controls)
        self.page.update()

    def buil_page(self):
        # Asegurar que la tabla esté actualizada al construir la página
        self.update_table()

        return ft.Column(
            controls=[
                self.table  # Mostrar la tabla de tokens aquí
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            scroll="adaptive"  # Permitir scroll si la tabla crece demasiado
        )
