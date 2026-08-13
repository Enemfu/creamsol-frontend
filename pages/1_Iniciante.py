# ====
# pages/1_Iniciante.py — CreamSol.io · Plano Iniciante (Gratuito)
# ====

import streamlit as st
import requests
import pandas as pd
import re
from config import API_BASE_URL
from components.estilo import aplicar_css

st.set_page_config(
    page_title="Iniciante · CreamSol.io",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_css()

# ── CSS local ────
st.markdown("""
<style>
.stApp { background-color: #F5F5F5; }
.block-container { padding-top: 1.2rem; padding-bottom: 1.5rem; max-width: 1100px; }

.cs-logo { font-size: 1.5rem; font-weight: 900; letter-spacing: -0.02em; color: #1A1A1A; }
.cs-logo span.sol { color: #3DBE7A; }
.cs-badge {
    display: inline-block; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    background: #E8F5E9; color: #2E7D32;
    border-radius: 4px; padding: 2px 10px;
    margin-left: 0.6rem; vertical-align: middle;
}
.cs-metric {
    background: #FFFF; border: 1px solid #E0E0E0;
    border-radius: 10px; padding: 0.85rem 1rem; text-align: left;
}
.cs-metric-label {
    font-size: 0.68rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.06em;
    color: #9E9E9E; margin-bottom: 0.25rem;
}
.cs-metric-valor { font-size: 1.3rem; font-weight: 800; color: #1A1A1A; line-height: 1.1; }
.cs-metric-valor.pos { color: #2E7D32; }
.cs-metric-valor.neg { color: #C62828; }
.cs-metric-valor.nd  { color: #BDBDBD; font-size: 1rem; font-weight: 500; }
.cs-metric-delta { font-size: 0.75rem; margin-top: 0.2rem; }
.cs-metric-delta.pos { color: #2E7D32; }
.cs-metric-delta.neg { color: #C62828; }
.cs-metric-delta.nd  { color: #BDBDBD; }

.cs-section-title {
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #9E9E9E; margin: 1.2rem 0 0.5rem 0;
}
.cs-comp-card {
    background: #FFFF; border: 1px solid #E0E0E0;
    border-radius: 10px; padding: 0.85rem 1.1rem;
    display: flex; flex-direction: column; gap: 0.15rem;
}
.cs-comp-label { font-size: 0.68rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.06em; }
.cs-comp-valor { font-size: 1.1rem; font-weight: 700; color: #1A1A1A; }
.cs-comp-pct   { font-size: 0.8rem; color: #757575; }

.cs-taxa-card {
    background: #FFF8F8; border: 1px solid #FFCDD2;
    border-radius: 10px; padding: 0.75rem 1rem;
}
.cs-taxa-label { font-size: 0.68rem; color: #E57373; text-transform: uppercase; letter-spacing: 0.06em; }
.cs-taxa-valor { font-size: 1.1rem; font-weight: 700; color: #C62828; }

.cs-dust-item {
    display: inline-block;
    background: #FAFAFA; border: 1px solid #E0E0E0;
    border-radius: 6px; padding: 3px 10px;
    font-size: 0.78rem; color: #757575; margin: 2px 3px;
}
.cs-aviso {
    background: #FAFAFA; border-left: 3px solid #BDBDBD;
    padding: 0.6rem 1rem; color: #9E9E9E;
    font-size: 0.74rem; border-radius: 0 6px 6px 0; margin-top: 1.2rem;
}
section[data-testid="stSidebar"] {
    background-color: #FFFF; border-right: 1px solid #E0E0E0;
}
thead tr th { background: #F5F5F5 !important; color: #424242 !important; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

SOLANA_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")

# ── Sidebar ────
with st.sidebar:
    st.markdown('<div class="cs-logo">Cream<span class="sol">Sol</span>.io</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Navegação**")
    st.page_link("app.py",                   label="🏠  Início")
    st.page_link("pages/1_Iniciante.py",      label="🟢  Iniciante")
    st.page_link("pages/2_Intermediario.py",  label="🔵  Intermediário")
    st.page_link("pages/3_Profissional.py",   label="⚫  Profissional")
    st.markdown("---")
    st.caption("v1.0.0 · creamsol.io")

# ── Header ────
st.markdown(
    '<div class="cs-logo">Cream<span class="sol">Sol</span>.io'
    '<span class="cs-badge">Gratuito</span></div>',
    unsafe_allow_html=True,
)
st.caption("Saldo, P&L e composição da carteira Solana · Sem registo de dados · Tempo real")
st.markdown("---")

# ── Formulário ────
tab_simples, tab_multi = st.tabs(["📌 Carteira única", "📂 Múltiplas carteiras (máx. 3)"])

with tab_simples:
    with st.form("form_single"):
        col_w, col_m, col_btn = st.columns([5, 1, 1])
        with col_w:
            carteira = st.text_input(
                "Endereço",
                placeholder="Introduza apenas o endereço público da carteira Solana",
                label_visibility="collapsed",
            )
        with col_m:
            moeda = st.selectbox("Moeda", ["USD", "EUR", "GBP"], label_visibility="collapsed")
        with col_btn:
            submitted_single = st.form_submit_button("🔍 Analisar", use_container_width=True)
    st.caption("⚠️ Utilize apenas o endereço público da carteira. Nunca partilhe a sua chave privada.")

with tab_multi:
    with st.form("form_multi"):
        carteiras_raw = st.text_area(
            "Carteiras",
            placeholder="Uma carteira por linha (máx. 3 — Plano Gratuito)",
            height=100,
            label_visibility="collapsed",
        )
        col_mm, col_mb = st.columns([1, 3])
        with col_mm:
            moeda_multi = st.selectbox("Moeda ", ["USD", "EUR", "GBP"], label_visibility="collapsed")
        submitted_multi = st.form_submit_button("🔍 Analisar Consolidado", use_container_width=True)
    st.caption("⚠️ Utilize apenas endereços públicos. O plano Gratuito suporta até 3 carteiras.")


# ── Helpers ────
def _cor(valor_str: str) -> str:
    if not valor_str or str(valor_str).strip() in ("N/D", "", "—"):
        return "nd"
    try:
        v = float(
            str(valor_str)
            .replace("$","").replace("€","").replace("£","")
            .replace("%","").replace(",","").replace("+","")
            .strip()
        )
        return "pos" if v > 0 else ("neg" if v < 0 else "")
    except Exception:
        return "nd"


def _metrica(label: str, valor: str, delta: str = ""):
    cor_v = _cor(valor)
    cor_d = _cor(delta)
    delta_html = (
        f'<div class="cs-metric-delta {cor_d}">{delta} vs 30d</div>'
        if delta and delta != "—" else ""
    )
    st.markdown(f"""
    <div class="cs-metric">
        <div class="cs-metric-label">{label}</div>
        <div class="cs-metric-valor {cor_v}">{valor}</div>
        {delta_html}
    </div>""", unsafe_allow_html=True)


def _taxa_card(label: str, valor: str):
    st.markdown(f"""
    <div class="cs-taxa-card">
        <div class="cs-taxa-label">{label}</div>
        <div class="cs-taxa-valor">{valor}</div>
    </div>""", unsafe_allow_html=True)


def _renderizar_dashboard(d: dict):

    # ── Linha 1 — Patrimônio + 30d ────
    st.markdown('<div class="cs-section-title">Patrimônio</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5, gap="small")
    with c1: _metrica("Hoje",        d["patrimonio_total"],  d.get("delta_valor", "—"))
    with c2: _metrica("Há 30 dias",  d.get("patrimonio_30d", "—"))
    with c3: _metrica("P&L Total",   d["pnl_total"])
    with c4: _metrica("ROI Total",   d["roi_total"])
    with c5: _metrica("NFTs",        str(d["n_nfts"]))

    # ── Linha 2 — Tokens + Atividade ────
    st.markdown('<div class="cs-section-title">Atividade</div>', unsafe_allow_html=True)
    a1, a2, a3, a4 = st.columns(4, gap="small")
    n_tok_delta = d.get("delta_tokens", "—")
    with a1: _metrica("Tokens hoje",    str(d["n_tokens"]),  n_tok_delta)
    with a2: _metrica("Tokens há 30d",  d.get("n_tokens_30d", "—"))
    with a3: _metrica("Volume movim.",  d.get("total_movimentado_usd", "—"))
    with a4: _metrica("Carteiras",      str(d["n_carteiras"]))

    # ── Linha 3 — Taxas (vermelho) ────
    st.markdown('<div class="cs-section-title">Custos de Transação</div>', unsafe_allow_html=True)
    t1, t2, t3, _ = st.columns(4, gap="small")
    with t1: _taxa_card("Taxas (SOL)", f"{d['total_taxas_sol']:.4f} SOL")
    with t2: _taxa_card("Taxas (valor)", d["total_taxas_usd"])
    with t3: _taxa_card("Slippage total", d.get("total_slippage_usd", "—"))

    # ── Composição ────
    st.markdown('<div class="cs-section-title">Composição do Portfólio</div>', unsafe_allow_html=True)
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

    # ── Tokens TOP 3 ────
    st.markdown('<div class="cs-section-title">Top Tokens</div>', unsafe_allow_html=True)
    tokens = d.get("tokens", [])
    top3   = tokens[:3]
    if top3:
        cols = st.columns(len(top3), gap="small")
        for col, t in zip(cols, top3):
            with col:
                delta_30d = t.get("delta_30d", "—")
                _metrica(t["simbolo"], t["valor"], delta_30d if delta_30d != "—" else "")

    # ── Tabela tokens (5 máx) ────
    if tokens:
        st.markdown('<div class="cs-section-title">Tokens</div>', unsafe_allow_html=True)
        rows = []
        for t in tokens[:5]:
            rows.append({
                "Símbolo":     t["simbolo"],
                "✔":           "✅" if t["verificado"] else "⚠️",
                "Quantidade":  t["quantidade"],
                "Preço":       t["preco_atual"],
                "Valor":       t["valor"],
                "Há 30d":      t.get("valor_30d", "—"),
                "Δ 30d":       t.get("delta_30d", "—"),
                "Custo Médio": t["custo_medio"],
                "P&L":         t["pnl"],
                "ROI":         t["roi"],
            })

        df = pd.DataFrame(rows)

        def _estilo(val):
            s = str(val)
            if s in ("N/D", "—", ""):
                return "color:#BDBDBD"
            try:
                v = float(s.replace("$","").replace("€","").replace("£","")
                           .replace("%","").replace(",","").replace("+","").strip())
                if v > 0: return "color:#2E7D32;font-weight:700"
                if v < 0: return "color:#C62828;font-weight:700"
            except Exception:
                pass
            return ""

        styled = (
            df.style
            .map(_estilo, subset=["P&L", "ROI", "Δ 30d"])
            .set_properties(**{"font-size": "0.83rem"})
        )
        st.dataframe(styled, use_container_width=True, hide_index=True)

        if len(tokens) > 5:
            st.caption(f"🔵 +{len(tokens) - 5} tokens adicionais disponíveis no plano Intermediário.")

    # ── Dust ────
    dust = d.get("tokens_dust", [])
    if dust:
        st.markdown('<div class="cs-section-title">Tokens Dust</div>', unsafe_allow_html=True)
        dust_html = "".join(
            f'<span class="cs-dust-item">{t["simbolo"]} · {t["quantidade"]}</span>'
            for t in dust
        )
        st.markdown(dust_html, unsafe_allow_html=True)
        st.caption("🔵 Análise detalhada de tokens dust disponível no plano Intermediário.")

    # ── Aviso legal ────
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
                try:    detalhe = e.response.json().get("detail", e.response.text)
                except: detalhe = e.response.text
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
    elif len(linhas) > 3:
        st.error("O plano Gratuito suporta no máximo 3 carteiras. Faça upgrade para o plano Intermediário.")
    else:
        with st.spinner(f"A consolidar {len(linhas)} carteira(s)..."):
            try:
                payload = {"carteiras": linhas, "moeda": moeda_multi}
                url     = f"{API_BASE_URL}/v1/iniciante/multi"
                resp    = requests.post(url, json=payload, timeout=60)
                resp.raise_for_status()
                st.success(f"✅ Consolidado de {len(linhas)} carteira(s)")
                _renderizar_dashboard(resp.json())
            except requests.exceptions.HTTPError as e:
                try:    detalhe = e.response.json().get("detail", e.response.text)
                except: detalhe = e.response.text
                st.error(f"Erro da API ({e.response.status_code}): {detalhe}")
            except requests.exceptions.Timeout:
                st.error("Timeout — tente novamente.")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")