import flet as ft
from Components.textArea import TextArea

class Home_page():
    def __init__(self, page):
        self.page = page
        self.text_field = None
        self.file_picker = ft.FilePicker(on_result=self.read_file)
        self.page.add(self.file_picker)  # Agregar el FilePicker a la página

    def buil_page(self):

        component = TextArea(self.page)
        self.text_field = component.textField

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
                            ft.ElevatedButton("Analizar Código", bgcolor="#64A6F5", color="white", width=200, height=50)
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
                    code = file.read()
                    print(code)
                    self.text_field.value = code
                    print("Texto asignado al TextField")
                    self.page.update()
                    print("Página actualizada")
            else:
                print("Por favor, seleccione un archivo .java")

