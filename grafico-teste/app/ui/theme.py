import flet as ft

def tema_claro():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#015afe", background="#ffffff", on_background="#000000"
        ),
        tabs_theme=ft.TabsTheme(
            indicator_color="#015afe",
            unselected_label_color="#555555",
            label_color="#015afe"
        )
    )

def tema_escuro():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#93C5FD", background="#141414", on_background="#ffffff"
        ),
        tabs_theme=ft.TabsTheme(
            indicator_color="#93C5FD",
            unselected_label_color="#bbbbbb",
            label_color="#93C5FD"
        )
    )
