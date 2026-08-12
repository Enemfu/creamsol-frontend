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
    initial_sidebar_state="collapsed",
)

from components.estilo import aplicar_css
aplicar_css()

st.markdown("""
<style>
/* ── Base ── */
.stApp { background-color: #F2F4F7; }
.block-container { padding-top: 0.4rem; padding-bottom: 0.4rem; max-width: 1280px; }

/* Esconder toolbar e header nativo do Streamlit */
div[data-testid="stToolbar"]      { display: none !important; }
div[data-testid="stHeader"]       { display: none !important; }
header[data-testid="stHeader"]    { display: none !important; }

/* ── Logo ── */
.cs-logo {
    font-size: 1.4rem; font-weight: 900;
    letter-spacing: -0.03em; color: #1A1A1A; line-height: 1;
}
.cs-logo span { color: #C62828; }
.cs-badge {
    display: inline-block; font-size: 0.6rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    background: #E8F5E9; color: #2E7D32;
    border-radius: 4px; padding: 2px 8px;
    margin-left: 0.5rem; vertical-align: middle;
}

/* ── Hero ── */
.cs-hero {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 12px; padding: 1rem 1.4rem; margin-bottom: 0.5rem;
}
.cs-hero-label {
    font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: #9E9E9E; margin-bottom: 0.2rem;
}
.cs-hero-valor {
    font-size: 2.2rem; font-weight: 900; color: #1A1A1A; line-height: 1;
}
.cs-hero-sub { font-size: 0.75rem; color: #9E9E9E; margin-top: 0.3rem; }

/* ── Métrica ── */
.cs-metric {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 8px; padding: 0.55rem 0.8rem;
}
.cs-metric-label {
    font-size: 0.62rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: #BDBDBD; margin-bottom: 0.1rem;
}
.cs-metric-valor {
    font-size: 1.05rem; font-weight: 800; color: #1A1A1A; line-height: 1.1;
}
.cs-metric-valor.pos { color: #2E7D32; }
.cs-metric-valor.neg { color: #C62828; }
.cs-metric-valor.nd  { color: #BDBDBD; font-size: 0.85rem; font-weight: 400; }
/* Custo — taxas/fees sempre vermelho */
.cs-metric-valor.custo { color: #C62828; font-weight: 800; }

/* ── Composição ── */
.cs-comp-wrap {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 8px; padding: 0.75rem 1rem;
}
.cs-comp-title {
    font-size: 0.62rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: #BDBDBD; margin-bottom: 0.5rem;
}
.cs-comp-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0.4rem; }
.cs-comp-block { display: flex; flex-direction: column; }
.cs-comp-block.right { text-align: right; }
.cs-comp-lbl { font-size: 0.62rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.06em; }
.cs-comp-val { font-size: 1rem; font-weight: 700; color: #1A1A1A; }
.cs-comp-pct { font-size: 0.72rem; color: #757575; }
.cs-comp-bar-outer {
    background: #E0E0E0; border-radius: 4px; height: 8px; overflow: hidden;
}
.cs-comp-bar-stable {
    background: #1565C0; height: 8px; border-radius: 4px 0 0 4px; float: left;
}
.cs-comp-bar-crypto {
    background: #C62828; height: 8px; border-radius: 0 4px 4px 0; float: left;
}
.cs-comp-legend {
    display: flex; gap: 1rem; margin-top: 0.35rem;
}
.cs-comp-dot {
    width: 8px; height: 8px; border-radius: 50%;
    display: inline-block; margin-right: 4px; vertical-align: middle;
}

/* ── Secção título ── */
.cs-section {
    font-size: 0.62rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.12em; color: #BDBDBD; margin: 0.75rem 0 0.35rem 0;
}

/* ── Tabela ── */
thead tr th { background: #F5F5F5 !important; color: #616161 !important; font-size: 0.76rem !important; }
tbody tr td { font-size: 0.78rem !important; }

/* ── Upsell ── */
.cs-upsell {
    background: linear-gradient(135deg, #1A237E, #283593);
    border-radius: 10px; padding: 0.85rem 1.1rem;
    display: flex; align-items: center; gap: 0.8rem;
    margin-top: 0.9rem;
}
.cs-upsell-icon { font-size: 1.3rem; }
.cs-upsell-txt  { color: #FFFFFF; font-size: 0.82rem; font-weight: 700; }
.cs-upsell-sub  { color: #9FA8DA; font-size: 0.7rem; margin-top: 3px; }

/* ── Aviso ── */
.cs-aviso {
    background: #FAFAFA; border-left: 3px solid #E0E0E0;
    padding: 0.35rem 0.75rem; color: #BDBDBD;
    font-size: 0.65rem; border-radius: 0 6px 6px 0; margin-top: 0.6rem;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E0E0E0; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-panel"] { padding-top: 0.4rem; }
</style>
""", unsafe_allow_html=True)

SOLANA_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")

