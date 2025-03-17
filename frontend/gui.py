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

    page.file_content = ""  # Inicializar el contenido del archivo

    # Instancia única de Home_page, Lexico_page, Sintactico_page
    page.page_h = None
    page.page_l = None
    page.page_s = None

    # Función para construir contenido específico de cada página
    def build_page_content(page_name, page):
        if page_name == "home":

            if not page.page_h:
                page.page_h = Home_page(page, page.file_content)

            content = page.page_h.buil_page()
            page.file_content = page.page_h.file_content  # Actualizar el contenido del archivo
            return content

        elif page_name == "lexico":
            
            if not page.page_l:
                page.page_l = Lexico_page(page, page.file_content)
            
            content = page.page_l.buil_page()
            page.file_content = page.page_l.file_content
            return content
        
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
