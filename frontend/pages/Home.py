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
                            ft.ElevatedButton("Cargar Archivo", bgcolor="#64A6F5", color="white", width=200, height=50, on_click=self.load_file),
                            ft.ElevatedButton("Analizar Código", bgcolor="#64A6F5", color="white", width=200, height=50, on_click=self.analizar)
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
        self.page.file_content = self.file_content  # Actualizar el contenido del archivo

