# ====
# pages/1_Iniciante.py — CreamSol.io · Beginner Plan (Free)
# ====

import streamlit as st
import requests
import pandas as pd
import re
from config import API_BASE_URL

# ── Page config ────
st.set_page_config(
    page_title="Beginner · CreamSol.io",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────
st.markdown("""
<style>
.stApp { background-color: #F5F5F5; }
.block-container { padding-top: 1.8rem; padding-bottom: 2rem; max-width: 1100px; }

.cs-logo { font-size: 1.5rem; font-weight: 900; letter-spacing: -0.02em; color: #1A1A1A; }
.cs-logo span { color: #2E7D32; }

.cs-badge {
    display: inline-block;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    background: #E8F5E9; color: #2E7D32;
    border-radius: 4px; padding: 2px 10px;
    margin-left: 0.6rem; vertical-align: middle;
}

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

# ── Solana address regex ────
SOLANA_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")

# ── Sidebar ────
with st.sidebar:
    st.markdown('<div class="cs-logo">Cream<span>Sol</span>.io</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Navigation**")
    st.page_link("app.py",                   label="🏠  Home")
    st.page_link("pages/1_Iniciante.py",      label="🟢  Beginner")
    st.page_link("pages/2_Intermediario.py",  label="🔵  Intermediate")
    st.page_link("pages/3_Profissional.py",   label="⚫  Professional")
    st.markdown("---")
    st.caption("v1.0.0 · creamsol.io")

# ── Header ────
st.markdown(
    '<div class="cs-logo">Cream<span>Sol</span>.io'
    '<span class="cs-badge">Free</span></div>',
    unsafe_allow_html=True,
)
st.caption("Balance, P&L and Solana wallet composition · No data stored · Real-time")
st.markdown("---")

# ── Warning: public address only ────
st.warning("⚠️ Use only your **public wallet address**. Never share your private key.")

# ── Tabs ────
tab_simples, tab_multi = st.tabs(["📌 Single wallet", "📂 Multiple wallets (max. 3)"])

# ── Tab: single wallet ────
with tab_simples:
    with st.form("form_single"):
        col_w, col_m, col_btn = st.columns([4, 1, 1])
        with col_w:
            carteira = st.text_input(
                "Solana wallet address",
                placeholder="e.g. Eyd3D8FzFSxaRwfYkGFyMhgFnnNhqW3di1wz4fQZkRn9",
                label_visibility="collapsed",
            )
        with col_m:
            moeda = st.selectbox("Currency", ["USD", "EUR", "GBP"], label_visibility="collapsed")
        with col_btn:
            submitted_single = st.form_submit_button("🔍 Analyse", use_container_width=True)

# ── Tab: multiple wallets ────
with tab_multi:
    with st.form("form_multi"):
        carteiras_raw = st.text_area(
            "One wallet per line (max. 3)",
            placeholder="Eyd3D8FzFSxaRwfYkGFyMhgFnnNhqW3di1wz4fQZkRn9\nHDixbrzwwLXczhDBk1JVrurPQsuLE8FUKnW2pucSXN3o",
            height=120,
            label_visibility="collapsed",
        )
        col_mm, col_mb = st.columns([1, 3])
        with col_mm:
            moeda_multi = st.selectbox("Currency ", ["USD", "EUR", "GBP"], label_visibility="collapsed")
        submitted_multi = st.form_submit_button("🔍 Analyse Combined", use_container_width=True)


# ── Helper functions ────
def _cor_classe(valor_str: str) -> str:
    if not valor_str or valor_str.strip() in ("N/A", "", "—"):
        return "nd"
    try:
        v = float(
            valor_str
            .replace("$", "").replace("€", "").replace("£", "")
            .replace("%", "").replace(",", "")
            .strip()
        )
        return "pos" if v > 0 else ("neg" if v < 0 else "")
    except Exception:
        return "nd"


def _metrica(label: str, valor: str):
    cor = _cor_classe(valor)
    st.markdown(f"""
    <div class="cs-metric">
        <div class="cs-metric-label">{label}</div>
        <div class="cs-metric-valor {cor}">{valor}</div>
    </div>""", unsafe_allow_html=True)


def _renderizar_dashboard(d: dict):
    # ── Overview metrics ────
    st.markdown('<div class="cs-section-title">Overview</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5, gap="small")
    with c1: _metrica("Total Portfolio", d["patrimonio_total"])
    with c2: _metrica("Total P&L", d["pnl_total"])
    with c3: _metrica("Total ROI", d["roi_total"])
    with c4: _metrica("Tokens", str(d["n_tokens"]))
    with c5: _metrica("NFTs", str(d["n_nfts"]))

    # ── Composition ────
    st.markdown('<div class="cs-section-title">Composition</div>', unsafe_allow_html=True)
    comp = d["composicao"]
    cc1, cc2 = st.columns(2, gap="small")
    with cc1:
        st.markdown(f"""
        <div class="cs-comp-card">
            <div class="cs-comp-label">Stablecoins</div>
            <div class="cs-comp-valor">{comp['stablecoins']}</div>
            <div class="cs-comp-pct">{comp['stablecoins_pct']} of portfolio</div>
        </div>""", unsafe_allow_html=True)
    with cc2:
        st.markdown(f"""
        <div class="cs-comp-card">
            <div class="cs-comp-label">Cryptocurrencies</div>
            <div class="cs-comp-valor">{comp['criptomoedas']}</div>
            <div class="cs-comp-pct">{comp['criptomoedas_pct']} of portfolio</div>
        </div>""", unsafe_allow_html=True)

    # ── Tokens table ────
    st.markdown('<div class="cs-section-title">Tokens</div>', unsafe_allow_html=True)
    tokens = d.get("tokens", [])
    if tokens:
        rows = []
        for t in tokens:
            rows.append({
                "Symbol":       t["simbolo"],
                "Verified":     "✅" if t["verificado"] else "⚠️",
                "Amount":       t["quantidade"],
                "Price":        t["preco_atual"],
                "Value":        t["valor"],
                "Avg. Cost":    t["custo_medio"],
                "P&L":          t["pnl"],
                "ROI":          t["roi"],
            })

        df = pd.DataFrame(rows)

        def _estilo_col(val):
            if str(val) in ("N/A", ""):
                return "color: #BDBDBD"
            try:
                v = float(
                    str(val)
                    .replace("$","").replace("€","").replace("£","")
                    .replace("%","").replace(",","")
                    .strip()
                )
                if v > 0: return "color: #2E7D32; font-weight: 700"
                if v < 0: return "color: #C62828; font-weight: 700"
            except Exception:
                pass
            return ""

        styled = (
            df.style
            .map(_estilo_col, subset=["P&L", "ROI"])
            .set_properties(**{"font-size": "0.85rem"})
        )
        st.dataframe(styled, use_container_width=True, hide_index=True)
    else:
        st.info("No significant tokens found.")

    # ── Dust tokens ────
    dust = d.get("tokens_dust", [])
    if dust:
        st.markdown('<div class="cs-section-title">Dust Tokens</div>', unsafe_allow_html=True)
        dust_html = "".join(
            f'<span class="cs-dust-item">{t["simbolo"]} · {t["quantidade"]}</span>'
            for t in dust
        )
        st.markdown(dust_html, unsafe_allow_html=True)

    # ── Legal notice ────
    st.markdown(f"""
    <div class="cs-aviso">
        🔒 <strong>Privacy:</strong> For informational purposes only. No wallet address or personal data is stored, logged or shared. CreamSol.io does not constitute financial or tax advice.
    </div>""", unsafe_allow_html=True)


# ── Logic: single wallet ────
if submitted_single:
    if not carteira or not carteira.strip():
        st.warning("Please enter a wallet address.")
    elif not SOLANA_RE.match(carteira.strip()):
        st.error("Invalid address. Please check and try again.")
    else:
        with st.spinner("Querying the blockchain..."):
            try:
                url = f"{API_BASE_URL}/v1/iniciante/{carteira.strip()}?moeda={moeda}"
                resp = requests.get(url, timeout=40)
                resp.raise_for_status()
                _renderizar_dashboard(resp.json())
            except requests.exceptions.HTTPError as e:
                detalhe = ""
                try:
                    detalhe = e.response.json().get("detail", e.response.text)
                except Exception:
                    detalhe = e.response.text
                st.error(f"API error ({e.response.status_code}): {detalhe}")
            except requests.exceptions.Timeout:
                st.error("The API took too long. Please try again.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# ── Logic: multiple wallets ────
if submitted_multi:
    linhas = [l.strip() for l in carteiras_raw.strip().splitlines() if l.strip()]
    invalidas = [l for l in linhas if not SOLANA_RE.match(l)]
    if not linhas:
        st.warning("Please enter at least one address.")
    elif invalidas:
        st.error(f"Invalid addresses: {', '.join(invalidas[:3])}")
    elif len(linhas) > 3:
        st.error("Maximum of 3 wallets per request.")
    else:
        with st.spinner(f"Consolidating {len(linhas)} wallet(s)..."):
            try:
                payload = {"carteiras": linhas, "moeda": moeda_multi}
                url = f"{API_BASE_URL}/v1/iniciante/multi"
                resp = requests.post(url, json=payload, timeout=60)
                resp.raise_for_status()
                st.success(f"Combined data from {len(linhas)} wallet(s)")
                _renderizar_dashboard(resp.json())
            except requests.exceptions.HTTPError as e:
                detalhe = ""
                try:
                    detalhe = e.response.json().get("detail", e.response.text)
                except Exception:
                    detalhe = e.response.text
                st.error(f"API error ({e.response.status_code}): {detalhe}")
            except requests.exceptions.Timeout:
                st.error("Timeout — the blockchain took too long. Please try again.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")