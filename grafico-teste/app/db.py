from app.queries import QUERIES, FALLBACK
from app.helpers import _to_int_safe

try:
    from model.database import executar_select
except Exception as e:
    print("⚠️ Não foi possível importar executar_select:", e)
    executar_select = None

def consultar(analise: str):
    if analise not in QUERIES:
        return FALLBACK.get(analise, ([], []))
    if executar_select is None:
        return FALLBACK.get(analise, ([], []))
    try:
        rows = executar_select(QUERIES[analise])
        if not rows:
            return FALLBACK.get(analise, ([], []))
        labels = [r[0] for r in rows]
        valores = [_to_int_safe(r[1]) for r in rows]
        return labels, valores
    except Exception:
        return FALLBACK.get(analise, ([], []))
