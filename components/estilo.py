import streamlit as st

COR_POSITIVO = "#2E7D32"
COR_NEGATIVO = "#C62828"
COR_NEUTRO   = "#757575"
COR_BORDA    = "#E0E0E0"
COR_CARD     = "#FFFFFF"

def injectar_css():
    st.markdown("""
    <style>
    /* Fundo geral */
    .stApp { background-color: #F5F5F5; }

    /* Remover padding excessivo */
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }

    /* Cards */
    .cs-card {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.8rem;
    }

    /* Métricas coloridas */
    .cs-positivo { color: #2E7D32; font-weight: 700; }
    .cs-negativo { color: #C62828; font-weight: 700; }
    .cs-neutro   { color: #757575; }
    .cs-label    { color: #757575; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; }
    .cs-valor    { font-size: 1.45rem; font-weight: 700; color: #1A1A1A; }

    /* Tabelas */
    thead tr th { background: #F0F0F0 !important; color: #424242 !important; font-size: 0.82rem; }
    tbody tr:hover { background: #FAFAFA !important; }

    /* Divisor */
    hr { border-color: #E0E0E0; margin: 0.8rem 0; }

    /* Badge verificado */
    .cs-badge-ok  { background:#E8F5E9; color:#2E7D32; border-radius:4px; padding:2px 7px; font-size:0.75rem; }
    .cs-badge-nd  { background:#FFF3E0; color:#E65100; border-radius:4px; padding:2px 7px; font-size:0.75rem; }

    /* Aviso */
    .cs-aviso {
        background: #FAFAFA;
        border-left: 3px solid #BDBDBD;
        padding: 0.6rem 1rem;
        color: #757575;
        font-size: 0.78rem;
        border-radius: 0 6px 6px 0;
    }

    /* Logo / título */
    .cs-logo { font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em; color: #1A1A1A; }
    .cs-logo span { color: #C62828; }
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
        v = float(valor_str.replace("$", "").replace("€","").replace("%","").replace(",","").strip())
        return "cs-positivo" if v > 0 else ("cs-negativo" if v < 0 else "cs-neutro")
    except Exception:
        return "cs-neutro"


def rodape():
    st.markdown("---")
    st.markdown('<div class="cs-aviso">CreamSol.io · Dados meramente informativos. Nenhum dado é armazenado ou registado. Não constitui assessoria financeira.</div>', unsafe_allow_html=True)

# components/estilo.py
def aplicar_css():
    import streamlit as st
    st.markdown("""<style>
    /* todo o CSS global aqui */
    </style>""", unsafe_allow_html=True)