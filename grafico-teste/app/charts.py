import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def gerar_grafico(df: pd.DataFrame, chart_type: str, cor: str, bg_color: str, text_color: str):
    if df.empty:
        return None

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    if chart_type == "Gráfico de Barras":
        sns.barplot(data=df, x="Categoria", y="Quantidade", ax=ax, color=cor)
        ax.tick_params(colors=text_color)
        ax.yaxis.label.set_color(text_color)
        ax.xaxis.label.set_color(text_color)
        for spine in ax.spines.values():
            spine.set_color(text_color)
        for lbl in ax.get_xticklabels():
            lbl.set_color(text_color)
    else:
        colors = ["#2563EB", "#3B82F6", "#60A5FA", "#93C5FD", "#FACC15", "#EAB308"]
        wedges, texts, autotexts = ax.pie(
            df["Quantidade"],
            labels=df["Categoria"],
            autopct="%1.1f%%",
            startangle=90,
            colors=colors[:len(df)],
            textprops={'color': text_color}
        )
        ax.axis("equal")

    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("utf-8")
