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

.cs-section-title {
    font-size: 0.78rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #9E9E9E; margin: 1.6rem 0 0.6rem 0;
}

/* Composition cards — side by side */
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

.cs-aviso {
    background: #FAFAFA; border-left: 3px solid #BDBDBD;
    padding: 0.6rem 1rem; color: #9E9E9E;
    font-size: 0.76rem; border-radius: 0 6px 6px 0; margin-top: 1.8rem;
}

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
    st.page_link("app.py",                  label="🏠  Home")
    st.page_link("pages/1_Iniciante.py",     label="🟢  Beginner")
    st.page_link("pages/2_Intermediario.py", label="🔵  Intermediate")
    st.page_link("pages/3_Profissional.py",  label="⚫  Professional")
    st.markdown("---")
    st.caption("v1.0.0 · creamsol.io")

# ──────────────────────────────────────────
# Header
# ──────────────────────────────────────────
st.markdown(
    '<div class="cs-logo">Cream<span>Sol</span>.io'
    '<span class="cs-badge">Beginner</span></div>',
    unsafe_allow_html=True,
)
st.caption("Portfolio snapshot · Token performance · Basic metrics")
st.markdown("---")


# ──────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────
def _parse_float(val_str: str) -> float | None:
    """Extrai float de qualquer string formatada: '$1,234.56', '-€20.00', '12.3%'."""
    try:
        cleaned = (
            str(val_str)
            .replace("$", "").replace("€", "").replace("£", "")
            .replace("%", "").replace(",", "").replace("+", "")
            .replace("<", "").replace("—", "").strip()
        )
        return float(cleaned)
    except Exception:
        return None


def _fmt2(val_str: str, prefix: str = "", suffix: str = "") -> str:
    """
    Reformata qualquer valor numérico para 2 casas decimais.
    Preserva sinal, prefixo monetário e sufixo (%).
    Valores não numéricos (N/A, N/D, —) passam sem alteração.
    """
    s = str(val_str).strip()
    if s in ("N/A", "N/D", "—", "", "?", "N/D"):
        return s

    # Detecta prefixo monetário original
    detected_prefix = ""
    for sym in ("$", "€", "£"):
        if sym in s:
            detected_prefix = sym
            break

    # Detecta sufixo
    detected_suffix = "%" if "%" in s else ""

    # Detecta sinal
    sign = ""
    stripped = s.lstrip("$€£").strip()
    if stripped.startswith("+"):
        sign = "+"
    elif stripped.startswith("-") or s.startswith("-"):
        sign = "-"

    v = _parse_float(s)
    if v is None:
        return s

    p  = prefix  or detected_prefix
    su = suffix  or detected_suffix
    return f"{sign}{p}{abs(v):,.2f}{su}"


def _cor(valor_str: str) -> str:
    """Retorna classe CSS: 'pos', 'neg' ou 'nd'."""
    s = str(valor_str).strip()
    if s in ("N/A", "N/D", "—", "", "?"):
        return "nd"
    v = _parse_float(s)
    if v is None:
        return "nd"
    return "pos" if v > 0 else ("neg" if v < 0 else "")


