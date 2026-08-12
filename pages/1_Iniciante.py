# ====
# pages/1_Iniciante.py — CreamSol.io · Plano Iniciante (Gratuito)
# ====

import streamlit as st
import requests
import pandas as pd
import re
from config import API_BASE_URL

st.set_page_config(
    page_title="Iniciante · CreamSol.io",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="collapsed",   # ← sidebar fechada por defeito = mais espaço
)

from components.estilo import aplicar_css
aplicar_css()

st.markdown("""
<style>
.stApp { background-color: #F5F5F5; }
.block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 1200px; }

/* Logo */
.cs-logo { font-size: 1.3rem; font-weight: 900; letter-spacing: -0.02em; color: #1A1A1A; }
.cs-logo span { color: #C62828; }
.cs-badge {
    display: inline-block; font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    background: #E8F5E9; color: #2E7D32;
    border-radius: 4px; padding: 2px 8px; margin-left: 0.5rem; vertical-align: middle;
}

/* Métrica compacta */
.cs-metric {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 8px; padding: 0.6rem 0.9rem; text-align: left;
}
.cs-metric-label {
    font-size: 0.65rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: #9E9E9E; margin-bottom: 0.15rem;
}
.cs-metric-valor {
    font-size: 1.15rem; font-weight: 800; color: #1A1A1A; line-height: 1.1;
}
.cs-metric-valor.pos { color: #2E7D32; }
.cs-metric-valor.neg { color: #C62828; }
.cs-metric-valor.nd  { color: #BDBDBD; font-size: 0.95rem; font-weight: 500; }

/* Título de secção */
.cs-section-title {
    font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: #9E9E9E; margin: 0.8rem 0 0.4rem 0;
}

/* Composição */
.cs-comp-card {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 8px; padding: 0.6rem 0.9rem;
}
.cs-comp-label { font-size: 0.65rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.06em; }
.cs-comp-valor { font-size: 1rem; font-weight: 700; color: #1A1A1A; }
.cs-comp-pct   { font-size: 0.78rem; color: #757575; }

/* Dust */
.cs-dust-item {
    display: inline-block; background: #FAFAFA; border: 1px solid #E0E0E0;
    border-radius: 6px; padding: 2px 8px; font-size: 0.72rem; color: #757575; margin: 2px;
}

/* Upsell */
.cs-upsell {
    background: linear-gradient(135deg, #1A237E 0%, #283593 100%);
    border-radius: 10px; padding: 0.7rem 1.1rem;
    display: flex; align-items: center; justify-content: space-between;
    margin-top: 0.6rem;
}
.cs-upsell-txt { color: #FFFFFF; font-size: 0.8rem; font-weight: 600; }
.cs-upsell-sub { color: #9FA8DA; font-size: 0.7rem; margin-top: 2px; }

/* Aviso */
.cs-aviso {
    background: #FAFAFA; border-left: 3px solid #BDBDBD;
    padding: 0.4rem 0.8rem; color: #9E9E9E;
    font-size: 0.7rem; border-radius: 0 6px 6px 0; margin-top: 0.6rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF; border-right: 1px solid #E0E0E0;
}

/* Tabela compacta */
thead tr th { background: #F5F5F5 !important; color: #424242 !important; font-size: 0.78rem; }
tbody tr td { font-size: 0.8rem !important; }

/* Remover padding excessivo dos tabs */
.stTabs [data-baseweb="tab-panel"] { padding-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

SOLANA_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")

# ── Sidebar ────
with st.sidebar:
    st.markdown('<div class="cs-logo">Cream<span>Sol</span>.io</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Navegação**")
    st.page_link("app.py",                  label="🏠  Início")
    st.page_link("pages/1_Iniciante.py",     label="🟢  Iniciante")
    st.page_link("pages/2_Intermediario.py", label="🔵  Intermediário")
    st.page_link("pages/3_Profissional.py",  label="⚫  Profissional")
    st.markdown("---")
    st.caption("v1.0.0 · creamsol.io")

# ── Header compacto ────
col_hdr, col_nav = st.columns([5, 1])
with col_hdr:
    st.markdown(
        '<div class="cs-logo">Cream<span>Sol</span>.io'
        '<span class="cs-badge">Gratuito</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("Saldo, P&L e composição da carteira Solana · Sem registo de dados · Tempo real")

st.markdown("<​hr style='margin: 0.4rem 0 0.6rem 0; border-color: #E0E0E0;'>", unsafe_allow_html=True)

# ── Formulário compacto (linha única) ────
tab_simples, tab_multi = st.tabs(["📌 Carteira única", "📂 Múltiplas carteiras (até 5)"])

with tab_simples:
    with st.form("form_single"):
        col_w, col_m, col_btn = st.columns([5, 1, 1])
        with col_w:
            carteira = st.text_input(
                "Carteira",
                placeholder="Endereço Solana (ex: Eyd3D8Fz...)",
                label_visibility="collapsed",
            )
        with col_m:
            moeda = st.selectbox("Moeda", ["USD", "EUR"], label_visibility="collapsed")
        with col_btn:
            submitted_single = st.form_submit_button("🔍 Analisar", use_container_width=True)

with tab_multi:
    with st.form("form_multi"):
        col_ta, col_right = st.columns([4, 1])
        with col_ta:
            carteiras_raw = st.text_area(
                "Carteiras",
                placeholder="Uma carteira por linha (máx. 5)",
                height=80,
                label_visibility="collapsed",
            )
        with col_right:
            moeda_multi = st.selectbox("Moeda ", ["USD", "EUR"], label_visibility="collapsed")
            submitted_multi = st.form_submit_button("🔍 Consolidar", use_container_width=True)


# ── Funções auxiliares ────
def _cor_classe(valor_str: str) -> str:
    if not valor_str or valor_str.strip() in ("N/D", "", "—"):
        return "nd"
    try:
        v = float(
            valor_str
            .replace("$","").replace("€","")
            .replace("%","").replace(",","")
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
    # ── Layout em duas colunas: esquerda (métricas) | direita (tabela) ────
    col_esq, col_dir = st.columns([1, 2], gap="medium")

    with col_esq:
        # Visão Geral
        st.markdown('<div class="cs-section-title">Visão Geral</div>', unsafe_allow_html=True)
        g1, g2 = st.columns(2, gap="small")
        with g1: _metrica("Patrimônio", d["patrimonio_total"])
        with g2: _metrica("P&L Total",  d["pnl_total"])
        g3, g4, g5 = st.columns(3, gap="small")
        with g3: _metrica("ROI",    d["roi_total"])
        with g4: _metrica("Tokens", str(d["n_tokens"]))
        with g5: _metrica("NFTs",   str(d["n_nfts"]))

        # Composição
        st.markdown('<div class="cs-section-title">Composição</div>', unsafe_allow_html=True)
        comp = d["composicao"]
        p1, p2 = st.columns(2, gap="small")
        with p1:
            st.markdown(f"""
            <div class="cs-comp-card">
                <div class="cs-comp-label">Stablecoins</div>
                <div class="cs-comp-valor">{comp['stablecoins']}</div>
                <div class="cs-comp-pct">{comp['stablecoins_pct']}</div>
            </div>""", unsafe_allow_html=True)
        with p2:
            st.markdown(f"""
            <div class="cs-comp-card">
                <div class="cs-comp-label">Criptomoedas</div>
                <div class="cs-comp-valor">{comp['criptomoedas']}</div>
                <div class="cs-comp-pct">{comp['criptomoedas_pct']}</div>
            </div>""", unsafe_allow_html=True)

        # Actividade
        st.markdown('<div class="cs-section-title">Actividade (90 dias)</div>', unsafe_allow_html=True)
        a1, a2 = st.columns(2, gap="small")
        taxa_sol = d.get("total_taxas_sol", 0.0)
        with a1: _metrica("Taxas SOL", f"{taxa_sol:.4f} SOL")
        with a2: _metrica("Taxas USD", d.get("total_taxas_usd", "N/D"))
        a3, a4 = st.columns(2, gap="small")
        with a3: _metrica("Slippage",  d.get("total_slippage_usd",    "N/D"))
        with a4: _metrica("Volume",    d.get("total_movimentado_usd", "N/D"))

        # Aviso legal
        st.markdown(f"""
        <div class="cs-aviso">
            🔒 {d.get("aviso_legal", "Dados apenas informativos. Nenhum dado é armazenado.")}
        </div>""", unsafe_allow_html=True)

    with col_dir:
        # Tabela de tokens — apenas top 3
        st.markdown('<div class="cs-section-title">Top 3 Tokens por Valor</div>', unsafe_allow_html=True)
        tokens = d.get("tokens", [])

        if tokens:
            top3  = tokens[:3]
            resto = tokens[3:]

            rows = []
            for t in top3:
                rows.append({
                    "Símbolo":     t["simbolo"],
                    "✓":           "✅" if t["verificado"] else "⚠️",
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
                    v = float(
                        str(val)
                        .replace("$","").replace("€","")
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
                .set_properties(**{"font-size": "0.8rem"})
            )
            st.dataframe(styled, use_container_width=True, hide_index=True)

            # ── Upsell ────
            if resto:
                n_ocultos = len(resto)
                valor_oculto = sum(
                    float(
                        t["valor"]
                        .replace("$","").replace("€","")
                        .replace("K","e3").replace(",","")
                        .strip()
                    )
                    for t in resto
                    if t["valor"] not in ("N/D","")
                )
                valor_fmt = f"${valor_oculto:,.0f}" if valor_oculto > 0 else f"{n_ocultos} token(s)"
                st.markdown(f"""
                <div class="cs-upsell">
                    <div>
                        <div class="cs-upsell-txt">🔒 +{n_ocultos} tokens ocultos · {valor_fmt}</div>
                        <div class="cs-upsell-sub">Aceda ao plano Intermediário ou Profissional para ver a análise completa</div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Nenhum token significativo encontrado.")

        # Dust
        dust = d.get("tokens_dust", [])
        if dust:
            st.markdown('<div class="cs-section-title">Tokens Dust</div>', unsafe_allow_html=True)
            dust_html = "".join(
                f'<span class="cs-dust-item">{t["simbolo"]} · {t["quantidade"]}</span>'
                for t in dust[:10]
            )
            st.markdown(dust_html, unsafe_allow_html=True)


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
    elif len(linhas) > 5:
        st.error("Máximo de 5 carteiras por pedido.")
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