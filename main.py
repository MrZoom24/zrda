import flet as ft
from database import init_db, save_season

def main(page: ft.Page):
    page.title = "zrda"
    init_db()

    season_field = ft.TextField(label="Season length (days)", width=250)
    block_field = ft.TextField(label="Block length (days)", width=250)
    error_text = ft.Text(value="", color=ft.Colors.RED)

    def start_season(e):
        season_raw = (season_field.value or "").strip()
        block_raw = (block_field.value or "").strip()

        if not season_raw.isdigit():
            error_text.value = "Season length must be a whole number."
            return
        if not block_raw.isdigit():
            error_text.value = "Block length must be a whole number."
            return
        
        season_length = int(season_raw)
        block_length = int(block_raw)

        if season_length <= 0 or block_length <= 0:
            error_text.value = "Both lengths must be greater than zero."
            return
        if block_length > season_length:
            error_text.value = "Block length can't be longer than the season."
            return
        
        error_text.value = ""
        season_index = save_season(season_length, block_length)

        page.controls.clear()
        page.controls.append(
            ft.Text(
                f"Season {season_index} started: {season_length} days, "
                f"split into blocks of {block_length} days."
            )
        )

    page.controls.append(
        ft.Column(
            controls=[
                ft.Text("Let's set up your first season.", size=20),
                season_field,
                block_field,
                error_text,
                ft.ElevatedButton("Continue", on_click=start_season),
            ]
        )
    )

ft.run(main)