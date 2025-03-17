import flet as ft
from Components.textArea import TextArea

class Sintactico_page():
    def __init__(self, page):
        self.page = page

    def buil_page(self):

        component = TextArea(self.page)

        return ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("Esquema del Arbol:", weight=ft.FontWeight.BOLD, color="black"),
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
