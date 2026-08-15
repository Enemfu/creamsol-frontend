# ====
# pages/2_Intermediario.py — CreamSol.io · Plano Intermediário (Privado)
# ====

import streamlit as st
import requests
import pandas as pd
import re
from config import API_BASE_URL, SENHA_INTERMEDIARIO

st.set_page_config(
    page_title="Intermediário · CreamSol.io",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.estilo import aplicar_css
aplicar_css()

st.markdown("""
<style>
.stApp { background-color: #F5F5F5; }
.block-container { padding-top: 1.8rem; padding-bottom: 2rem; max-width: 1100px; }

.cs-logo { font-size: 1.5rem; font-weight: 900; letter-spacing: -0.02em; color: #1A1A1A; }
.cs-logo span { color: #14F195; }   /* verde Solana */

.cs-badge {
    display: inline-block;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    background: #E3F2FD; color: #1565C0;
    border-radius: 4px; padding: 2px 10px;
    margin-left: 0.6rem; vertical-align: middle;
}
.cs-metric {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 10px; padding: 1rem 1.2rem;
}
.cs-metric-label {
    font-size: 0.72rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.06em;
    color: #9E9E9E; margin-bottom: 0.3rem;
}
.cs-metric-valor { font-size: 1.45rem; font-weight: 800; color: #1A1A1A; line-height: 1.1; }
.cs-metric-valor.pos { color: #2E7D32; }
.cs-metric-valor.neg { color: #C62828; }
.cs-metric-valor.nd  { color: #BDBDBD; font-size: 1.05rem; font-weight: 500; }
.cs-section-title {
    font-size: 0.78rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #9E9E9E; margin: 1.4rem 0 0.6rem 0;
}
.cs-defi-nota {
    background: #FAFAFA; border: 1px dashed #BDBDBD;
    border-radius: 10px; padding: 1.2rem 1.5rem;
    color: #9E9E9E; font-size: 0.85rem; text-align: center;
}
.cs-login-box {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 12px; padding: 2rem;
    max-width: 420px; margin: 3rem auto; text-align: center;
}
.cs-aviso {
    background: #FAFAFA; border-left: 3px solid #BDBDBD;
    padding: 0.6rem 1rem; color: #9E9E9E;
    font-size: 0.76rem; border-radius: 0 6px 6px 0; margin-top: 1.5rem;
}
section[data-testid="stSidebar"] {
    background-color: #FFFFFF; border-right: 1px solid #E0E0E0;
}
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
    '<span class="cs-badge">Intermediário</span></div>',
    unsafe_allow_html=True,
)
st.caption("Performance detalhada · Estatísticas avançadas · Export CSV/JSON")
st.markdown("---")


# ════ AUTENTICAÇÃO ════
if "auth_intermediario" not in st.session_state:
    st.session_state["auth_intermediario"] = False

if not st.session_state["auth_intermediario"]:
    st.markdown("""
    <div class="cs-login-box">
        <div style="font-size:2rem; margin-bottom:0.5rem">🔒</div>
        <div style="font-size:1.1rem; font-weight:700; color:#1A1A1A; margin-bottom:0.3rem">
            Acesso Privado
        </div>
        <div style="font-size:0.85rem; color:#757575; margin-bottom:1.2rem">
            Introduza a senha para aceder ao plano Intermediário.
        </div>
    </div>
    """, unsafe_allow_html=True)
    col_c, col_f, col_d = st.columns([1, 2, 1])
    with col_f:
        with st.form("form_login"):
            senha_input = st.text_input("Senha", type="password", placeholder="••••", label_visibility="collapsed")
            btn_login   = st.form_submit_button("Entrar", use_container_width=True)
        if btn_login:
            if senha_input == SENHA_INTERMEDIARIO:
                st.session_state["auth_intermediario"] = True
                st.rerun()
            else:
                st.error("Senha incorrecta.")
    st.stop()


# ════ ÁREA AUTENTICADA ════
with st.form("form_carteira"):
    col_w, col_m, col_btn = st.columns([4, 1, 1])
    with col_w:
        carteira = st.text_input(
            "Endereço da carteira Solana",
            placeholder="Ex: Eyd3D8FzFSxaRwfYkGFyMhgFnnNhqW3di1wz4fQZkRn9",
            label_visibility="collapsed",
        )
    with col_m:
        moeda = st.selectbox("Moeda", ["USD", "EUR", "GBP"], label_visibility="collapsed")
    with col_btn:
        submitted = st.form_submit_button("🔍 Analisar", use_container_width=True)

col_sair, _ = st.columns([1, 5])
with col_sair:
    if st.button("🔓 Sair", use_container_width=True):
        st.session_state["auth_intermediario"] = False
        st.rerun()


# ── Helpers ────
def _cor(valor_str: str, neutral: bool = False) -> str:
    if neutral:
        return ""
    if not valor_str or str(valor_str).strip() in ("N/D", "", "—"):
        return "nd"
    try:
        v = float(
            str(valor_str)
            .replace("$","").replace("€","").replace("£","")
            .replace("%","").replace(",","").replace("<","").strip()
        )
        return "pos" if v > 0 else ("neg" if v < 0 else "")
    except Exception:
        return "nd"


def _metrica(label: str, valor: str, neutral: bool = False):
    cor = _cor(valor, neutral=neutral)
    st.markdown(f"""
    <div class="cs-metric">
        <div class="cs-metric-label">{label}</div>
        <div class="cs-metric-valor {cor}">{valor}</div>
    </div>""", unsafe_allow_html=True)


def _estilo_pnl(val):
    s = str(val)
    if s in ("N/D", "—", ""):
        return "color: #BDBDBD"
    try:
        v = float(s.replace("$","").replace("€","").replace("£","").replace("%","").replace(",","").replace("<","").strip())
        if v > 0: return "color: #2E7D32; font-weight:700"
        if v < 0: return "color: #C62828; font-weight:700"
    except Exception:
        pass
    return ""


def _chamar_api(endpoint: str, carteira: str, moeda: str) -> dict | None:
    try:
        url  = f"{API_BASE_URL}/v1/intermediario/{endpoint}/{carteira}"
        resp = requests.get(url, params={"moeda": moeda}, timeout=45)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        try: detalhe = e.response.json().get("detail", e.response.text)
        except Exception: detalhe = e.response.text
        st.error(f"Erro API ({e.response.status_code}): {detalhe}")
    except requests.exceptions.Timeout:
        st.error("Timeout — a blockchain demorou demasiado. Tente novamente.")
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
    return None


# ── Renderização ────
if submitted:
    if not carteira or not carteira.strip():
        st.warning("Introduza um endereço de carteira.")
        st.stop()
    if not SOLANA_RE.match(carteira.strip()):
        st.error("Endereço inválido. Verifique e tente novamente.")
        st.stop()

    carteira = carteira.strip()

    with st.spinner("A consultar a blockchain..."):
        snap  = _chamar_api("snapshot",     carteira, moeda)
        perf  = _chamar_api("performance",  carteira, moeda)
        stats = _chamar_api("estatisticas", carteira, moeda)
        defi  = _chamar_api("defi",         carteira, moeda)

    if not snap:
        st.stop()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Visão Geral", "📈 Performance", "📉 Estatísticas", "⚡ DeFi", "💾 Exportar",
    ])

    # ══ Tab 1 — Visão Geral ════
    with tab1:
        st.markdown('<div class="cs-section-title">Snapshot</div>', unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns(5, gap="small")
        with c1: _metrica("Patrimônio",  snap.get("patrimonio_total_usd", "N/D"))
        with c2: _metrica("Saldo SOL",   snap.get("saldo_sol_usd", "N/D"),     neutral=True)
        with c3: _metrica("Tokens",      str(snap.get("n_tokens", "—")),        neutral=True)
        with c4: _metrica("NFTs",        str(snap.get("n_nfts", "—")),          neutral=True)
        with c5: _metrica("Taxas Pagas", snap.get("total_taxas_usd", "N/D"),    neutral=True)  # fees → neutro

        st.markdown('<div class="cs-section-title">Evolução (30 dias)</div>', unsafe_allow_html=True)
        e1, e2, e3, e4, e5 = st.columns(5, gap="small")
        with e1: _metrica("Patrimônio 30d", snap.get("patrimonio_30d_usd", "N/D"), neutral=True)
        with e2: _metrica("Δ Valor 30d",    snap.get("delta_valor", "—"))
        with e3: _metrica("Tokens hoje",    str(snap.get("n_tokens", "—")),         neutral=True)
        with e4: _metrica("Tokens há 30d",  str(snap.get("n_tokens_30d", "—")),     neutral=True)
        with e5: _metrica("Δ Tokens",       str(snap.get("delta_tokens", "—")),     neutral=True)

        st.markdown('<div class="cs-section-title">Detalhe</div>', unsafe_allow_html=True)
        d1, d2, d3 = st.columns(3, gap="small")
        with d1: _metrica("SOL (quantidade)", f"{snap.get('saldo_sol', 0):.6f}", neutral=True)
        with d2: _metrica("Taxas (SOL)",      f"{snap.get('total_taxas_sol', 0):.6f} SOL", neutral=True)
        with d3:
            slip = snap.get("total_slippage_usd", "—")
            _metrica("Slippage Est.", slip if slip != "—" else "N/D", neutral=True)  # slippage → neutro

        st.markdown(f"""
        <div class="cs-aviso">
            🕒 <strong>{snap.get("timestamp","—")}</strong> &nbsp;·&nbsp;
            Carteira: <code style="font-size:0.75rem">{carteira}</code>
        </div>""", unsafe_allow_html=True)

    # ══ Tab 2 — Performance ════
    with tab2:
        if perf and perf.get("tokens"):
            st.markdown('<div class="cs-section-title">Performance por Token</div>', unsafe_allow_html=True)
            rows = [
                {
                    "Símbolo":       t.get("simbolo",                "—"),
                    "Verif.":        "✅" if t.get("verificado") else "⚠️",
                    "Quantidade":    t.get("quantidade_atual",        "—"),
                    "Preço":         t.get("preco_atual_usd",         "—"),
                    "Valor":         t.get("valor_atual_usd",         "—"),
                    "Vol. Comprado": t.get("volume_comprado_usd",     "N/D"),
                    "Custo Médio":   t.get("preco_medio_compra_usd",  "N/D"),
                    "P&L Não Real.": t.get("lucro_nao_realizado_usd", "N/D"),
                    "ROI":           t.get("roi_pct",                 "N/D"),
                }
                for t in perf["tokens"]
            ]
            df = pd.DataFrame(rows)
            styled = df.style.map(_estilo_pnl, subset=["P&L Não Real.", "ROI"]).set_properties(**{"font-size": "0.84rem"})
            st.dataframe(styled, use_container_width=True, hide_index=True)
        else:
            st.info("Sem dados de performance disponíveis.")

    # ══ Tab 3 — Estatísticas ════
    with tab3:
        if stats:
            st.markdown('<div class="cs-section-title">Resumo Global</div>', unsafe_allow_html=True)
            s1, s2, s3 = st.columns(3, gap="small")
            with s1: _metrica("Patrimônio Total",  stats.get("patrimonio_total_usd",         "N/D"))
            with s2: _metrica("Volume Comprado",   stats.get("volume_total_comprado_usd",     "N/D"), neutral=True)
            with s3: _metrica("P&L Não Realizado", stats.get("lucro_nao_realizado_total_usd", "N/D"))

            s4, s5, s6 = st.columns(3, gap="small")
            with s4: _metrica("ROI Médio",         stats.get("roi_medio_pct",   "N/D"))
            with s5: _metrica("Taxas Pagas (USD)", stats.get("total_taxas_usd", "N/D"), neutral=True)  # neutro
            with s6:
                slip = stats.get("total_slippage_usd", "—")
                _metrica("Slippage Est. (USD)", slip if slip != "—" else "N/D", neutral=True)  # neutro

            st.markdown('<div class="cs-section-title">Distribuição de Tokens</div>', unsafe_allow_html=True)
            t1, t2, t3 = st.columns(3, gap="small")
            with t1: _metrica("Com Lucro",       str(stats.get("num_tokens_com_lucro",    "—")), neutral=True)
            with t2: _metrica("Com Prejuízo",    str(stats.get("num_tokens_com_prejuizo", "—")), neutral=True)
            with t3: _metrica("Sem Custo (N/D)", str(stats.get("num_tokens_neutros",      "—")), neutral=True)

            if stats.get("aviso"):
                st.markdown(f'<div class="cs-aviso">⚠️ {stats["aviso"]}</div>', unsafe_allow_html=True)
        else:
            st.info("Sem estatísticas disponíveis.")

    # ══ Tab 4 — DeFi ════
    with tab4:
        st.markdown('<div class="cs-section-title">Posições DeFi</div>', unsafe_allow_html=True)
        if defi:
            stk = defi.get("staking_sol", {})
            d1, d2 = st.columns(2, gap="small")
            with d1: _metrica("Staking SOL (quantidade)", str(stk.get("quantidade_sol", "0.0")), neutral=True)
            with d2: _metrica("Staking SOL (USD)",        stk.get("valor_usd", "$0.00"), neutral=True)
            st.markdown(f"""
            <div class="cs-defi-nota">
                ⚡ {defi.get("nota", "Posições DeFi completas disponíveis na versão Profissional.")}
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Sem dados DeFi disponíveis.")

    # ══ Tab 5 — Exportar ════
    with tab5:
        st.markdown('<div class="cs-section-title">Exportar Dados</div>', unsafe_allow_html=True)

        for _k in ("int_export_json", "int_export_csv"):
            if _k not in st.session_state:
                st.session_state[_k] = None

        col_j, col_c, _ = st.columns([1, 1, 2], gap="small")

        with col_j:
            if st.button("⬇️ Gerar JSON", use_container_width=True, key="int_btn_json"):
                try:
                    url = f"{API_BASE_URL}/v1/intermediario/export/{carteira}"
                    r = requests.get(url, params={"formato": "json", "moeda": moeda}, timeout=45)
                    r.raise_for_status()
                    st.session_state["int_export_json"] = r.text
                except Exception as e:
                    st.error(f"Erro ao gerar JSON: {e}")

            if st.session_state.get("int_export_json"):
                st.download_button(
                    label="💾 Guardar JSON",
                    data=st.session_state["int_export_json"],
                    file_name=f"creamsol_int_{carteira[:8]}.json",
                    mime="application/json",
                    use_container_width=True,
                    key="int_dl_json",
                )

        with col_c:
            if st.button("⬇️ Gerar CSV", use_container_width=True, key="int_btn_csv"):
                try:
                    url = f"{API_BASE_URL}/v1/intermediario/export/{carteira}"
                    r = requests.get(url, params={"formato": "csv", "moeda": moeda}, timeout=45)
                    r.raise_for_status()
                    st.session_state["int_export_csv"] = r.content
                except Exception as e:
                    st.error(f"Erro ao gerar CSV: {e}")

            if st.session_state.get("int_export_csv"):
                st.download_button(
                    label="💾 Guardar CSV",
                    data=st.session_state["int_export_csv"],
                    file_name=f"creamsol_int_{carteira[:8]}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="int_dl_csv",
                )

        st.markdown("""
        <div class="cs-aviso">
            🔒 Os ficheiros exportados não contêm dados identificativos além do endereço público da carteira.
            Nenhum dado é retido no servidor após a resposta.
        </div>""", unsafe_allow_html=True)