# ── Sidebar ────
with st.sidebar:
    st.markdown('<div class="cs-logo">Cream<span>Sol</span>.io</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",                  label="🏠  Início")
    st.page_link("pages/1_Iniciante.py",     label="🟢  Iniciante")
    st.page_link("pages/2_Intermediario.py", label="🔵  Intermediário")
    st.page_link("pages/3_Profissional.py",  label="⚫  Profissional")
    st.markdown("---")
    st.caption("v1.0.0 · creamsol.io")

# ── Header — logo visível imediatamente ────
col_logo, col_caption = st.columns([3, 6])
with col_logo:
    st.markdown(
        '<div class="cs-logo">Cream<span>Sol</span>.io'
        '<span class="cs-badge">Gratuito</span></div>',
        unsafe_allow_html=True,
    )
with col_caption:
    st.caption("Análise da carteira Solana · Sem registo de dados · Tempo real")

st.divider()

# ── Formulário ────
tab_simples, tab_multi = st.tabs(["📌 Carteira única", "📂 Múltiplas carteiras (até 5)"])

with tab_simples:
    with st.form("form_single"):
        col_w, col_m, col_btn = st.columns([6, 1, 1])
        with col_w:
            carteira = st.text_input(
                "Carteira",
                placeholder="Cole aqui o endereço da carteira Solana...",
                label_visibility="collapsed",
            )
        with col_m:
            moeda = st.selectbox("Moeda", ["USD", "EUR"], label_visibility="collapsed")
        with col_btn:
            submitted_single = st.form_submit_button("🔍 Analisar", use_container_width=True)

with tab_multi:
    with st.form("form_multi"):
        col_ta, col_r = st.columns([5, 1])
        with col_ta:
            carteiras_raw = st.text_area(
                "Carteiras",
                placeholder="Cole um endereço por linha (máx. 5 carteiras)...",
                height=75,
                label_visibility="collapsed",
            )
        with col_r:
            moeda_multi = st.selectbox("Moeda ", ["USD", "EUR"], label_visibility="collapsed")
            submitted_multi = st.form_submit_button("🔍 Consolidar", use_container_width=True)


# ── Helpers ────
def _cor(v: str) -> str:
    if not v or v.strip() in ("N/D", "", "—"):
        return "nd"
    try:
        n = float(v.replace("$","").replace("€","").replace("%","").replace(",","").strip())
        return "pos" if n > 0 else ("neg" if n < 0 else "")
    except:
        return "nd"


def _metrica(label: str, valor: str, custo: bool = False):
    """custo=True força vermelho (taxas, slippage)."""
    cls = "custo" if custo else _cor(valor)
    st.markdown(f"""
    <div class="cs-metric">
        <div class="cs-metric-label">{label}</div>
        <div class="cs-metric-valor {cls}">{valor}</div>
    </div>""", unsafe_allow_html=True)


def _renderizar_dashboard(d: dict):
    col_esq, col_dir = st.columns([5, 7], gap="medium")

    # ══════════════════════════════════
    # COLUNA ESQUERDA
    # ══════════════════════════════════
    with col_esq:

        # 1 — Hero: Patrimônio
        pnl     = d.get("pnl_total", "N/D")
        cor_pnl = ("color:#2E7D32" if _cor(pnl) == "pos"
                   else ("color:#C62828" if _cor(pnl) == "neg" else "color:#BDBDBD"))
        st.markdown(f"""
        <div class="cs-hero">
            <div class="cs-hero-label">Patrimônio Total</div>
            <div class="cs-hero-valor">{d['patrimonio_total']}</div>
            <div class="cs-hero-sub">
                P&L: <span style="font-weight:700;{cor_pnl}">{pnl}</span>
                &nbsp;·&nbsp;
                ROI: <span style="font-weight:700;{cor_pnl}">{d.get('roi_total','N/D')}</span>
                &nbsp;·&nbsp;
                {d['n_tokens']} tokens &nbsp;·&nbsp; {d['n_nfts']} NFTs
            </div>
        </div>""", unsafe_allow_html=True)

        # 2 — Composição: barra bicolor com legenda clara
        comp = d["composicao"]
        try:
            pct_stable = max(0, min(100, float(comp["stablecoins_pct"].replace("%","").strip())))
        except:
            pct_stable = 0
        pct_crypto = 100 - pct_stable

        st.markdown(f"""
        <div class="cs-comp-wrap">
            <div class="cs-comp-title">Composição do Portfólio</div>
            <div class="cs-comp-row">
                <div class="cs-comp-block">
                    <span class="cs-comp-lbl">
                        <span class="cs-comp-dot" style="background:#1565C0;"></span>Stablecoins
                    </span>
                    <span class="cs-comp-val">{comp['stablecoins']}</span>
                    <span class="cs-comp-pct">{comp['stablecoins_pct']} do portfólio</span>
                </div>
                <div class="cs-comp-block right">
                    <span class="cs-comp-lbl">
                        Criptomoedas<span class="cs-comp-dot" style="background:#C62828;margin-left:4px;margin-right:0;"></span>
                    </span>
                    <span class="cs-comp-val">{comp['criptomoedas']}</span>
                    <span class="cs-comp-pct">{comp['criptomoedas_pct']} do portfólio</span>
                </div>
            </div>
            <div class="cs-comp-bar-outer" style="overflow:hidden;height:8px;border-radius:4px;background:#E0E0E0;margin-top:0.5rem;">
                <div style="width:{pct_stable}%;background:#1565C0;height:8px;float:left;
                     border-radius:{'4px 0 0 4px' if pct_crypto > 0 else '4px'};"></div>
                <div style="width:{pct_crypto}%;background:#C62828;height:8px;float:left;
                     border-radius:{'0 4px 4px 0' if pct_stable > 0 else '4px'};"></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # 3 — Actividade 90 dias (taxas sempre vermelho)
        st.markdown('<div class="cs-section">Actividade · 90 dias</div>', unsafe_allow_html=True)
        r1, r2 = st.columns(2, gap="small")
        taxa_sol = d.get("total_taxas_sol", 0.0)
        with r1: _metrica("Taxas On-Chain", f"{taxa_sol:.4f} SOL", custo=True)
        with r2: _metrica("Taxas (USD)",    d.get("total_taxas_usd",       "N/D"), custo=True)
        r3, r4 = st.columns(2, gap="small")
        with r3: _metrica("Slippage Est.",  d.get("total_slippage_usd",    "N/D"), custo=True)
        with r4: _metrica("Vol. Total",     d.get("total_movimentado_usd", "N/D"))

        # Aviso legal
        st.markdown(f"""
        <div class="cs-aviso">
            🔒 {d.get('aviso_legal','Dados apenas informativos. Nenhum dado é armazenado.')}
        </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════
    # COLUNA DIREITA
    # ══════════════════════════════════
    with col_dir:
        st.markdown('<div class="cs-section">Top 3 Tokens por Valor</div>', unsafe_allow_html=True)
        tokens = d.get("tokens", [])

        if tokens:
            top3  = tokens[:3]
            resto = tokens[3:]

            rows = [{
                "Símbolo":     t["simbolo"],
                "✓":           "✅" if t["verificado"] else "⚠️",
                "Quantidade":  t["quantidade"],
                "Preço":       t["preco_atual"],
                "Valor":       t["valor"],
                "Custo Médio": t["custo_medio"],
                "P&L":         t["pnl"],
                "ROI":         t["roi"],
            } for t in top3]

            df = pd.DataFrame(rows)

            def _style(val):
                s = str(val)
                if s in ("N/D","","nan"):
                    return "color:#BDBDBD"
                try:
                    v = float(s.replace("$","").replace("€","").replace("%","").replace(",","").strip())
                    if v > 0: return "color:#2E7D32;font-weight:700"
                    if v < 0: return "color:#C62828;font-weight:700"
                except:
                    pass
                return ""

            styled = (
                df.style
                .map(_style, subset=["P&L","ROI"])
                .set_properties(**{"font-size":"0.78rem"})
            )
            st.dataframe(styled, use_container_width=True, hide_index=True, height=160)

            # Upsell — com espaçamento generoso acima
            if resto:
                n = len(resto)
                try:
                    val_oculto = sum(
                        float(t["valor"].replace("$","").replace("€","")
                              .replace("K","e3").replace(",","").strip())
                        for t in resto if t["valor"] not in ("N/D","")
                    )
                    val_fmt = f"${val_oculto:,.0f}"
                except:
                    val_fmt = f"{n} token(s)"

                st.markdown(f"""
                <div class="cs-upsell">
                    <div class="cs-upsell-icon">🔒</div>
                    <div>
                        <div class="cs-upsell-txt">+{n} tokens ocultos · {val_fmt} em gestão</div>
                        <div class="cs-upsell-sub">
                            Planos Intermediário e Profissional desbloqueiam análise completa,
                            P&L detalhado, alertas e exportação de dados
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Dust — separado visualmente com margin-top
            dust = d.get("tokens_dust", [])
            if dust:
                st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
                with st.expander(f"🔹 Tokens Dust ({len(dust)})", expanded=False):
                    dust_html = "".join(
                        f'<span style="display:inline-block;background:#FAFAFA;border:1px solid #E0E0E0;'
                        f'border-radius:5px;padding:2px 8px;font-size:0.72rem;color:#757575;margin:2px;">'
                        f'{t["simbolo"]} · {t["quantidade"]}</span>'
                        for t in dust
                    )
                    st.markdown(dust_html, unsafe_allow_html=True)

        else:
            st.info("Nenhum token significativo encontrado.")


# ── Carteira única ────
if submitted_single:
    if not carteira or not carteira.strip():
        st.warning("Introduza um endereço de carteira.")
    elif not SOLANA_RE.match(carteira.strip()):
        st.error("Endereço inválido. Verifique e tente novamente.")
    else:
        with st.spinner("A consultar a blockchain..."):
            try:
                resp = requests.get(
                    f"{API_BASE_URL}/v1/iniciante/{carteira.strip()}?moeda={moeda}",
                    timeout=40,
                )
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

# ── Múltiplas carteiras ────
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
                resp = requests.post(
                    f"{API_BASE_URL}/v1/iniciante/multi",
                    json={"carteiras": linhas, "moeda": moeda_multi},
                    timeout=60,
                )
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