# ====
# pages/1_Beginner.py — CreamSol.io · Plano Iniciante (Gratuito)
# ====

import streamlit as st
import requests
import pandas as pd
import re
from config import API_BASE_URL

st.set_page_config(
    page_title="Iniciante · CreamSol.io",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.estilo import aplicar_css
aplicar_css()

# ── CSS local ────
st.markdown("""
<style>
.stApp { background-color: #F5F5F5; }
.block-container { padding-top: 3rem; padding-bottom: 2rem; max-width: 1100px; }

.cs-logo { font-size: 1.5rem; font-weight: 900; letter-spacing: -0.02em; color: #1A1A1A; }
.cs-logo span { color: #14F195; }   /* verde Solana */

.cs-badge {
    display: inline-block;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    background: #E8F5E9; color: #2E7D32;
    border-radius: 4px; padding: 2px 10px;
    margin-left: 0.6rem; vertical-align: middle;
}
.cs-metric {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 10px; padding: 1rem 1.2rem; text-align: left;
}
.cs-metric-label {
    font-size: 0.72rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.06em;
    color: #9E9E9E; margin-bottom: 0.3rem;
}
.cs-metric-valor { font-size: 1.5rem; font-weight: 800; color: #1A1A1A; line-height: 1.1; }
.cs-metric-valor.pos { color: #2E7D32; }
.cs-metric-valor.neg { color: #C62828; }
.cs-metric-valor.nd  { color: #BDBDBD; font-size: 1.1rem; font-weight: 500; }
.cs-section-title {
    font-size: 0.78rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #9E9E9E; margin: 1.4rem 0 0.6rem 0;
}
.cs-comp-card {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 10px; padding: 0.9rem 1.2rem;
    display: flex; flex-direction: column; gap: 0.2rem;
}
.cs-comp-label { font-size: 0.72rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.06em; }
.cs-comp-valor { font-size: 1.15rem; font-weight: 700; color: #1A1A1A; }
.cs-comp-pct   { font-size: 0.82rem; color: #757575; }
.cs-dust-item {
    display: inline-block;
    background: #FAFAFA; border: 1px solid #E0E0E0;
    border-radius: 6px; padding: 3px 10px;
    font-size: 0.78rem; color: #757575; margin: 2px 3px;
}
.cs-aviso {
    background: #FAFAFA; border-left: 3px solid #BDBDBD;
    padding: 0.6rem 1rem; color: #9E9E9E;
    font-size: 0.76rem; border-radius: 0 6px 6px 0; margin-top: 1.5rem;
}
section[data-testid="stSidebar"] {
    background-color: #FFFFFF; border-right: 1px solid #E0E0E0;
}
thead tr th { background: #F5F5F5 !important; color: #424242 !important; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

SOLANA_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")

# ── Sidebar ────
with st.sidebar:
    st.markdown('<div class="cs-logo">Cream<span>Sol</span>.io</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Navegação**")
    st.page_link("app.py",                   label="🏠  Início")
    st.page_link("pages/1_Beginner.py",      label="🟢  Iniciante")
    st.page_link("pages/2_Intermediario.py",  label="🔵  Intermediário")
    st.page_link("pages/3_Profissional.py",   label="⚫  Profissional")
    st.markdown("---")
    st.caption("v1.0.0 · creamsol.io")

# ── Header ────
st.markdown(
    '<div class="cs-logo">Cream<span>Sol</span>.io'
    '<span class="cs-badge">Gratuito</span></div>',
    unsafe_allow_html=True,
)
st.caption("Saldo, P&L e composição da carteira Solana · Sem registo de dados · Tempo real")
st.markdown("---")

# ── Formulário ────
tab_simples, tab_multi = st.tabs(["📌 Carteira única", "📂 Múltiplas carteiras (até 5)"])

with tab_simples:
    with st.form("form_single"):
        col_w, col_m, col_btn = st.columns([4, 1, 1])
        with col_w:
            carteira = st.text_input(
                "Endereço da carteira Solana",
                placeholder="Ex: Eyd3D8FzFSxaRwfYkGFyMhgFnnNhqW3di1wz4fQZkRn9",
                label_visibility="collapsed",
            )
        with col_m:
            moeda = st.selectbox("Moeda", ["USD", "EUR"], label_visibility="collapsed")
        with col_btn:
            submitted_single = st.form_submit_button("🔍 Analisar", use_container_width=True)

with tab_multi:
    with st.form("form_multi"):
        carteiras_raw = st.text_area(
            "Uma carteira por linha (máx. 5)",
            placeholder="Eyd3D8FzFSxaRwfYkGFyMhgFnnNhqW3di1wz4fQZkRn9\nHDixbrzwwLXczhDBk1JVrurPQsuLE8FUKnW2pucSXN3o",
            height=120,
            label_visibility="collapsed",
        )
        col_mm, col_mb = st.columns([1, 3])
        with col_mm:
            moeda_multi = st.selectbox("Moeda ", ["USD", "EUR"], label_visibility="collapsed")
        submitted_multi = st.form_submit_button("🔍 Analisar Consolidado", use_container_width=True)


# ── Helpers ────
def _cor_classe(valor_str: str, neutral: bool = False) -> str:
    if neutral:
        return ""
    if not valor_str or valor_str.strip() in ("N/D", "", "—"):
        return "nd"
    try:
        v = float(
            valor_str
            .replace("$","").replace("€","").replace("%","").replace(",","").strip()
        )
        return "pos" if v > 0 else ("neg" if v < 0 else "")
    except Exception:
        return "nd"


def _metrica(label: str, valor: str, neutral: bool = False):
    cor = _cor_classe(valor, neutral=neutral)
    st.markdown(f"""
    <div class="cs-metric">
        <div class="cs-metric-label">{label}</div>
        <div class="cs-metric-valor {cor}">{valor}</div>
    </div>""", unsafe_allow_html=True)


def _renderizar_dashboard(d: dict):
    # ── Visão Geral ────
    st.markdown('<div class="cs-section-title">Visão Geral</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5, gap="small")
    with c1: _metrica("Patrimônio Total", d["patrimonio_total"])
    with c2: _metrica("P&L Total",        d["pnl_total"])
    with c3: _metrica("ROI Total",        d["roi_total"])
    with c4: _metrica("Tokens",           str(d["n_tokens"]), neutral=True)
    with c5: _metrica("NFTs",             str(d["n_nfts"]), neutral=True)

    # ── Histórico de tokens ────
    n30  = d.get("n_tokens_30d", "—")
    n90  = d.get("n_tokens_90d", "—")
    delt = d.get("delta_tokens", "—")
    pat30 = d.get("patrimonio_30d", "N/D")
    dval  = d.get("delta_valor", "—")

    st.markdown('<div class="cs-section-title">Evolução (30 dias)</div>', unsafe_allow_html=True)
    e1, e2, e3, e4, e5 = st.columns(5, gap="small")
    with e1: _metrica("Patrimônio 30d",   pat30, neutral=True)
    with e2: _metrica("Δ Valor 30d",      dval)
    with e3: _metrica("Tokens hoje",      str(d["n_tokens"]), neutral=True)
    with e4: _metrica("Tokens há 30d",    str(n30), neutral=True)
    with e5: _metrica("Δ Tokens 30d",     str(delt), neutral=True)

    # ── Actividade 90 dias ────
    st.markdown('<div class="cs-section-title">Actividade (90 dias)</div>', unsafe_allow_html=True)
    a1, a2, a3, a4 = st.columns(4, gap="small")
    with a1:
        taxa_sol = d.get("total_taxas_sol", 0.0)
        _metrica("Taxas (SOL)", f"{taxa_sol:.6f} SOL" if isinstance(taxa_sol, float) else str(taxa_sol), neutral=True)
    with a2:
        _metrica("Taxas (USD)",      d.get("total_taxas_usd", "N/D"), neutral=True)
    with a3:
        _metrica("Slippage Est.",    d.get("total_slippage_usd", "N/D"), neutral=True)
    with a4:
        _metrica("Vol. Movimentado", d.get("total_movimentado_usd", "N/D"), neutral=True)

    # ── Composição ────
    st.markdown('<div class="cs-section-title">Composição</div>', unsafe_allow_html=True)
    comp = d["composicao"]
    cc1, cc2 = st.columns(2, gap="small")
    with cc1:
        st.markdown(f"""
        <div class="cs-comp-card">
            <div class="cs-comp-label">Stablecoins</div>
            <div class="cs-comp-valor">{comp['stablecoins']}</div>
            <div class="cs-comp-pct">{comp['stablecoins_pct']} do portfólio</div>
        </div>""", unsafe_allow_html=True)
    with cc2:
        st.markdown(f"""
        <div class="cs-comp-card">
            <div class="cs-comp-label">Criptomoedas</div>
            <div class="cs-comp-valor">{comp['criptomoedas']}</div>
            <div class="cs-comp-pct">{comp['criptomoedas_pct']} do portfólio</div>
        </div>""", unsafe_allow_html=True)

    # ── Tokens ────
    st.markdown('<div class="cs-section-title">Tokens</div>', unsafe_allow_html=True)
    tokens = d.get("tokens", [])
    if tokens:
        rows = []
        for t in tokens:
            rows.append({
                "Símbolo":     t["simbolo"],
                "Verificado":  "✅" if t["verificado"] else "⚠️",
                "Quantidade":  t["quantidade"],
                "Preço":       t["preco_atual"],
                "Valor":       t["valor"],
                "Custo Médio": t["custo_medio"],
                "P&L":         t["pnl"],
                "ROI":         t["roi"],
            })
        df = pd.DataFrame(rows)

        def _estilo_col(val):
            if str(val) in ("N/D", ""):
                return "color: #BDBDBD"
            try:
                v = float(str(val).replace("$","").replace("€","").replace("%","").replace(",","").strip())
                if v > 0: return "color: #2E7D32; font-weight: 700"
                if v < 0: return "color: #C62828; font-weight: 700"
            except Exception:
                pass
            return ""

        styled = df.style.map(_estilo_col, subset=["P&L", "ROI"]).set_properties(**{"font-size": "0.85rem"})
        st.dataframe(styled, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum token significativo encontrado.")

    # ── Dust ────
    dust = d.get("tokens_dust", [])
    if dust:
        st.markdown('<div class="cs-section-title">Tokens Dust</div>', unsafe_allow_html=True)
        dust_html = "".join(
            f'<span class="cs-dust-item">{t["simbolo"]} · {t["quantidade"]}</span>'
            for t in dust
        )
        st.markdown(dust_html, unsafe_allow_html=True)

    # ── Aviso ────
    st.markdown(f"""
    <div class="cs-aviso">
        🔒 {d.get("aviso_legal", "Dados apenas informativos. Nenhum dado é armazenado.")}
    </div>""", unsafe_allow_html=True)


# ── Lógica: carteira única ────
if submitted_single:
    if not carteira or not carteira.strip():
        st.warning("Introduza um endereço de carteira.")
    elif not SOLANA_RE.match(carteira.strip()):
        st.error("Endereço inválido. Verifique e tente novamente.")
    else:
        with st.spinner("A consultar a blockchain..."):
            try:
                url  = f"{API_BASE_URL}/v1/iniciante/{carteira.strip()}?moeda={moeda}"
                resp = requests.get(url, timeout=40)
                resp.raise_for_status()
                _renderizar_dashboard(resp.json())
            except requests.exceptions.HTTPError as e:
                try: detalhe = e.response.json().get("detail", e.response.text)
                except Exception: detalhe = e.response.text
                st.error(f"Erro da API ({e.response.status_code}): {detalhe}")
            except requests.exceptions.Timeout:
                st.error("A API demorou demasiado. Tente novamente.")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")

# ── Lógica: múltiplas carteiras ────
if submitted_multi:
    linhas    = [l.strip() for l in carteiras_raw.strip().splitlines() if l.strip()]
    invalidas = [l for l in linhas if not SOLANA_RE.match(l)]
    if not linhas:
        st.warning("Introduza pelo menos um endereço.")
    elif invalidas:
        st.error(f"Endereços inválidos: {', '.join(invalidas[:3])}")
    elif len(linhas) > 5:
        st.error("Máximo de 5 carteiras por pedido.")
    else:
        with st.spinner(f"A consolidar {len(linhas)} carteira(s)..."):
            try:
                payload = {"carteiras": linhas, "moeda": moeda_multi}
                url     = f"{API_BASE_URL}/v1/iniciante/multi"
                resp    = requests.post(url, json=payload, timeout=60)
                resp.raise_for_status()
                st.success(f"Consolidado de {len(linhas)} carteira(s)")
                _renderizar_dashboard(resp.json())
            except requests.exceptions.HTTPError as e:
                try: detalhe = e.response.json().get("detail", e.response.text)
                except Exception: detalhe = e.response.text
                st.error(f"Erro da API ({e.response.status_code}): {detalhe}")
            except requests.exceptions.Timeout:
                st.error("Timeout — a blockchain demorou demasiado. Tente novamente.")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")
