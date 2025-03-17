import flet as ft
from Components.textArea import TextArea

class Lexico_page():
    def __init__(self, page, file_content=""):
        self.page = page
        self.file_content = file_content  # Guardar el contenido del archivo

    def buil_page(self):

        component = TextArea(self.page)

        return ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("Tabla de tokens:", weight=ft.FontWeight.BOLD, color="black"),
                        padding=ft.padding.only(top=20)
                    ),
                    ft.Container(content=component.textArea_component(), padding=ft.padding.only(bottom=20)),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton("Cargar Archivo", bgcolor="#64A6F5", color="white", width=200, height=50),
                            ft.ElevatedButton("Analizar Código", bgcolor="#64A6F5", color="white", width=200, height=50)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=80,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