def _metrica(label: str, valor: str, sub: str = "", forcar_neg: bool = False):
    """Renderiza um card de métrica com label, valor formatado e sub-texto opcional."""
    cor    = "neg" if forcar_neg else _cor(valor)
    valor_fmt = _fmt2(valor)
    sub_html  = f'<div class="cs-metric-sub">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div class="cs-metric">
        <div class="cs-metric-label">{label}</div>
        <div class="cs-metric-valor {cor}">{valor_fmt}</div>
        {sub_html}
    </div>""", unsafe_allow_html=True)


def _pct_float(pct_str: str) -> float:
    v = _parse_float(pct_str)
    return max(0.0, min(100.0, v)) if v is not None else 0.0


def _delta_tokens_fmt(delta_tok) -> str:
    """Formata delta de tokens com sinal explícito."""
    try:
        dt = int(str(delta_tok).replace("+", "").replace("—", "").strip())
        return f"+{dt}" if dt > 0 else str(dt)
    except Exception:
        return str(delta_tok) if delta_tok not in (None, "—", "") else "—"


# ──────────────────────────────────────────
# API
# ──────────────────────────────────────────
def _chamar_api(carteira: str, moeda: str) -> dict | None:
    try:
        url  = f"{API_BASE_URL}/v1/iniciante/{carteira}?moeda={moeda}"
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
# Dashboard
# ──────────────────────────────────────────
def _renderizar_dashboard(d: dict, carteira: str):

    # ── Extrai dados SOL da lista de tokens ────
    sol_amount_raw = "—"
    sol_valor_raw  = "—"
    for t in d.get("tokens", []):
        simbolo_limpo = str(t.get("simbolo", "")).replace("⚠️ ", "").strip().upper()
        if simbolo_limpo in ("SOL", "WSOL"):
            q = t.get("quantidade", None)
            sol_amount_raw = f"{float(q):.6f}" if isinstance(q, (int, float)) else str(q or "—")
            sol_valor_raw  = t.get("valor", "—")
            break

    # ─────────────────────────────────────
    # SECTION 1 — Portfolio Overview
    # ─────────────────────────────────────
    st.markdown('<div class="cs-section-title">Portfolio Overview</div>', unsafe_allow_html=True)

    n_tokens_atual = d.get("n_tokens", "—")
    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        _metrica(
            "Total Portfolio",
            d.get("patrimonio_total", "N/A"),
            sub=f"{n_tokens_atual} tokens",
        )
    with c2:
        _metrica(
            "SOL Balance",
            sol_valor_raw,
            sub=f"{sol_amount_raw} SOL",
        )
    with c3:
        _metrica("Total P&L", d.get("pnl_total", "N/A"))
    with c4:
        _metrica(
            "Fees Paid",
            d.get("total_taxas_usd", "N/A"),
            forcar_neg=True,
        )

    # ─────────────────────────────────────
    # SECTION 2 — 30-Day Comparison
    # ─────────────────────────────────────
    st.markdown('<div class="cs-section-title">30-Day Comparison</div>', unsafe_allow_html=True)

    pat_atual  = d.get("patrimonio_total", "—")
    pat_30d    = d.get("patrimonio_30d",   "N/D")
    n_atual    = d.get("n_tokens",         "—")
    n_30d      = d.get("n_tokens_30d",     "—")
    delta_tok  = d.get("delta_tokens",     "—")
    delta_tok_fmt = _delta_tokens_fmt(delta_tok)

    # Calcula delta_valor com sinal correcto a partir dos floats
    pat_atual_v = _parse_float(str(pat_atual)) or 0.0
    pat_30d_v   = _parse_float(str(pat_30d))   or 0.0

    if pat_30d_v > 0:
        delta_calc = pat_atual_v - pat_30d_v
        # Detecta símbolo monetário do patrimonio_total
        sym = ""
        for s in ("$", "€", "£"):
            if s in str(pat_atual):
                sym = s
                break
        delta_val = f"{'+' if delta_calc >= 0 else ''}{sym}{abs(delta_calc):,.2f}"
    else:
        # Fallback: usa o que a API devolveu
        delta_val = d.get("delta_valor", "—")

    m1, m2, m3 = st.columns(3, gap="small")
    with m1:
        _metrica("Now",     pat_atual, sub=f"{n_atual} tokens")
    with m2:
        _metrica("30d ago", pat_30d,   sub=f"{n_30d} tokens" if n_30d != "—" else "—")
    with m3:
        _metrica("Change",  delta_val, sub=f"{delta_tok_fmt} tokens")

    # ─────────────────────────────────────
    # SECTION 3 — Details
    # ─────────────────────────────────────
    st.markdown('<div class="cs-section-title">Details</div>', unsafe_allow_html=True)

    taxas_sol_raw = d.get("total_taxas_sol", 0)
    try:
        taxas_sol_fmt = f"{float(taxas_sol_raw):.6f} SOL"
    except Exception:
        taxas_sol_fmt = str(taxas_sol_raw)

    d1, d2, d3, d4 = st.columns(4, gap="small")
    with d1:
        _metrica("SOL (amount)", sol_amount_raw)
    with d2:
        _metrica("Fees (SOL)",    taxas_sol_fmt,                        forcar_neg=True)
    with d3:
        _metrica("Est. Slippage", d.get("total_slippage_usd", "—"),     forcar_neg=True)
    with d4:
        _metrica("Moved (USD)",   d.get("total_movimentado_usd", "—"),  forcar_neg=True)

    # ─────────────────────────────────────
    # SECTION 4 — Composition
    # ─────────────────────────────────────
    comp = d.get("composicao", {})
    # Defesa: a API pode devolver dict ou objeto
    if isinstance(comp, list):
        comp = {}
    if comp:
        st.markdown('<div class="cs-section-title">Composition</div>', unsafe_allow_html=True)

        pct_st     = _pct_float(comp.get("stablecoins_pct",  "0"))
        pct_cr     = _pct_float(comp.get("criptomoedas_pct", "0"))
        val_st_fmt = _fmt2(comp.get("stablecoins",      "—"))
        val_cr_fmt = _fmt2(comp.get("criptomoedas",     "—"))
        pct_st_fmt = _fmt2(comp.get("stablecoins_pct",  "—"))
        pct_cr_fmt = _fmt2(comp.get("criptomoedas_pct", "—"))

        st.markdown(f"""
        <div class="cs-comp-row">
            <div class="cs-comp-card">
                <div class="cs-comp-card-label">Stablecoins</div>
                <div class="cs-comp-card-pct" style="color:#1565C0">{pct_st_fmt}%</div>
                <div class="cs-comp-card-val">{val_st_fmt}</div>
                <div class="cs-comp-track">
                    <div class="cs-comp-fill-stable" style="width:{pct_st:.1f}%"></div>
                </div>
            </div>
            <div class="cs-comp-card">
                <div class="cs-comp-card-label">Crypto</div>
                <div class="cs-comp-card-pct" style="color:#2E7D32">{pct_cr_fmt}%</div>
                <div class="cs-comp-card-val">{val_cr_fmt}</div>
                <div class="cs-comp-track">
                    <div class="cs-comp-fill-crypto" style="width:{pct_cr:.1f}%"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ─────────────────────────────────────
    # SECTION 5 — Tokens (Top 3 + locked)
    # ─────────────────────────────────────
    st.markdown('<div class="cs-section-title">Tokens</div>', unsafe_allow_html=True)

    tokens = d.get("tokens", [])
    if tokens:
        rows = []
        for t in tokens:
            rows.append({
                "Symbol":    t.get("simbolo", "?"),
                "Verified":  "✅" if t.get("verificado") else "⚠️",
                "Amount":    _fmt2(str(t.get("quantidade", "N/A"))),
                "Price":     _fmt2(t.get("preco_atual", "N/A")),
                "Value":     _fmt2(t.get("valor", "N/A")),
                "Avg. Cost": _fmt2(t.get("custo_medio", "N/A")),
                "P&L":       _fmt2(t.get("pnl", "N/A")),
                "ROI":       _fmt2(t.get("roi", "N/A")),
            })

        df = pd.DataFrame(rows)

        def _estilo_col(val):
            v = _parse_float(str(val))
            if v is None:
                return ""
            if v > 0:
                return "color: #2E7D32; font-weight: 700"
            if v < 0:
                return "color: #C62828; font-weight: 700"
            return ""

        # Top 3 visível
        styled_top = (
            df.head(3).style
            .map(_estilo_col, subset=["P&L", "ROI"])
            .set_properties(**{"font-size": "0.85rem"})
        )
        st.dataframe(styled_top, use_container_width=True, hide_index=True)

        # Restante — locked
        if len(df) > 3:
            with st.expander(f"🔒 {len(df) - 3} more tokens — Intermediate plan required"):
                st.markdown("""
                <div style="text-align:center; padding:1.5rem 0;">
                    <div style="font-size:1.5rem; margin-bottom:0.5rem">🔒</div>
                    <div style="font-weight:700; color:#1A1A1A; margin-bottom:0.4rem">
                        Intermediate Plan required
                    </div>
                    <div style="font-size:0.85rem; color:#757575;">
                        Upgrade to view your full token list, detailed P&amp;L,
                        ROI per token and CSV export.
                    </div>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("No significant tokens found in this wallet.")

    # ─────────────────────────────────────
    # SECTION 6 — Dust tokens
    # ─────────────────────────────────────
    dust = d.get("tokens_dust", [])
    if dust:
        with st.expander(f"🪣 Dust tokens ({len(dust)})"):
            dust_rows = [
                {
                    "Symbol": t.get("simbolo", "?"),
                    "Amount": _fmt2(str(t.get("quantidade", "—"))),
                }
                for t in dust
            ]
            st.dataframe(pd.DataFrame(dust_rows), use_container_width=True, hide_index=True)

    # ─────────────────────────────────────
    # Footer
    # ─────────────────────────────────────
    st.markdown(f"""
    <div class="cs-aviso">
        🔒 <strong>Privacy:</strong> For informational purposes only. No wallet address or personal data
        is stored, logged or shared. CreamSol.io does not constitute financial or tax advice.
        &nbsp;·&nbsp;
        🕒 Wallet: <code style="font-size:0.74rem">{carteira}</code>
    </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────
# Wallet input form
# ──────────────────────────────────────────
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