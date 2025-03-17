import flet as ft

class Header:
    def __init__(self,page, navigate_to):
        self.page = page
        self.navigate_to = navigate_to

    def logo_name(self):
        return ft.Row(
                    controls=[
                        ft.Text("JavThon", size=24, weight=ft.FontWeight.BOLD, color="black"),
                        ft.Image(src="../public/cobra.png", width=30, height=30)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )

    def barra_navegacion(self):
        return ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Home", 
                            icon=ft.icons.HOME, 
                            bgcolor="#AAAAAA" if self.page.current_page == "home" else "#D9D9D9", 
                            color="white" if self.page.current_page == "home" else "black", 
                            on_click=lambda e: self.navigate_to("home")
                        ),
                        ft.ElevatedButton(
                            "Lexico", 
                            icon=ft.icons.TABLE_CHART, 
                            bgcolor="#AAAAAA" if self.page.current_page == "lexico" else "#D9D9D9", 
                            color="white" if self.page.current_page == "lexico" else "black", 
                            on_click=lambda e: self.navigate_to("lexico")
                        ),
                        ft.ElevatedButton(
                            "Sintactico", 
                            icon=ft.icons.PARK_SHARP, 
                            bgcolor="#AAAAAA" if self.page.current_page == "sintactico" else "#D9D9D9", 
                            color="white" if self.page.current_page == "sintactico" else "black", 
                            on_click=lambda e: self.navigate_to("sintactico")
                        ),
                        ft.ElevatedButton(
                            "Semantico", 
                            icon=ft.icons.LIGHTBULB, 
                            bgcolor="#AAAAAA" if self.page.current_page == "semantico" else "#D9D9D9", 
                            color="white" if self.page.current_page == "semantico" else "black", 
                            on_click=lambda e: self.navigate_to("semantico")
                        ),
                        ft.ElevatedButton(
                            "Cod medio", 
                            icon=ft.icons.CODE_OUTLINED, 
                            bgcolor="#AAAAAA" if self.page.current_page == "cod_medio" else "#D9D9D9", 
                            color="white" if self.page.current_page == "cod_medio" else "black", 
                            on_click=lambda e: self.navigate_to("cod_medio")
                        ),
                        ft.ElevatedButton(
                            "Optimizacion", 
                            icon=ft.icons.SETTINGS, 
                            bgcolor="#AAAAAA" if self.page.current_page == "optimizacion" else "#D9D9D9", 
                            color="white" if self.page.current_page == "optimizacion" else "black", 
                            on_click=lambda e: self.navigate_to("optimizacion")
                        ),
                        ft.ElevatedButton(
                            "Cod Final", 
                            icon=ft.icons.DONE_ALL, 
                            bgcolor="#AAAAAA" if self.page.current_page == "cod_final" else "#D9D9D9", 
                            color="white" if self.page.current_page == "cod_final" else "black", 
                            on_click=lambda e: self.navigate_to("cod_final")
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    wrap= self.page.width < 800,  # Envolver botones en varias filas si la ventana es pequeña
                    scroll=ft.ScrollMode.AUTO if self.page.width < 800 else None,  # Habilitar scroll si la ventana es pequeña
                )
    
    def header_componet(self):
        padding_top = 10 if self.page.current_page != "home" else 0
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.logo_name(),
                    self.barra_navegacion()
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.only(top=padding_top)
        )