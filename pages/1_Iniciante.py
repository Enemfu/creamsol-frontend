# ====
# pages/1_Iniciante.py — CreamSol.io · Beginner Plan
# ====

import streamlit as st
import requests
import pandas as pd
import re
from config import API_BASE_URL

st.set_page_config(
    page_title="Beginner · CreamSol.io",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp { background-color: #F5F5F5; }
.block-container { padding-top: 1.8rem; padding-bottom: 2rem; max-width: 1100px; }

.cs-logo { font-size: 1.5rem; font-weight: 900; letter-spacing: -0.02em; color: #1A1A1A; }
.cs-logo span { color: #2E7D32; }

.cs-badge {
    display: inline-block; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    background: #E8F5E9; color: #2E7D32;
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

/* Composition — side by side */
.cs-comp-row {
    display: flex; gap: 1rem; margin-top: 0.4rem;
}
.cs-comp-card {
    flex: 1; background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 10px; padding: 0.9rem 1.1rem;
}
.cs-comp-card-label {
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.06em; color: #9E9E9E; margin-bottom: 0.5rem;
}
.cs-comp-card-pct {
    font-size: 1.3rem; font-weight: 800; margin-bottom: 0.4rem;
}
.cs-comp-card-val { font-size: 0.82rem; color: #757575; }
.cs-comp-track {
    height: 6px; background: #EEEEEE;
    border-radius: 4px; overflow: hidden; margin-top: 0.6rem;
}
.cs-comp-fill-stable { height: 100%; border-radius: 4px; background: #1565C0; }
.cs-comp-fill-crypto  { height: 100%; border-radius: 4px; background: #2E7D32; }

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
    '<span class="cs-badge">Beginner</span></div>',
    unsafe_allow_html=True,
)
st.caption("Portfolio snapshot · Token performance · Basic metrics")
st.markdown("---")


# ── Helpers ────
def _cor(valor_str: str) -> str:
    if not valor_str or str(valor_str).strip() in ("N/A", "N/D", "", "—"):
        return "nd"
    try:
        v = float(
            str(valor_str)
            .replace("$","").replace("€","").replace("£","")
            .replace("%","").replace(",","").replace("<","").replace("+","").strip()
        )
        return "pos" if v > 0 else ("neg" if v < 0 else "")
    except Exception:
        return "nd"


def _metrica(label: str, valor: str, forcar_neg: bool = False):
    cor = "neg" if forcar_neg else _cor(valor)
    st.markdown(f"""
    <div class="cs-metric">
        <div class="cs-metric-label">{label}</div>
        <div class="cs-metric-valor {cor}">{valor}</div>
    </div>""", unsafe_allow_html=True)


def _pct_float(pct_str: str) -> float:
    try:
        return float(str(pct_str).replace("%","").replace("+","").replace(",",".").strip())
    except Exception:
        return 0.0


def _chamar_api(carteira: str, moeda: str) -> dict | None:
    try:
        url = f"{API_BASE_URL}/v1/iniciante/{carteira}?moeda={moeda}"
        resp = requests.get(url, timeout=45)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        try:
            detalhe = e.response.json().get("detail", e.response.text)
        except Exception:
            detalhe = e.response.text
        st.error(f"API Error ({e.response.status_code}): {detalhe}")
    except requests.exceptions.Timeout:
        st.error("Timeout — the blockchain took too long to respond. Please try again.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    return None


def _renderizar_dashboard(d: dict, carteira: str):

    # ── Portfolio Overview ────
    st.markdown('<div class="cs-section-title">Portfolio Overview</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4, gap="small")

    # Extrai SOL balance da lista de tokens
    sol_amount = "—"
    sol_valor  = "—"
    for t in d.get("tokens", []):
        if str(t.get("simbolo","")).upper() in ("SOL", "WSOL"):
            sol_amount = f"{t.get('quantidade', 0):.6f}" if isinstance(t.get('quantidade'), (int, float)) else str(t.get('quantidade','—'))
            sol_valor  = t.get("valor", "—")
            break

    with c1: _metrica("Total Portfolio", d.get("patrimonio_total", "N/A"))
    with c2: _metrica("SOL Balance",     sol_valor)
    with c3: _metrica("Total P&L",       d.get("pnl_total", "N/A"))
    with c4: _metrica("Fees Paid",       d.get("total_taxas_usd", "N/A"), forcar_neg=True)

    # ── 30-Day Comparison ────
    st.markdown('<div class="cs-section-title">30-Day Comparison</div>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3, gap="small")
    with m1: _metrica("Portfolio (30d ago)", d.get("patrimonio_30d", "N/D"))
    with m2: _metrica("Change (30d)",        d.get("delta_valor", "—"))
    with m3: _metrica("Tokens (30d ago)",    str(d.get("n_tokens_30d", "—")))

    # ── Details ────
    st.markdown('<div class="cs-section-title">Details</div>', unsafe_allow_html=True)
    d1, d2, d3, d4 = st.columns(4, gap="small")
    with d1: _metrica("SOL (amount)",  sol_amount)
    with d2: _metrica("Fees (SOL)",    f"{d.get('total_taxas_sol', 0):.6f}", forcar_neg=True)
    with d3: _metrica("Est. Slippage", d.get("total_slippage_usd", "—"),    forcar_neg=True)
    with d4: _metrica("Tokens",        str(d.get("n_tokens", "N/A")))

    # ── Composition — side by side, cores diferentes ────
    comp = d.get("composicao", {})
    if comp:
        st.markdown('<div class="cs-section-title">Composition</div>', unsafe_allow_html=True)
        pct_st = _pct_float(comp.get("stablecoins_pct", "0"))
        pct_cr = _pct_float(comp.get("criptomoedas_pct", "0"))
        bar_st = min(max(pct_st, 0), 100)
        bar_cr = min(max(pct_cr, 0), 100)

        st.markdown(f"""
        <div class="cs-comp-row">
            <div class="cs-comp-card">
                <div class="cs-comp-card-label">Stablecoins</div>
                <div class="cs-comp-card-pct" style="color:#1565C0">{comp.get("stablecoins_pct","—")}</div>
                <div class="cs-comp-card-val">{comp.get("stablecoins","—")}</div>
                <div class="cs-comp-track">
                    <div class="cs-comp-fill-stable" style="width:{bar_st}%"></div>
                </div>
            </div>
            <div class="cs-comp-card">
                <div class="cs-comp-card-label">Crypto</div>
                <div class="cs-comp-card-pct" style="color:#2E7D32">{comp.get("criptomoedas_pct","—")}</div>
                <div class="cs-comp-card-val">{comp.get("criptomoedas","—")}</div>
                <div class="cs-comp-track">
                    <div class="cs-comp-fill-crypto" style="width:{bar_cr}%"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tokens table — Top 3 visível, restante locked ────
    st.markdown('<div class="cs-section-title">Tokens</div>', unsafe_allow_html=True)
    tokens = d.get("tokens", [])
    if tokens:
        rows = []
        for t in tokens:
            rows.append({
                "Symbol":    t.get("simbolo", "?"),
                "Verified":  "✅" if t.get("verificado") else "⚠️",
                "Amount":    t.get("quantidade", "N/A"),
                "Price":     t.get("preco_atual", "N/A"),
                "Value":     t.get("valor", "N/A"),
                "Avg. Cost": t.get("custo_medio", "N/A"),
                "P&L":       t.get("pnl", "N/A"),
                "ROI":       t.get("roi", "N/A"),
            })

        df = pd.DataFrame(rows)

        def _estilo_col(val):
            try:
                v = float(
                    str(val)
                    .replace("$","").replace("€","").replace("£","")
                    .replace("%","").replace(",","").replace("+","").strip()
                )
                if v > 0: return "color: #2E7D32; font-weight: 700"
                if v < 0: return "color: #C62828; font-weight: 700"
            except Exception:
                pass
            return ""

        # Top 3 sempre visível
        styled_top = (
            df.head(3).style
            .map(_estilo_col, subset=["P&L", "ROI"])
            .set_properties(**{"font-size": "0.85rem"})
        )
        st.dataframe(styled_top, use_container_width=True, hide_index=True)

        # Restante — locked, sem dados
        if len(df) > 3:
            with st.expander(f"🔒 {len(df) - 3} more tokens — Intermediate plan"):
                st.markdown("""
                <div style="text-align:center; padding:1.5rem 0;">
                    <div style="font-size:1.5rem; margin-bottom:0.5rem">🔒</div>
                    <div style="font-weight:700; color:#1A1A1A; margin-bottom:0.4rem">
                        Intermediate Plan required
                    </div>
                    <div style="font-size:0.85rem; color:#757575;">
                        Upgrade to view your full token list, detailed P&L,
                        ROI per token and CSV export.
                    </div>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("No significant tokens found in this wallet.")

    # ── Dust tokens ────
    dust = d.get("tokens_dust", [])
    if dust:
        with st.expander(f"🪣 Dust tokens ({len(dust)})"):
            dust_rows = [{"Symbol": t.get("simbolo","?"), "Amount": t.get("quantidade","—")} for t in dust]
            st.dataframe(pd.DataFrame(dust_rows), use_container_width=True, hide_index=True)

    # ── Footer ────
    st.markdown(f"""
    <div class="cs-aviso">
        🔒 <strong>Privacy:</strong> For informational purposes only. No wallet address or personal data
        is stored, logged or shared. CreamSol.io does not constitute financial or tax advice. &nbsp;·&nbsp;
        🕒 Wallet: <code style="font-size:0.74rem">{carteira}</code>
    </div>""", unsafe_allow_html=True)


# ── Wallet form ────
with st.form("form_carteira"):
    col_w, col_m, col_btn = st.columns([4, 1, 1])
    with col_w:
        carteira = st.text_input(
            "Solana wallet address",
            placeholder="Ex: Eyd3D8FzFSxaRwfYkGFyMhgFnnNhqW3di1wz4fQZkRn9",
            label_visibility="collapsed",
        )
    with col_m:
        moeda = st.selectbox("Currency", ["USD", "EUR", "GBP"], label_visibility="collapsed")
    with col_btn:
        submitted = st.form_submit_button("🔍 Analyse", use_container_width=True)

if submitted:
    if not carteira or not carteira.strip():
        st.warning("Please enter a Solana wallet address.")
        st.stop()
    if not SOLANA_RE.match(carteira.strip()):
        st.error("Invalid address. Please check and try again.")
        st.stop()

    carteira = carteira.strip()

    with st.spinner("Querying the blockchain, please wait…"):
        dados = _chamar_api(carteira, moeda)

    if dados:
        _renderizar_dashboard(dados, carteira)