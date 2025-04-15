import flet as ft
from pages.Home import Home_page
from pages.Lexico import Lexico_page
from pages.sintactico import Sintactico_page
from pages.semantico import Semantico_page
from pages.cod_final import CodFinal_page
from Components.header import Header

def main(page: ft.Page):
    page.title = "JavThon - Compilador"
    page.bgcolor = "#EAEAEA"
    page.padding = 20
    page.scroll = True  # Habilitar scroll en la página

    # Estado de la página actual
    page.current_page = "home"

    page.file_content = ""  # Inicializar el contenido del archivo
    page.tokens = None # Inicializar lista de tokens

    # Instancia única de cada página
    page.page_h = None
    page.page_l = None
    page.page_s = None
    page.page_sem = None
    page.page_cf = None

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
            
            page.page_l.update_code(page.file_content)  # Actualizar el contenido 
            page.tokens = page.page_l.tokens
            content = page.page_l.buil_page()
            return content
        
        elif page_name == "sintactico":
            if not page.page_l:
                page.page_l = Lexico_page(page, page.file_content)  # Asegurar que Lexico_page está inicializado

            page.page_l.update_code(page.file_content)  # Asegurar que los tokens están actualizados
            page.page_s = Sintactico_page(page, page.page_l)            

            content = page.page_s.buil_page()
            return content

        elif page_name == "semantico":
            if not page.page_s:
                # Si no hay análisis sintáctico, redirigir a esa página
                page.current_page = "sintactico"
                return build_page_content("sintactico", page)
            
            page.page_sem = Semantico_page(page, page.page_s)
            content = page.page_sem.buil_page()
            return content

        elif page_name == "cod_final":
            if not page.page_sem:
                # Si no hay análisis semántico, redirigir a esa página
                page.current_page = "semantico"
                return build_page_content("semantico", page)
            
            page.page_cf = CodFinal_page(page, page.page_sem)
            content = page.page_cf.buil_page()
            return content

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
    
    # Agregar método de navegación al objeto page para que sea accesible desde otras clases
    page.navigate_to = navigate_to

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
