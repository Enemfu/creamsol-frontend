# ====
# pages/2_Intermediario.py — CreamSol.io · Intermediate Plan
# ====

import streamlit as st
import requests
import pandas as pd
import re
from config import API_BASE_URL, SENHA_INTERMEDIARIO

st.set_page_config(
    page_title="Intermediate · CreamSol.io",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp { background-color: #F5F5F5; }
.block-container { padding-top: 3rem; padding-bottom: 2rem; max-width: 1100px; }

.cs-logo { font-size: 1.5rem; font-weight: 900; letter-spacing: -0.02em; color: #1A1A1A; }
.cs-logo span { color: #2E7D32; }

.cs-badge {
    display: inline-block; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    background: #E3F2FD; color: #1565C0;
    border-radius: 4px; padding: 2px 10px;
    margin-left: 0.6rem; vertical-align: middle;
}

/* ── Metric card ── */
.cs-metric {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 10px; padding: 1rem 1.2rem;
    height: 100%;
}
.cs-metric-label {
    font-size: 0.72rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.06em;
    color: #9E9E9E; margin-bottom: 0.3rem;
}
.cs-metric-valor {
    font-size: 1.45rem; font-weight: 800;
    color: #1A1A1A; line-height: 1.1;
}
.cs-metric-valor.pos { color: #2E7D32; }
.cs-metric-valor.neg { color: #C62828; }
.cs-metric-valor.nd  { color: #BDBDBD; font-size: 1.05rem; font-weight: 500; }
.cs-metric-sub {
    font-size: 0.78rem; color: #9E9E9E;
    margin-top: 0.25rem; font-weight: 500;
}

/* ── Tooltip ── */
.cs-tooltip-wrap {
    position: relative; display: inline-block;
    margin-left: 5px; cursor: help;
}
.cs-tooltip-icon {
    display: inline-flex; align-items: center; justify-content: center;
    width: 14px; height: 14px; border-radius: 50%;
    background: #E0E0E0; color: #757575;
    font-size: 0.6rem; font-weight: 800; line-height: 1;
    vertical-align: middle;
}
.cs-tooltip-box {
    visibility: hidden; opacity: 0;
    background: #1A1A1A; color: #FFFFFF;
    font-size: 0.72rem; line-height: 1.4;
    border-radius: 6px; padding: 6px 10px;
    width: 200px;
    position: absolute; z-index: 999;
    bottom: 125%; left: 50%; transform: translateX(-50%);
    transition: opacity 0.15s ease;
    pointer-events: none;
}
.cs-tooltip-wrap:hover .cs-tooltip-box { visibility: visible; opacity: 1; }

/* ── Section title ── */
.cs-section-title {
    font-size: 0.78rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #9E9E9E; margin: 1.6rem 0 0.6rem 0;
}

/* ── Composition cards ── */
.cs-comp-row { display: flex; gap: 1rem; margin-top: 0.4rem; }
.cs-comp-card {
    flex: 1; background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 10px; padding: 0.9rem 1.1rem;
}
.cs-comp-card-label {
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.06em; color: #9E9E9E; margin-bottom: 0.5rem;
}
.cs-comp-card-pct { font-size: 1.3rem; font-weight: 800; margin-bottom: 0.3rem; }
.cs-comp-card-val { font-size: 0.82rem; color: #757575; }
.cs-comp-track {
    height: 6px; background: #EEEEEE;
    border-radius: 4px; overflow: hidden; margin-top: 0.7rem;
}
.cs-comp-fill-stable { height: 100%; border-radius: 4px; background: #1565C0; }
.cs-comp-fill-crypto  { height: 100%; border-radius: 4px; background: #2E7D32; }

/* ── DeFi placeholder ── */
.cs-defi-nota {
    background: #FAFAFA; border: 1px dashed #BDBDBD;
    border-radius: 10px; padding: 1.2rem 1.5rem;
    color: #9E9E9E; font-size: 0.85rem; text-align: center;
}

/* ── Login box ── */
.cs-login-box {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 12px; padding: 2rem;
    max-width: 420px; margin: 3rem auto;
    text-align: center;
}

/* ── Footer notice ── */
.cs-aviso {
    background: #FAFAFA; border-left: 3px solid #BDBDBD;
    padding: 0.6rem 1rem; color: #9E9E9E;
    font-size: 0.76rem; border-radius: 0 6px 6px 0; margin-top: 1.8rem;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF; border-right: 1px solid #E0E0E0;
}
</style>
""", unsafe_allow_html=True)

SOLANA_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")

# ──────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="cs-logo">Cream<span>Sol</span>.io</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Navigation**")
    st.page_link("app.py",                   label="🏠  Home")
    st.page_link("pages/1_Beginner.py",       label="🟢  Beginner")
    st.page_link("pages/2_Intermediario.py",  label="🔵  Intermediate")
    st.page_link("pages/3_Profissional.py",   label="⚫  Professional")
    st.markdown("---")
    st.caption("v1.0.0 · creamsol.io")

# ──────────────────────────────────────────
# Header
# ──────────────────────────────────────────
st.markdown(
    '<div class="cs-logo">Cream<span>Sol</span>.io'
    '<span class="cs-badge">Intermediate</span></div>',
    unsafe_allow_html=True,
)
st.caption("Detailed performance · Advanced statistics · CSV / JSON export")
st.markdown("---")


# ──────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────
def _parse_float(val_str: str) -> float | None:
    try:
        cleaned = (
            str(val_str)
            .replace("$", "").replace("€", "").replace("£", "")
            .replace("%", "").replace(",", "")
            .replace("+", "").replace("<", "")
            .strip()
        )
        return float(cleaned)
    except Exception:
        return None


def _fmt2(val_str: str) -> str:
    """Rounds any numeric string to 2 decimal places, preserving sign, prefix and suffix."""
    s = str(val_str).strip()
    if s in ("N/A", "N/D", "—", "", "?"):
        return s

    prefix = ""
    for sym in ("$", "€", "£"):
        if sym in s:
            prefix = sym
            break

    suffix = "%" if "%" in s else ""

    sign = ""
    core = s.replace(prefix, "").strip()
    if core.startswith("+"):
        sign = "+"
    elif core.startswith("-") or s.startswith("-"):
        sign = "-"

    v = _parse_float(s)
    if v is None:
        return s

    return f"{sign}{prefix}{abs(v):,.2f}{suffix}"


def _cor(valor_str: str) -> str:
    """Returns CSS class: 'pos', 'neg' or 'nd'."""
    s = str(valor_str).strip()
    if s in ("N/A", "N/D", "—", "", "?"):
        return "nd"
    has_minus = "-" in s
    v = _parse_float(s)
    if v is None:
        return "nd"
    if has_minus:
        v = -abs(v)
    return "pos" if v > 0 else ("neg" if v < 0 else "")


def _metrica(label: str, valor: str, sub: str = "",
             forcar_neg: bool = False, neutral: bool = False,
             tooltip: str = ""):
    """
    Metric card.
    neutral=True   → no colour (always black).
    forcar_neg     → forces CSS class 'neg' (red).
    tooltip        → shows '?' bubble with explanation on hover.
    """
    if neutral:
        cor = ""
    elif forcar_neg:
        cor = "neg"
    else:
        cor = _cor(valor)

    valor_fmt = _fmt2(valor)
    sub_html  = f'<div class="cs-metric-sub">{sub}</div>' if sub else ""

    if tooltip:
        tip_html = f"""<span class="cs-tooltip-wrap">
            <span class="cs-tooltip-icon">?</span>
            <span class="cs-tooltip-box">{tooltip}</span>
        </span>"""
    else:
        tip_html = ""

    st.markdown(f"""
    <div class="cs-metric">
        <div class="cs-metric-label">{label}{tip_html}</div>
        <div class="cs-metric-valor {cor}">{valor_fmt}</div>
        {sub_html}
    </div>""", unsafe_allow_html=True)


def _neg_valor(valor_str: str) -> str:
    """Ensures the value has a negative sign in the displayed string."""
    s = str(valor_str).strip()
    if s in ("N/A", "N/D", "—", "", "?"):
        return s
    if s.startswith("-"):
        return _fmt2(s)
    prefix = ""
    for sym in ("$", "€", "£"):
        if sym in s:
            prefix = sym
            break
    v = _parse_float(s)
    if v is None:
        return s
    return f"-{prefix}{abs(v):,.2f}"


def _pct_float(pct_str: str) -> float:
    v = _parse_float(pct_str)
    return max(0.0, min(100.0, v)) if v is not None else 0.0


def _comp_pct_fmt(pct_str: str) -> str:
    """Formats composition percentage: no sign, no double '%', 2 decimal places."""
    s = str(pct_str).strip().replace("+", "")
    v = _parse_float(s)
    if v is None:
        return s.replace("%", "") + "%"
    return f"{abs(v):.2f}%"


def _estilo_pnl(val):
    """DataFrame cell style for P&L / ROI columns."""
    s = str(val)
    if s in ("N/D", "—", ""):
        return "color: #BDBDBD"
    has_minus = "-" in s
    v = _parse_float(s)
    if v is None:
        return ""
    if has_minus:
        v = -abs(v)
    if v > 0:
        return "color: #2E7D32; font-weight: 700"
    if v < 0:
        return "color: #C62828; font-weight: 700"
    return ""


def _chamar_api(endpoint: str, carteira: str, moeda: str) -> dict | None:
    try:
        url  = f"{API_BASE_URL}/v1/intermediario/{endpoint}/{carteira}?moeda={moeda}"
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


# ──────────────────────────────────────────
# Authentication
# ──────────────────────────────────────────
if "auth_intermediario" not in st.session_state:
    st.session_state["auth_intermediario"] = False

if not st.session_state["auth_intermediario"]:
    st.markdown("""
    <div class="cs-login-box">
        <div style="font-size:2rem; margin-bottom:0.5rem">🔒</div>
        <div style="font-size:1.1rem; font-weight:700; color:#1A1A1A; margin-bottom:0.3rem">
            Private Access
        </div>
        <div style="font-size:0.85rem; color:#757575; margin-bottom:1.2rem">
            Enter your password to access the Intermediate plan.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_f, col_r = st.columns([1, 2, 1])
    with col_f:
        with st.form("form_login"):
            senha_input = st.text_input(
                "Password",
                type="password",
                placeholder="••••",
                label_visibility="collapsed",
            )
            btn_login = st.form_submit_button("Sign in", use_container_width=True)

        if btn_login:
            if senha_input == SENHA_INTERMEDIARIO:
                st.session_state["auth_intermediario"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    st.stop()


# ──────────────────────────────────────────
# Authenticated area
# ──────────────────────────────────────────

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

col_sair, _ = st.columns([1, 5])
with col_sair:
    if st.button("🔓 Sign out", use_container_width=True):
        st.session_state["auth_intermediario"] = False
        st.rerun()

# ──────────────────────────────────────────
# Dashboard
# ──────────────────────────────────────────
if submitted:
    if not carteira or not carteira.strip():
        st.warning("Please enter a Solana wallet address.")
        st.stop()
    if not SOLANA_RE.match(carteira.strip()):
        st.error("Invalid address. Please check and try again.")
        st.stop()

    carteira = carteira.strip()

    with st.spinner("Querying the blockchain, please wait…"):
        snap  = _chamar_api("snapshot",     carteira, moeda)
        perf  = _chamar_api("performance",  carteira, moeda)
        stats = _chamar_api("estatisticas", carteira, moeda)
        defi  = _chamar_api("defi",         carteira, moeda)

    if not snap:
        st.stop()

    # ── Tabs ────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "📈 Performance",
        "📉 Statistics",
        "⚡ DeFi",
        "💾 Export",
    ])

    # ══════════════════════════════════════
    # Tab 1 — Overview
    # ══════════════════════════════════════
    with tab1:

        # ── Snapshot ────
        st.markdown('<div class="cs-section-title">Snapshot</div>', unsafe_allow_html=True)

        n_tokens = snap.get("n_tokens", "—")
        n_nfts   = snap.get("n_nfts",   "—")

        # SOL amount → 2dp
        sol_amount_raw = snap.get("saldo_sol", 0)
        try:
            sol_amount_fmt = f"{abs(float(sol_amount_raw)):,.2f} SOL"
        except Exception:
            sol_amount_fmt = str(sol_amount_raw)

        # Fees SOL → 2dp + negative
        taxas_sol_raw = snap.get("total_taxas_sol", 0)
        try:
            taxas_sol_fmt = f"-{abs(float(taxas_sol_raw)):,.2f} SOL"
        except Exception:
            taxas_sol_fmt = str(taxas_sol_raw)

        c1, c2, c3, c4, c5 = st.columns(5, gap="small")
        with c1:
            _metrica(
                "Total Portfolio",
                snap.get("patrimonio_total_usd", "N/A"),
                sub=f"{n_tokens} tokens",
                tooltip="Total estimated value of all tokens in your wallet at current market prices.",
            )
        with c2:
            _metrica(
                "SOL Balance",
                snap.get("saldo_sol_usd", "N/A"),
                sub=sol_amount_fmt,
                tooltip="Current value and amount of native SOL held in your wallet.",
            )
        with c3:
            _metrica(
                "Tokens",
                str(n_tokens),
                neutral=True,
                tooltip="Total number of token types held in this wallet.",
            )
        with c4:
            _metrica(
                "NFTs",
                str(n_nfts),
                neutral=True,
                tooltip="Total number of NFTs detected in this wallet.",
            )
        with c5:
            _metrica(
                "Fees Paid",
                _neg_valor(snap.get("total_taxas_usd", "N/A")),
                forcar_neg=True,
                tooltip="Total USD equivalent of all network fees (gas) paid across your transaction history.",
            )

        # ── Details ────
        st.markdown('<div class="cs-section-title">Details</div>', unsafe_allow_html=True)

        d1, d2, d3 = st.columns(3, gap="small")
        with d1:
            _metrica(
                "SOL (amount)",
                sol_amount_fmt,
                neutral=True,
                tooltip="Amount of native SOL currently held in your wallet.",
            )
        with d2:
            _metrica(
                "Fees (SOL)",
                taxas_sol_fmt,
                forcar_neg=True,
                sub="last 90 days",
                tooltip="Total SOL spent on network gas fees across all transactions in the last 90 days.",
            )
        with d3:
            _metrica(
                "Est. Slippage",
                _neg_valor(snap.get("total_slippage_usd", "—")),
                forcar_neg=True,
                sub="last 90 days",
                tooltip="Estimated USD value lost to price slippage during token swaps in the last 90 days.",
            )

        # ── Composition ────
        comp = snap.get("composicao", {})
        if isinstance(comp, list):
            comp = {}
        if comp:
            st.markdown('<div class="cs-section-title">Composition</div>', unsafe_allow_html=True)

            pct_st     = _pct_float(comp.get("stablecoins_pct",  "0"))
            pct_cr     = _pct_float(comp.get("criptomoedas_pct", "0"))
            pct_st_fmt = _comp_pct_fmt(comp.get("stablecoins_pct",  "0"))
            pct_cr_fmt = _comp_pct_fmt(comp.get("criptomoedas_pct", "0"))
            val_st_fmt = _fmt2(comp.get("stablecoins",  "—"))
            val_cr_fmt = _fmt2(comp.get("criptomoedas", "—"))

            st.markdown(f"""
            <div class="cs-comp-row">
                <div class="cs-comp-card">
                    <div class="cs-comp-card-label">Stablecoins</div>
                    <div class="cs-comp-card-pct" style="color:#1565C0">{pct_st_fmt}</div>
                    <div class="cs-comp-card-val">{val_st_fmt}</div>
                    <div class="cs-comp-track">
                        <div class="cs-comp-fill-stable" style="width:{pct_st:.1f}%"></div>
                    </div>
                </div>
                <div class="cs-comp-card">
                    <div class="cs-comp-card-label">Crypto</div>
                    <div class="cs-comp-card-pct" style="color:#2E7D32">{pct_cr_fmt}</div>
                    <div class="cs-comp-card-val">{val_cr_fmt}</div>
                    <div class="cs-comp-track">
                        <div class="cs-comp-fill-crypto" style="width:{pct_cr:.1f}%"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Footer ────
        st.markdown(f"""
        <div class="cs-aviso">
            🕒 Timestamp: <strong>{snap.get("timestamp", "—")}</strong>
            &nbsp;·&nbsp;
            🔒 Wallet: <code style="font-size:0.74rem">{carteira}</code>
        </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════
    # Tab 2 — Performance
    # ══════════════════════════════════════
    with tab2:
        if perf and perf.get("tokens"):
            st.markdown('<div class="cs-section-title">Performance by Token</div>', unsafe_allow_html=True)

            rows = []
            for t in perf["tokens"]:
                rows.append({
                    "Symbol":        t.get("simbolo", "?"),
                    "Verified":      "✅" if t.get("verificado") else "⚠️",
                    "Amount":        _fmt2(str(t.get("quantidade_atual", "N/A"))),
                    "Price":         _fmt2(t.get("preco_atual_usd",        "N/A")),
                    "Value":         _fmt2(t.get("valor_atual_usd",        "N/A")),
                    "Vol. Bought":   _fmt2(t.get("volume_comprado_usd",    "N/A")),
                    "Avg. Cost":     _fmt2(t.get("preco_medio_compra_usd", "N/A")),
                    "Unrealised P&L":_fmt2(t.get("lucro_nao_realizado_usd","N/A")),
                    "ROI":           _fmt2(t.get("roi_pct",                "N/A")),
                })

            df_perf = pd.DataFrame(rows)
            styled_perf = (
                df_perf.style
                .map(_estilo_pnl, subset=["Unrealised P&L", "ROI"])
                .set_properties(**{"font-size": "0.84rem"})
            )
            st.dataframe(styled_perf, use_container_width=True, hide_index=True)

            st.markdown(f"""
            <div class="cs-aviso">
                ℹ️ P&amp;L and ROI are estimates based on on-chain transaction history.
                Tokens with unknown cost basis are shown as N/D.
                &nbsp;·&nbsp;
                Wallet: <code style="font-size:0.74rem">{carteira}</code>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("No performance data available for this wallet.")

    # ══════════════════════════════════════
    # Tab 3 — Statistics
    # ══════════════════════════════════════
    with tab3:
        if stats:
            st.markdown('<div class="cs-section-title">Global Summary</div>', unsafe_allow_html=True)

            s1, s2, s3 = st.columns(3, gap="small")
            with s1:
                _metrica(
                    "Total Portfolio",
                    stats.get("patrimonio_total_usd", "N/A"),
                    tooltip="Total estimated value of all tokens at current market prices.",
                )
            with s2:
                _metrica(
                    "Volume Bought",
                    stats.get("volume_total_comprado_usd", "N/A"),
                    tooltip="Total USD value of all purchase transactions identified on-chain.",
                )
            with s3:
                _metrica(
                    "Unrealised P&L",
                    stats.get("lucro_nao_realizado_total_usd", "N/A"),
                    tooltip="Total unrealised profit or loss across all current token positions.",
                )

            s4, s5, s6 = st.columns(3, gap="small")
            with s4:
                _metrica(
                    "Average ROI",
                    stats.get("roi_medio_pct", "N/A"),
                    tooltip="Average return on investment across all tokens with known cost basis.",
                )
            with s5:
                _metrica(
                    "Fees Paid (USD)",
                    _neg_valor(stats.get("total_taxas_usd", "N/A")),
                    forcar_neg=True,
                    sub="last 90 days",
                    tooltip="Total USD equivalent of all network fees paid in the last 90 days.",
                )
            with s6:
                _metrica(
                    "Est. Slippage (USD)",
                    _neg_valor(stats.get("total_slippage_usd", "—")),
                    forcar_neg=True,
                    sub="last 90 days",
                    tooltip="Estimated USD value lost to price slippage during swaps in the last 90 days.",
                )

            st.markdown('<div class="cs-section-title">Token Distribution</div>', unsafe_allow_html=True)

            t1, t2, t3 = st.columns(3, gap="small")
            with t1:
                _metrica(
                    "In Profit",
                    str(stats.get("num_tokens_com_lucro", "—")),
                    neutral=True,
                    tooltip="Number of tokens currently showing unrealised profit.",
                )
            with t2:
                _metrica(
                    "In Loss",
                    str(stats.get("num_tokens_com_prejuizo", "—")),
                    neutral=True,
                    tooltip="Number of tokens currently showing unrealised loss.",
                )
            with t3:
                _metrica(
                    "Unknown Cost (N/D)",
                    str(stats.get("num_tokens_neutros", "—")),
                    neutral=True,
                    tooltip="Tokens where the cost basis could not be determined from on-chain data.",
                )

            if stats.get("aviso"):
                st.markdown(
                    f'<div class="cs-aviso">⚠️ {stats["aviso"]}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No statistics available for this wallet.")

    # ══════════════════════════════════════
    # Tab 4 — DeFi
    # ══════════════════════════════════════
    with tab4:
        st.markdown('<div class="cs-section-title">DeFi Positions</div>', unsafe_allow_html=True)

        if defi:
            stk = defi.get("staking_sol", {})

            stk_sol_raw = stk.get("quantidade_sol", 0)
            try:
                stk_sol_fmt = f"{abs(float(stk_sol_raw)):,.2f} SOL"
            except Exception:
                stk_sol_fmt = str(stk_sol_raw)

            d1, d2 = st.columns(2, gap="small")
            with d1:
                _metrica(
                    "Staking SOL (amount)",
                    stk_sol_fmt,
                    neutral=True,
                    tooltip="Amount of SOL currently staked and earning rewards.",
                )
            with d2:
                _metrica(
                    "Staking SOL (USD)",
                    _fmt2(stk.get("valor_usd", "$0.00")),
                    tooltip="Estimated USD value of your staked SOL at current market price.",
                )

            st.markdown(f"""
            <div class="cs-defi-nota">
                ⚡ {defi.get("nota", "Full DeFi positions (liquidity pools, yield farming) are available on the Professional plan.")}
            </div>""", unsafe_allow_html=True)
        else:
            st.info("No DeFi data available for this wallet.")

    # ══════════════════════════════════════
    # ══ Tab 5 — Exportar ════
    with tab5:
        st.markdown('<div class="cs-section-title">Exportar Dados</div>', unsafe_allow_html=True)

        # Inicializar estado
        for _k in ("int_export_json", "int_export_csv"):
            if _k not in st.session_state:
                st.session_state[_k] = None

        col_j, col_c, _ = st.columns([1, 1, 2], gap="small")

        with col_j:
            if st.button("⬇️ Gerar JSON", use_container_width=True, key="int_btn_json"):
                try:
                    url = f"{API_BASE_URL}/v1/intermediario/export/{carteira}?formato=json&moeda={moeda}"
                    r = requests.get(url, timeout=45)
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
                    url = f"{API_BASE_URL}/v1/intermediario/export/{carteira}?formato=csv&moeda={moeda}"
                    r = requests.get(url, timeout=45)
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