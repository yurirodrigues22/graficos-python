import flet as ft
import pandas as pd
from app.db import consultar
from app.charts import gerar_grafico
from app.helpers import is_color_dark
from flet import icons

def render_tab(page: ft.Page, titulo: str, opcoes_map: dict, cor: str, metric_label: str):
    bg = page.theme.color_scheme.background
    fg = page.theme.color_scheme.on_background
    card_bg = bg
    border_color = "#e6e6e6" if not is_color_dark(bg) else "#333333"
    shadow = ft.BoxShadow(color="#00000011", blur_radius=8, offset=ft.Offset(0, 2)) if not is_color_dark(bg) else None

    analise_label = ft.Text("Escolha a análise", size=14, weight="bold", color=fg)
    dropdown_analise = ft.Dropdown(
        options=[ft.dropdown.Option(k) for k in opcoes_map.keys()],
        value=list(opcoes_map.keys())[0],
        width=320, color=fg, bgcolor=bg, border_color=fg
    )

    chart_label = ft.Text("Tipo de Visualização", size=14, weight="bold", color=fg)
    dropdown_chart = ft.Dropdown(
        options=[ft.dropdown.Option("Gráfico de Barras"), ft.dropdown.Option("Gráfico de Pizza")],
        value="Gráfico de Barras", width=320, color=fg, bgcolor=bg, border_color=fg
    )

    kpi_card = ft.Container(
        content=ft.Column([
            ft.Icon(icons.PEOPLE, size=28, color="#EAA900"),
            ft.Text("0", size=28, weight="bold", color=fg),
            ft.Text(metric_label, size=12, color=fg)
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.padding.all(16),
        width=140,
        border_radius=12,
        bgcolor=card_bg,
        border=ft.border.all(1, border_color),
        shadow=shadow
    )

    tabela = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Categoria", color=fg)), ft.DataColumn(ft.Text("Quantidade", color=fg))],
        rows=[], width=320
    )
    tabela_box = ft.Container(tabela, padding=8, height=370, width=320, bgcolor=card_bg, border_radius=12, border=ft.border.all(1, border_color), shadow=shadow)

    grafico_img = ft.Image(expand=True, fit=ft.ImageFit.CONTAIN)
    grafico_box = ft.Container(grafico_img, expand=True, padding=16, bgcolor=card_bg, border_radius=12, border=ft.border.all(1, border_color))

    def atualizar(e=None):
        analise_key = opcoes_map[dropdown_analise.value]
        labels, valores = consultar(analise_key)
        df = pd.DataFrame({"Categoria": labels, "Quantidade": valores})

        total = int(df["Quantidade"].sum()) if not df.empty else 0
        kpi_card.content.controls[1].value = f"{total}"

        tabela.rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(str(cat), color=fg)), ft.DataCell(ft.Text(str(qtd), color=fg))]) for cat, qtd in zip(labels, valores)]

        img64 = gerar_grafico(df, dropdown_chart.value, cor, bg_color=bg, text_color=fg)
        grafico_img.src_base64 = img64 if img64 else None

        page.update()

    dropdown_analise.on_change = atualizar
    dropdown_chart.on_change = atualizar

    left_panel = ft.ListView([
        ft.Container(ft.Text(titulo, size=20, weight="bold", color=fg), padding=ft.padding.only(bottom=6)),
        ft.Container(analise_label, padding=ft.padding.only(bottom=2)),
        ft.Container(dropdown_analise, padding=ft.padding.only(bottom=6)),
        ft.Container(chart_label, padding=ft.padding.only(bottom=2)),
        ft.Container(dropdown_chart, padding=ft.padding.only(bottom=6)),
        kpi_card,
        tabela_box
    ], width=360, padding=ft.padding.all(12), spacing=12)

    right_panel = ft.Container(ft.Column([grafico_box], expand=True), padding=ft.padding.all(12), expand=True)

    layout = ft.Row([left_panel, right_panel], expand=True, spacing=36, alignment=ft.alignment.center)

    atualizar()
    return layout
