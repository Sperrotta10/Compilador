import flet as ft
from pages.Home import Home_page
from pages.Lexico import Lexico_page
from pages.Sintactico import Sintactico_page
from Components.header import Header

def main(page: ft.Page):
    page.title = "JavThon - Compilador"
    page.bgcolor = "#EAEAEA"
    page.padding = 20
    page.scroll = True  # Habilitar scroll en la página

    # Estado de la página actual
    page.current_page = "home"

    # Función para construir contenido específico de cada página
    def build_page_content(page_name, page):
        if page_name == "home":

            page_h = Home_page(page)
            return page_h.buil_page()

        elif page_name == "lexico":
            
            page_l = Lexico_page(page)
            return page_l.buil_page()
        
        elif page_name == "sintactico":
            
            page_s = Sintactico_page(page)
            return page_s.buil_page()

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
        nonlocal page  
        page.current_page = page_name
        page.clean()
        page.add(
            Header(page, navigate_to).header_componet(), 
            ft.Divider(thickness=1, color="black"),
            build_page_content(page_name, page)
        )
        page.update()

    # Función para actualizar el diseño al cambiar el tamaño de la ventana
    def update_layout(e):
        page.clean()
        page.add(
            Header(page, navigate_to).header_componet(),
            ft.Divider(thickness=1, color="black"),
            build_page_content(page.current_page, page)
        )
        page.update()

    # Escuchar cambios en el tamaño de la ventana
    page.on_resized = update_layout

    # Actualizar el diseño al iniciar la aplicación
    navigate_to("home")

ft.app(target=main)
