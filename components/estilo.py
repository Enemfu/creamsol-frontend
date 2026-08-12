# ====
# components/estilo.py — CreamSol.io · Estilos Globais
# ====

import streamlit as st

COR_POSITIVO = "#2E7D32"
COR_NEGATIVO = "#C62828"
COR_NEUTRO   = "#757575"
COR_BORDA    = "#E0E0E0"
COR_CARD     = "#FFFFFF"


def aplicar_css():
    """Injeta o CSS global. Chamar imediatamente após st.set_page_config."""
    st.markdown("""
    <style>
    /* Fundo geral */
    .stApp { background-color: #F5F5F5; }
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }

    /* Cards genéricos */
    .cs-card {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.8rem;
    }

    /* Métrica */
    .cs-metric {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: left;
    }
    .cs-metric-label {
        font-size: 0.72rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.06em;
        color: #9E9E9E; margin-bottom: 0.3rem;
    }
    .cs-metric-valor {
        font-size: 1.5rem; font-weight: 800; color: #1A1A1A; line-height: 1.1;
    }
    .cs-metric-valor.pos { color: #2E7D32; }
    .cs-metric-valor.neg { color: #C62828; }
    .cs-metric-valor.nd  { color: #BDBDBD; font-size: 1.1rem; font-weight: 500; }

    /* Métricas coloridas */
    .cs-positivo { color: #2E7D32; font-weight: 700; }
    .cs-negativo { color: #C62828; font-weight: 700; }
    .cs-neutro   { color: #757575; }
    .cs-label    { color: #757575; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; }
    .cs-valor    { font-size: 1.45rem; font-weight: 700; color: #1A1A1A; }

    /* Secção */
    .cs-section-title {
        font-size: 0.78rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.1em;
        color: #9E9E9E; margin: 1.4rem 0 0.6rem 0;
    }

    /* Composição */
    .cs-comp-card {
        background: #FFFFFF; border: 1px solid #E0E0E0;
        border-radius: 10px; padding: 0.9rem 1.2rem;
        display: flex; flex-direction: column; gap: 0.2rem;
    }
    .cs-comp-label { font-size: 0.72rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.06em; }
    .cs-comp-valor { font-size: 1.15rem; font-weight: 700; color: #1A1A1A; }
    .cs-comp-pct   { font-size: 0.82rem; color: #757575; }

    /* Dust */
    .cs-dust-item {
        display: inline-block;
        background: #FAFAFA; border: 1px solid #E0E0E0;
        border-radius: 6px; padding: 3px 10px;
        font-size: 0.78rem; color: #757575; margin: 2px 3px;
    }

    /* Tabelas */
    thead tr th { background: #F5F5F5 !important; color: #424242 !important; font-size: 0.8rem; }
    tbody tr:hover { background: #FAFAFA !important; }

    /* Divisor */
    hr { border-color: #E0E0E0; margin: 0.8rem 0; }

    /* Badges */
    .cs-badge-ok { background:#E8F5E9; color:#2E7D32; border-radius:4px; padding:2px 7px; font-size:0.75rem; }
    .cs-badge-nd { background:#FFF3E0; color:#E65100; border-radius:4px; padding:2px 7px; font-size:0.75rem; }
    .cs-badge {
        display: inline-block;
        font-size: 0.7rem; font-weight: 700;
        letter-spacing: 0.08em; text-transform: uppercase;
        background: #E8F5E9; color: #2E7D32;
        border-radius: 4px; padding: 2px 10px;
        margin-left: 0.6rem; vertical-align: middle;
    }

    /* Logo */
    .cs-logo { font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em; color: #1A1A1A; }
    .cs-logo span { color: #C62828; }

    /* Aviso */
    .cs-aviso {
        background: #FAFAFA;
        border-left: 3px solid #BDBDBD;
        padding: 0.6rem 1rem;
        color: #757575;
        font-size: 0.78rem;
        border-radius: 0 6px 6px 0;
        margin-top: 1.5rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
    }
    </style>
    """, unsafe_allow_html=True)


def metrica_card(label: str, valor: str, sufixo: str = "", cor: str = "neutro"):
    cor_map = {"positivo": COR_POSITIVO, "negativo": COR_NEGATIVO, "neutro": COR_NEUTRO}
    c = cor_map.get(cor, COR_NEUTRO)
    st.markdown(f"""
    <div class="cs-card">
        <div class="cs-label">{label}</div>
        <div class="cs-valor" style="color:{c}">{valor} <span style="font-size:0.9rem;color:{COR_NEUTRO}">{sufixo}</span></div>
    </div>""", unsafe_allow_html=True)


def cor_pnl(valor_str: str) -> str:
    """Devolve classe CSS com base no sinal do valor."""
    if valor_str in ("N/D", "", None):
        return "cs-neutro"
    try:
        v = float(valor_str.replace("$", "").replace("€", "").replace("%", "").replace(",", "").strip())
        return "cs-positivo" if v > 0 else ("cs-negativo" if v < 0 else "cs-neutro")
    except Exception:
        return "cs-neutro"


def rodape():
    st.markdown("---")
    st.markdown(
        '<div class="cs-aviso">CreamSol.io · Dados meramente informativos. '
        'Nenhum dado é armazenado ou registado. Não constitui assessoria financeira.</div>',
        unsafe_allow_html=True,
    )