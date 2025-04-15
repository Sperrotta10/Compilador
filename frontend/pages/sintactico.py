import flet as ft
import os
import time
from backend.analizador_sintactico import Parser

class Sintactico_page():
    def __init__(self, page, lexico_page):
        self.page = page
        self.lexico_page = lexico_page  # Instancia de Lexico_page
        self.result_text = ft.Text("", color="black")  # Mensaje de resultado del análisis

        # Variables para el desplazamiento
        self.offset_x = 0
        self.offset_y = 0
        self.zoom_factor = 1.0  # Factor de zoom inicial

        # Imagen del árbol sintáctico
        self.image = None
        self.generated_image_path = None

        # Contenedor con detector de gestos para mover y hacer zoom en la imagen
        self.image_container = ft.GestureDetector(
            content=ft.Stack(
                controls=[
                    ft.Container(
                        content=self.image,
                        left=self.offset_x,
                        top=self.offset_y,
                        alignment=ft.alignment.center,
                        border=ft.border.all(1, "gray"),
                        border_radius=10,
                        bgcolor="#f8f8f8",
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,  # Evita que la imagen salga del contenedor
                    )
                ],
                width=500,
                height=400,
            ),
            on_pan_update=self.mover_imagen,
            on_scale_update=self.zoom_imagen
        )


    def limpiar_imagenes(self):
        """Eliminar imágenes generadas cuando el usuario navega o cierra la página"""
        if self.generated_image_path and os.path.exists(self.generated_image_path):
            try:
                os.remove(self.generated_image_path)
                print(f"🗑 Imagen eliminada: {self.generated_image_path}")
            except Exception as e:
                print(f"❌ Error al eliminar la imagen: {e}")

    def analizar_codigo(self, e):
        """Función que se ejecuta cuando el usuario presiona 'Analizar Código'"""
        tokens = self.lexico_page.get_tokens()
        print("Tokens recibidos en Sintactico_page: \n", tokens)

        if tokens:
            try:
                # Generar un nombre único para la imagen
                timestamp = int(time.time())
                image_path = f"arbol_sintactico_{timestamp}.png"

                self.limpiar_imagenes()

                parsear = Parser(tokens)  # Crear el analizador sintáctico
                ast = parsear.parse()  # Asumimos que el parseo devuelve un AST

                print("✅ Análisis sintáctico exitoso.")

                # Verificar si la imagen fue creada y su ruta
                self.generated_image_path = ast.graficar_mpl(output_filename=image_path)

                if os.path.exists(self.generated_image_path):
                    self.image = ft.Image(
                        src=self.generated_image_path,
                        width=int(500 * self.zoom_factor),
                        height=int(400 * self.zoom_factor),
                        visible=True
                    )

                    self.image_container.content.controls[0] = ft.Container(
                        content=self.image,
                        left=self.offset_x,
                        top=self.offset_y,
                        alignment=ft.alignment.center,
                        border=ft.border.all(1, "gray"),
                        border_radius=10,
                        bgcolor="#f8f8f8",
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    )

                    self.image_container.update()

                    self.result_text.value = "✅ Análisis sintáctico exitoso. Árbol generado."
                    self.result_text.color = "green"
                else:
                    self.image.visible = False
                    self.result_text.value = "⚠ Análisis completado, pero no se encontró la imagen."
                    self.result_text.color = "orange"

            except Exception as ex:
                print("❌ Error en el análisis sintáctico:", ex)
                self.result_text.value = "❌ Error en el análisis sintáctico."
                self.result_text.color = "red"

        else:
            print("⚠ No se encontraron tokens para analizar")
            self.result_text.value = "⚠ No se encontraron tokens para analizar."
            self.result_text.color = "orange"

        self.page.update()


    def zoom_in(self, e=None):
        """Aumenta el zoom de la imagen"""
        self.zoom_factor += 0.2
        self.image.width = int(500 * self.zoom_factor)
        self.image.height = int(400 * self.zoom_factor)
        #self.image.update()
        self.page.update()

    def zoom_out(self, e=None):
        """Disminuye el zoom de la imagen"""
        if self.zoom_factor > 0.4:  # Evita que sea demasiado pequeño
            self.zoom_factor -= 0.2
            self.image.width = int(500 * self.zoom_factor)
            self.image.height = int(400 * self.zoom_factor)
        self.image.update()
        self.page.update()

    def zoom_imagen(self, e):
        """Permite hacer zoom en la imagen con gestos"""
        self.zoom_factor *= e.scale
        self.image.width = int(500 * self.zoom_factor)
        self.image.height = int(400 * self.zoom_factor)
        self.image.update()
        self.page.update()

    def mover_imagen(self, e):
        """Mueve la imagen al arrastrarla con el mouse o el dedo"""
        self.offset_x += e.delta_x
        self.offset_y += e.delta_y

        # Actualizar la posición de la imagen dentro del Stack
        image_container = self.image_container.content.controls[0]
        image_container.left = self.offset_x
        image_container.top = self.offset_y
        image_container.update()
        self.page.update()

    def buil_page(self):
        
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Esquema del Árbol:", weight=ft.FontWeight.BOLD, color="black"),
                    padding=ft.padding.only(top=20)
                ),
                # Contenedor de la imagen con zoom y movimiento
                self.image_container,
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Zoom In 🔍➕", bgcolor="#64A6F5", color="white", on_click=self.zoom_in),
                        ft.ElevatedButton("Zoom Out 🔍➖", bgcolor="#64A6F5", color="white", on_click=self.zoom_out),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Generar Árbol Sintáctico",
                            bgcolor="#64A6F5",
                            color="white",
                            width=200,
                            height=50,
                            on_click=self.analizar_codigo
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=80,
                ),
                ft.Container(content=self.result_text, padding=ft.padding.only(top=20)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
