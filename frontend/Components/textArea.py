import flet as ft

class TextArea():
    def __init__(self, page):
        self.page = page

    def textArea_component(self):
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
            height= self.page.width * 0.315 if self.page.width < 1270 else 500,
        )