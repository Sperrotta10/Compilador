import flet as ft

def main(page: ft.Page):
    page.title = "JavThon - Compilador"
    page.bgcolor = "#EAEAEA"
    page.padding = 20
    page.scroll = True  # Habilitar scroll en la página

    # Función para construir el encabezado
    def build_header():
        return ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("JavThon", size=24, weight=ft.FontWeight.BOLD, color="black"),
                        ft.Image(src="../public/cobra.png", width=30, height=30)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Home", icon=ft.icons.HOME, bgcolor="#D9D9D9", color="black"),
                        ft.ElevatedButton("Lexico", icon=ft.icons.TABLE_CHART, bgcolor="#D9D9D9", color="black"),
                        ft.ElevatedButton("Sintactico", icon=ft.icons.PARK_SHARP, bgcolor="#D9D9D9", color="black"),
                        ft.ElevatedButton("Semantico", icon=ft.icons.LIGHTBULB, bgcolor="#D9D9D9", color="black"),
                        ft.ElevatedButton("Cod medio", icon=ft.icons.CODE_OUTLINED, bgcolor="#D9D9D9", color="black"),
                        ft.ElevatedButton("Optimizacion", icon=ft.icons.SETTINGS, bgcolor="#D9D9D9", color="black"),
                        ft.ElevatedButton("Cod Final", icon=ft.icons.DONE_ALL, bgcolor="#D9D9D9", color="black")
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    wrap=page.width < 800,  # Envolver botones en varias filas si la ventana es pequeña
                    scroll=ft.ScrollMode.AUTO if page.width < 800 else None,  # Habilitar scroll si la ventana es pequeña
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    # Función para construir el área de texto
    def build_code_container():
        return ft.Container(
            content=ft.TextField(
                multiline=True,
                bgcolor="white",
                color="black",
                border_radius=0,
                border=None,
            ),
            bgcolor="white",
            border_radius=0,
            border=None,
            padding=5,
            width=800,
            height=page.width * 0.315 if page.width < 1270 else 500,
        )

    # Función para actualizar el diseño
    def update_layout(e):
        # Reconstruir los controles
        header = build_header()
        code_container = build_code_container()

        # Limpiar la página y agregar los controles actualizados
        page.clean()
        page.add(
            header,
            ft.Divider(thickness=1, color="black"),
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("Código Java:", weight=ft.FontWeight.BOLD, color="black"),
                        padding=ft.padding.only(top=20)
                    ),
                    ft.Container(content=code_container, padding=ft.padding.only(bottom=20)),
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
        )

    # Escuchar cambios en el tamaño de la ventana
    page.on_resize = update_layout

    # Actualizar el diseño al iniciar la aplicación
    update_layout(None)

ft.app(target=main)