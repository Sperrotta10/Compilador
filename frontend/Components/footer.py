import flet as ft

class Footer:
    def __init__(self, page):
        self.page = page

    def footer_component(self):
        return ft.Container(
            content=ft.Column([
                ft.Divider(thickness=1, color="black"),
                ft.Row([
                    ft.Text("© 2025 JavThon Compilador. Todos los derechos reservados.", color="black"),
                    ft.Text("Desarrollado por: Santiago Perrotta y Manuel Nava", color="black")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]),
            padding=ft.Padding(10, 5, 10, 10),
            margin=ft.margin.only(top=20)
        ) 