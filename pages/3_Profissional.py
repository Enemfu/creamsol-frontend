# ====
# pages/3_Profissional.py — CreamSol.io · Plano Profissional (Contador)
# ====

import streamlit as st
import requests
import pandas as pd
import re
from config import API_BASE_URL, TOKEN_PROFISSIONAL

st.set_page_config(
    page_title="Profissional · CreamSol.io",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────
st.markdown("""
<style>
.stApp { background-color: #F5F5F5; }
.block-container { padding-top: 1.8rem; padding-bottom: 2rem; max-width: 1100px; }

.cs-logo { font-size: 1.5rem; font-weight: 900; letter-spacing: -0.02em; color: #1A1A1A; }
.cs-logo span { color: #C62828; }

.cs-badge {
    display: inline-block; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    background: #EEEEEE; color: #212121;
    border-radius: 4px; padding: 2px 10px;
    margin-left: 0.6rem; vertical-align: middle;
}
.cs-metric {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 10px; padding: 1rem 1.2rem;
}
.cs-metric-label {
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: #9E9E9E; margin-bottom: 0.3rem;
}
.cs-metric-valor { font-size: 1.45rem; font-weight: 800; color: #1A1A1A; line-height: 1.1; }
.cs-metric-valor.pos { color: #2E7D32; }
.cs-metric-valor.neg { color: #C62828; }
.cs-metric-valor.nd  { color: #BDBDBD; font-size: 1.05rem; font-weight: 500; }

.cs-var-card {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 10px; padding: 1rem 1.2rem;
}
.cs-var-label { font-size: 0.72rem; color: #9E9E9E; text-transform: uppercase; letter-spacing: 0.06em; }
.cs-var-valor { font-size: 1.3rem; font-weight: 800; color: #1A1A1A; }
.cs-var-valor.pos { color: #2E7D32; }
.cs-var-valor.neg { color: #C62828; }

.cs-risco-baixo  { color: #2E7D32; font-weight: 700; }
.cs-risco-medio  { color: #F57C00; font-weight: 700; }
.cs-risco-alto   { color: #C62828; font-weight: 700; }

.cs-section-title {
    font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: #9E9E9E; margin: 1.4rem 0 0.6rem 0;
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
    st.page_link("pages/1_Beginner.py",      label="🟢  Beginner")
    st.page_link("pages/2_Intermediario.py",  label="🔵  Intermediário")
    st.page_link("pages/3_Profissional.py",   label="⚫  Profissional")
    st.markdown("---")
    st.caption("v1.0.0 · creamsol.io")

# ── Header ────
st.markdown(
    '<div class="cs-logo">Cream<span>Sol</span>.io'
    '<span class="cs-badge">Profissional</span></div>',
    unsafe_allow_html=True,
)
st.caption("Relatório completo · Score de risco · NFTs · Histórico · Export CSV/JSON")
st.markdown("---")


# ════════════════════════════════════════════
# AUTENTICAÇÃO
# ════════════════════════════════════════════
if "auth_profissional" not in st.session_state:
    st.session_state["auth_profissional"] = False

if not st.session_state["auth_profissional"]:
    st.markdown("""
    <div class="cs-login-box">
        <div style="font-size:2rem; margin-bottom:0.5rem">🔐</div>
        <div style="font-size:1.1rem; font-weight:700; color:#1A1A1A; margin-bottom:0.3rem">
            Acesso Profissional
        </div>
        <div style="font-size:0.85rem; color:#757575; margin-bottom:1.2rem">
            Introduza o token de acesso fornecido pelo administrador.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_c, col_f, col_d = st.columns([1, 2, 1])
    with col_f:
        with st.form("form_token"):
            token_input = st.text_input(
                "Token", type="password",
                placeholder="••••••••••••••••",
                label_visibility="collapsed",
            )
            btn_token = st.form_submit_button("Autenticar", use_container_width=True)

        if btn_token:
            if token_input.strip() == TOKEN_PROFISSIONAL:
                st.session_state["auth_profissional"] = True
                st.rerun()
            else:
                st.error("Token inválido.")
    st.stop()


# ════════════════════════════════════════════
# ÁREA AUTENTICADA
# ════════════════════════════════════════════

with st.form("form_carteira_pro"):
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
        submitted = st.form_submit_button("🔍 Analisar", use_container_width=True)

col_sair, _ = st.columns([1, 5])
with col_sair:
    if st.button("🔓 Sair", use_container_width=True):
        st.session_state["auth_profissional"] = False
        st.rerun()


# ── Helpers ────
def _cor(valor_str: str) -> str:
    if not valor_str or str(valor_str).strip() in ("N/D", "", "—"):
        return "nd"
    try:
        v = float(
            str(valor_str)
            .replace("$","").replace("€","").replace("%","")
            .replace(",","").replace("<","").strip()
        )
        return "pos" if v > 0 else ("neg" if v < 0 else "")
    except Exception:
        return "nd"


def _metrica(label: str, valor: str):
    cor = _cor(valor)
    st.markdown(f"""
    <div class="cs-metric">
        <div class="cs-metric-label">{label}</div>
        <div class="cs-metric-valor {cor}">{valor}</div>
    </div>""", unsafe_allow_html=True)


def _variacao_card(label: str, patrimonio: str, variacao: str):
    cor = _cor(variacao)
    st.markdown(f"""
    <div class="cs-var-card">
        <div class="cs-var-label">{label}</div>
        <div class="cs-var-valor">{patrimonio}</div>
        <div class="cs-var-valor {cor}" style="font-size:1rem">{variacao}</div>
    </div>""", unsafe_allow_html=True)


def _estilo_pnl(val):
    s = str(val)
    if s in ("N/D", ""):
        return "color: #BDBDBD"
    try:
        v = float(s.replace("$","").replace("€","").replace("%","")
                   .replace(",","").replace("<","").strip())
        if v > 0: return "color: #2E7D32; font-weight:700"
        if v < 0: return "color: #C62828; font-weight:700"
    except Exception:
        pass
    return ""


def _nivel_cor(nivel: str) -> str:
    return {"baixo": "cs-risco-baixo", "medio": "cs-risco-medio", "alto": "cs-risco-alto"}.get(
        nivel.lower(), ""
    )


def _get(endpoint: str, carteira: str, moeda: str, params: dict = None) -> dict | None:
    try:
        url = f"{API_BASE_URL}/v1/profissional/{endpoint}/{carteira}"
        p = {"moeda": moeda}
        if params:
            p.update(params)
        resp = requests.get(url, params=p, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        detalhe = ""
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

    with st.spinner("A consultar a blockchain e processar relatório..."):
        relatorio = _get("relatorio", carteira, moeda)
        nfts      = _get("nfts",      carteira, moeda)
        historico = _get("historico", carteira, moeda, {"max_eventos": 100})
        risco     = _get("risco",     carteira, moeda)

    if not relatorio:
        st.stop()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Relatório",
        "📈 Tokens",
        "🛡️ Risco",
        "🕒 Histórico",
        "💾 Exportar",
    ])

    # ══ Tab 1 — Relatório ══════════════════
    with tab1:
        st.markdown('<div class="cs-section-title">Patrimônio</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4, gap="small")
        with c1: _metrica("Patrimônio Total",      relatorio["patrimonio_total"])
        with c2: _metrica("Saldo SOL",             relatorio["saldo_sol_usd"])
        with c3: _metrica("P&L Total",             relatorio["pnl_total"])
        with c4: _metrica("ROI Médio",             relatorio["roi_medio"])

        st.markdown('<div class="cs-section-title">Variação Histórica</div>', unsafe_allow_html=True)
        v1, v2, v3 = st.columns(3, gap="small")
        with v1: _variacao_card("Actual",         relatorio["patrimonio_total"],     "—")
        with v2: _variacao_card("7 dias atrás",   relatorio["patrimonio_7d_atras"],  relatorio["variacao_7d"])
        with v3: _variacao_card("30 dias atrás",  relatorio["patrimonio_30d_atras"], relatorio["variacao_30d"])

        st.markdown('<div class="cs-section-title">Custos e Taxas</div>', unsafe_allow_html=True)
        f1, f2, f3, f4 = st.columns(4, gap="small")
        with f1: _metrica("Custo Total Investido", relatorio["custo_total_investido"])
        with f2: _metrica("Taxas Pagas (USD)",     relatorio["total_taxas_usd"])
        with f3: _metrica("Taxas Pagas (SOL)",     f"{relatorio['total_taxas_sol']:.6f}")
        with f4: _metrica("Slippage Estimado",     relatorio["total_slippage_usd"])

        st.markdown('<div class="cs-section-title">Composição</div>', unsafe_allow_html=True)
        comp = relatorio["composicao"]
        cp1, cp2 = st.columns(2, gap="small")
        with cp1: _metrica(f"Stablecoins ({comp['stablecoins_pct']})", comp["stablecoins"])
        with cp2: _metrica(f"Criptomoedas ({comp['criptomoedas_pct']})", comp["criptomoedas"])

        st.markdown('<div class="cs-section-title">NFTs</div>', unsafe_allow_html=True)
        n1, n2 = st.columns(2, gap="small")
        with n1: _metrica("NFTs em carteira",    str(relatorio["n_nfts"]))
        with n2: _metrica("Valor Estimado NFTs", relatorio["valor_nfts_estimado"])

        if nfts and nfts.get("nfts"):
            with st.expander(f"🖼️ Ver NFTs ({nfts['n_nfts']})"):
                rows_nft = []
                for nft in nfts["nfts"]:
                    rows_nft.append({
                        "Nome":        nft["nome"],
                        "Colecção":    nft["collection"],
                        "Floor (USD)": nft["floor_usd"],
                        "ID":          nft["id"][:20] + "…",
                    })
                st.dataframe(pd.DataFrame(rows_nft), use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="cs-aviso">
            🕒 Timestamp: <strong>{relatorio.get("timestamp","—")}</strong> &nbsp;·&nbsp;
            Carteira: <code style="font-size:0.75rem">{carteira}</code>
        </div>""", unsafe_allow_html=True)

    # ══ Tab 2 — Tokens ══════════════════
    with tab2:
        tokens = relatorio.get("tokens", [])
        if tokens:
            st.markdown('<div class="cs-section-title">Performance por Token</div>', unsafe_allow_html=True)
            rows = []
            for t in tokens:
                rows.append({
                    "Símbolo":    t["simbolo"],
                    "Verif.":     "✅" if t["verificado"] else "⚠️",
                    "Quantidade": t["quantidade_atual"],
                    "Preço":      t["preco_atual"],
                    "Valor":      t["valor_atual"],
                    "Custo Total":t["custo_total"],
                    "Custo Médio":t["custo_medio"],
                    "P&L":        t["pnl"],
                    "ROI":        t["roi"],
                })
            df = pd.DataFrame(rows)
            styled = (
                df.style
                .map(_estilo_pnl, subset=["P&L", "ROI"])
                .set_properties(**{"font-size": "0.84rem"})
            )
            st.dataframe(styled, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum token encontrado.")

    # ══ Tab 3 — Risco ══════════════════
    with tab3:
        dados_risco = risco or relatorio  # fallback para indicadores no próprio relatório
        score = dados_risco.get("score_risco", "N/D")
        indicadores = dados_risco.get("indicadores_risco", [])

        st.markdown('<div class="cs-section-title">Score de Risco Global</div>', unsafe_allow_html=True)
        nivel_map = {"Baixo": "cs-risco-baixo", "Médio": "cs-risco-medio", "Alto": "cs-risco-alto"}
        cls_score = nivel_map.get(score, "")
        st.markdown(f'<p style="font-size:2rem; font-weight:900" class="{cls_score}">{score}</p>',
                    unsafe_allow_html=True)

        if indicadores:
            st.markdown('<div class="cs-section-title">Indicadores</div>', unsafe_allow_html=True)
            rows_risco = []
            for ind in indicadores:
                rows_risco.append({
                    "Indicador":  ind["nome"],
                    "Valor":      ind["valor"],
                    "Nível":      ind["nivel"].capitalize(),
                    "Descrição":  ind["descricao"],
                })

            def _cor_nivel(val):
                if val == "Alto":    return "color: #C62828; font-weight:700"
                if val == "Medio":   return "color: #F57C00; font-weight:700"
                if val == "Baixo":   return "color: #2E7D32; font-weight:700"
                return ""

            df_risco = pd.DataFrame(rows_risco)
            styled_r = df_risco.style.map(_cor_nivel, subset=["Nível"])
            st.dataframe(styled_r, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="cs-aviso">
            ⚠️ A análise de risco é indicativa e não substitui assessoria financeira.
            Tokens não verificados podem ser scams ou ativos sem liquidez.
        </div>""", unsafe_allow_html=True)

    # ══ Tab 4 — Histórico ══════════════════
    with tab4:
        if historico and historico.get("eventos"):
            st.markdown('<div class="cs-section-title">Resumo</div>', unsafe_allow_html=True)
            h1, h2, h3 = st.columns(3, gap="small")
            with h1: _metrica("Eventos",            str(historico["n_eventos"]))
            with h2: _metrica("Total Movimentado",  historico["total_movimentado_usd"])
            with h3: _metrica("Taxas Pagas",        historico["total_taxas_usd"])

            st.markdown('<div class="cs-section-title">Transacções</div>', unsafe_allow_html=True)
            rows_hist = []
            for ev in historico["eventos"]:
                rows_hist.append({
                    "Data":       ev["timestamp"],
                    "Tipo":       ev["tipo"],
                    "Descrição":  ev["descricao"],
                    "Valor":      ev["valor_usd"],
                    "Assinatura": ev["signature"],
                })
            st.dataframe(pd.DataFrame(rows_hist), use_container_width=True, hide_index=True)
        else:
            st.info("Sem histórico de transacções disponível.")

    # ══ Tab 5 — Exportar ══════════════════
    with tab5:
        st.markdown('<div class="cs-section-title">Exportar Relatório</div>', unsafe_allow_html=True)
        col_j, col_c, _ = st.columns([1, 1, 2], gap="small")

        with col_j:
            if st.button("⬇️ Download JSON", use_container_width=True):
                try:
                    url = f"{API_BASE_URL}/v1/profissional/export/{carteira}"
                    r = requests.get(url, params={"formato": "json", "moeda": moeda}, timeout=60)
                    r.raise_for_status()
                    st.download_button(
                        label="💾 Guardar JSON",
                        data=r.text,
                        file_name=f"creamsol_pro_{carteira[:8]}.json",
                        mime="application/json",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Erro ao gerar JSON: {e}")

        with col_c:
            if st.button("⬇️ Download CSV", use_container_width=True):
                try:
                    url = f"{API_BASE_URL}/v1/profissional/export/{carteira}"
                    r = requests.get(url, params={"formato": "csv", "moeda": moeda}, timeout=60)
                    r.raise_for_status()
                    st.download_button(
                        label="💾 Guardar CSV",
                        data=r.content,
                        file_name=f"creamsol_pro_{carteira[:8]}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Erro ao gerar CSV: {e}")

        st.markdown("""
        <div class="cs-aviso">
            🔒 O relatório exportado contém apenas dados públicos on-chain associados ao endereço fornecido.
            Nenhum dado é retido no servidor após a resposta.
        </div>""", unsafe_allow_html=True)