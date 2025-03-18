import flet as ft
from Components.textArea import TextArea

class Home_page():
    def __init__(self, page, file_content=""):
        self.page = page
        self.text_field = None
        self.file_picker = ft.FilePicker(on_result=self.read_file)
        self.page.add(self.file_picker)  # Agregar el FilePicker a la página
        self.file_content = file_content  # Guardar el contenido del archivo

    def buil_page(self):

        component = TextArea(self.page)
        self.text_field = component.textField

        if self.file_content:  # Si hay contenido guardado, asignarlo al TextField
            self.text_field.value = self.file_content
            print("Asignando contenido al TextField:", self.file_content)

        # Guardar el contenido del TextField cada vez que se escriba
        self.text_field.on_change = self.update_file_content

        if not self.page.controls:  # Agregar el FilePicker solo si no hay controles en la página
            self.page.add(self.file_picker)

        return ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("Código Java:", weight=ft.FontWeight.BOLD, color="black"),
                        padding=ft.padding.only(top=20)
                    ),
                    ft.Container(content=component.textArea_component(), padding=ft.padding.only(bottom=20)),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton("Cargar Archivo", bgcolor="#64A6F5", color="white", width=200, height=50, on_click=self.on_button_click(self.load_file), on_hover=self.on_hover),
                            ft.ElevatedButton("Analizar Código", bgcolor="#64A6F5", color="white", width=200, height=50, on_click=self.on_button_click(self.analizar), on_hover=self.on_hover)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=80,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
    
    def load_file(self, e):
        self.file_picker.pick_files(allow_multiple=False)

    def read_file(self, e):
        if e.files:
            file_path = e.files[0].path
            if file_path.endswith(".java"):  # Verificar si el archivo es .java
                with open(file_path, "r") as file:
                    self.file_content = file.read()  # Guardar el contenido 
                    print(self.file_content)
                    self.text_field.value = self.file_content
                    print("Texto asignado al TextField")
                    self.page.update()
                    print("Página actualizada")
            else:
                print("Por favor, seleccione un archivo .java")

    def analizar(self, e):
        self.page.file_content = self.text_field.value  # Actualizar el contenido del archivo

    def update_file_content(self, e):
        # Guardamos el contenido actual del TextField en file_content
        self.file_content = self.text_field.value

    def on_hover(self,event):
        # Cambiar estilo cuando el mouse esté sobre el botón
        event.control.bgcolor = "#3D8BF4" if event.data == "true" else "#64A6F5"
        event.control.update()

    def on_button_click(self, original_func):
        """Funcion para aplicar el efecto de pulsación antes de ejecutar la función original."""
        def wrapper(e):
            e.control.bgcolor = "#2C6BA3"  # Color cuando el botón es presionado
            e.control.update()
            e.page.update()

            # Llamar a la función original
            original_func(e)

            # Volver al color original después de un pequeño retraso
            e.control.bgcolor = "#64A6F5"
            e.control.update()

        return wrapper

