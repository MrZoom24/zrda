import flet as ft
from database import init_db, save_season, get_active_season, save_habit

def main(page: ft.Page):
    page.title = "zrda"
    init_db()

    def show_habit_screen(season_id, season_index):
        habit_name_field = ft.TextField(label="Habit name", width=250)
        habit_points_field = ft.TextField(label="Points for completing", width=250)
        error_text = ft.Text(value="", color=ft.Colors.RED)
        habits_list_display = ft.Column()
        added_habits = []

        def add_habit(e):
            name = (habit_name_field.value or "").strip()
            points_raw = (habit_points_field.value or "").strip()

            if not name:
                error_text.value = "Habit name can't be empty."
                return
            if not points_raw.isdigit() or int(points_raw) <= 0:
                error_text.value = "Points must be a whole number greater than zero."
                return
            
            points = int(points_raw)
            save_habit(season_id, name, points)

            added_habits.append(name)
            habits_list_display.controls.append(ft.Text(f"✓ {name} ({points} pts)"))

            habit_name_field.value = ""
            habit_points_field.value = ""
            error_text.value = ""

        def finish_habits(e):
            if not added_habits:
                error_text.value = "Add at least one habit before continuing."
                return
            
            # Placeholder confirmation. I will replace this with reflection screen
            page.controls.clear()
            page.controls.append(
                ft.Text(f"Season {season_index}: {len(added_habits)} habit(s) saved.")
            )

        page.controls.clear()
        page.controls.append(
            ft.Column(
                controls=[
                    ft.Text("Add your habits for this season.", size=20),
                    ft.Text(
                        "(Binary yes/no habits only for now.)",
                        italic=True,
                        size=12,
                    ),
                    habit_name_field,
                    habit_points_field,
                    ft.ElevatedButton("Add habit", on_click=add_habit),
                    error_text,
                    habits_list_display,
                    ft.ElevatedButton("Done adding habits", on_click=finish_habits),
                ]
            )
        )

    def show_setup_screen():
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
            season_id, season_index = save_season(season_length, block_length)

            show_habit_screen(season_id, season_index)

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
    
    def show_active_season(season_row):
        _, season_index, season_length, block_length, start_date, _ = season_row

        page.controls.append(
            ft.Column(
                controls=[
                    ft.Text(f"Season {season_index} is active", size=20),
                    ft.Text(f"Started: {start_date}"),
                    ft.Text(f"Length: {season_length} days"),
                    ft.Text(f"Block length: {block_length} days"),
                ]
            )
        )
    
    active_season = get_active_season()
    if active_season is None:
        show_setup_screen()
    else:
        show_active_season(active_season)

ft.run(main)