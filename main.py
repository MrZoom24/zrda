import flet as ft

def main(page: ft.Page):
    page.title = "zrda"
    page.controls.append(ft.Text("Hello, world!"))

ft.run(main)