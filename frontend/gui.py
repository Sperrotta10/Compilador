import flet as ft

def main(page: ft.Page):
    page.title = "JavThon - Compilador"
    page.bgcolor = "#EAEAEA"
    page.padding = 20
    page.scroll = True  # Habilitar scroll en la página

    # Estado de la página actual
    page.current_page = "home"

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
                        ft.ElevatedButton(
                            "Home", 
                            icon=ft.icons.HOME, 
                            bgcolor="#AAAAAA" if page.current_page == "home" else "#D9D9D9", 
                            color="white" if page.current_page == "home" else "black", 
                            on_click=lambda e: navigate_to("home")
                        ),
                        ft.ElevatedButton(
                            "Lexico", 
                            icon=ft.icons.TABLE_CHART, 
                            bgcolor="#AAAAAA" if page.current_page == "lexico" else "#D9D9D9", 
                            color="white" if page.current_page == "lexico" else "black", 
                            on_click=lambda e: navigate_to("lexico")
                        ),
                        ft.ElevatedButton(
                            "Sintactico", 
                            icon=ft.icons.PARK_SHARP, 
                            bgcolor="#AAAAAA" if page.current_page == "sintactico" else "#D9D9D9", 
                            color="white" if page.current_page == "sintactico" else "black", 
                            on_click=lambda e: navigate_to("sintactico")
                        ),
                        ft.ElevatedButton(
                            "Semantico", 
                            icon=ft.icons.LIGHTBULB, 
                            bgcolor="#AAAAAA" if page.current_page == "semantico" else "#D9D9D9", 
                            color="white" if page.current_page == "semantico" else "black", 
                            on_click=lambda e: navigate_to("semantico")
                        ),
                        ft.ElevatedButton(
                            "Cod medio", 
                            icon=ft.icons.CODE_OUTLINED, 
                            bgcolor="#AAAAAA" if page.current_page == "cod_medio" else "#D9D9D9", 
                            color="white" if page.current_page == "cod_medio" else "black", 
                            on_click=lambda e: navigate_to("cod_medio")
                        ),
                        ft.ElevatedButton(
                            "Optimizacion", 
                            icon=ft.icons.SETTINGS, 
                            bgcolor="#AAAAAA" if page.current_page == "optimizacion" else "#D9D9D9", 
                            color="white" if page.current_page == "optimizacion" else "black", 
                            on_click=lambda e: navigate_to("optimizacion")
                        ),
                        ft.ElevatedButton(
                            "Cod Final", 
                            icon=ft.icons.DONE_ALL, 
                            bgcolor="#AAAAAA" if page.current_page == "cod_final" else "#D9D9D9", 
                            color="white" if page.current_page == "cod_final" else "black", 
                            on_click=lambda e: navigate_to("cod_final")
                        )
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

    # Función para construir contenido específico de cada página
    def build_page_content(page_name):
        if page_name == "home":
            return ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("Código Java:", weight=ft.FontWeight.BOLD, color="black"),
                        padding=ft.padding.only(top=20)
                    ),
                    ft.Container(content=build_code_container(), padding=ft.padding.only(bottom=20)),
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
        elif page_name == "lexico":
            return ft.Text("Página de Análisis Léxico")
        elif page_name == "sintactico":
            return ft.Text("Página de Análisis Sintáctico")
        elif page_name == "semantico":
            return ft.Text("Página de Análisis Semántico")
        elif page_name == "cod_medio":
            return ft.Text("Página de Código Intermedio")
        elif page_name == "optimizacion":
            return ft.Text("Página de Optimización")
        elif page_name == "cod_final":
            return ft.Text("Página de Código Final")

    # Función para navegar entre páginas
    def navigate_to(page_name):
        page.current_page = page_name
        page.clean()
        page.add(
            build_header(),
            ft.Divider(thickness=1, color="black"),
            build_page_content(page_name)
        )
        page.update()

    # Función para actualizar el diseño al cambiar el tamaño de la ventana
    def update_layout(e):
        page.clean()
        page.add(
            build_header(),
            ft.Divider(thickness=1, color="black"),
            build_page_content(page.current_page)
        )
        page.update()

    # Escuchar cambios en el tamaño de la ventana
    page.on_resized = update_layout

    # Actualizar el diseño al iniciar la aplicación
    navigate_to("home")

ft.app(target=main)
