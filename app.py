# ====
# app.py — CreamSol.io · Página de Entrada (Streamlit)
# ====

import streamlit as st

st.set_page_config(
    page_title="CreamSol.io",
    page_icon="🟥",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.estilo import aplicar_css
aplicar_css()

# ── CSS específico desta página ────
st.markdown("""
<style>
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 960px; }

.cs-logo-main {
    font-size: 2.2rem; font-weight: 900;
    letter-spacing: -0.03em; color: #1A1A1A; margin-bottom: 0.2rem;
}
.cs-logo-main span { color: #C62828; }
.cs-sub { font-size: 1rem; color: #757575; margin-bottom: 2rem; }

.cs-plan-card {
    background: #FFFFFF; border: 1px solid #E0E0E0;
    border-radius: 12px; padding: 1.6rem 1.8rem;
    height: 100%; transition: box-shadow 0.2s;
}
.cs-plan-card:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.08); }

.cs-plan-badge {
    display: inline-block; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    border-radius: 4px; padding: 3px 10px; margin-bottom: 0.8rem;
}
.badge-free    { background: #E8F5E9; color: #2E7D32; }
.badge-private { background: #E3F2FD; color: #1565C0; }
.badge-pro     { background: #EEEEEE; color: #212121; }

.cs-plan-title { font-size: 1.25rem; font-weight: 800; color: #1A1A1A; margin-bottom: 0.3rem; }
.cs-plan-desc  { font-size: 0.85rem; color: #616161; margin-bottom: 1rem; line-height: 1.5; }
.cs-plan-feat  { font-size: 0.82rem; color: #424242; list-style: none; padding: 0; margin: 0; }
.cs-plan-feat li { margin-bottom: 0.4rem; }
.cs-plan-feat li::before     { content: "✓  "; color: #2E7D32; font-weight: 700; }
.cs-plan-feat li.nd::before  { content: "✗  "; color: #BDBDBD; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────
with st.sidebar:
    st.markdown('<div class="cs-logo">Cream<span>Sol</span>.io</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Navegação**")
    st.page_link("app.py",                   label="🏠  Início")
    st.page_link("pages/1_Iniciante.py",      label="🟢  Iniciante")
    st.page_link("pages/2_Intermediario.py",  label="🔵  Intermediário")
    st.page_link("pages/3_Profissional.py",   label="⚫  Profissional")
    st.markdown("---")
    st.caption("v1.0.0 · creamsol.io")

# ── Header ────
st.markdown('<div class="cs-logo-main">Cream<span>Sol</span>.io</div>', unsafe_allow_html=True)
st.markdown('<div class="cs-sub">Análise patrimonial de carteiras Solana · Dados em tempo real · Sem registo de dados</div>', unsafe_allow_html=True)
st.markdown("---")

# ── Cards de plano ────
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="cs-plan-card">
        <span class="cs-plan-badge badge-free">Gratuito</span>
        <div class="cs-plan-title">Iniciante</div>
        <div class="cs-plan-desc">Visão geral da carteira sem necessidade de conta ou autenticação.</div>
        <ul class="cs-plan-feat">
            <li>Patrimônio total</li>
            <li>Saldo por token</li>
            <li>P&amp;L e custo médio</li>
            <li>Composição (Stable / Cripto)</li>
            <li>Taxas on-chain pagas</li>
            <li>Tokens dust identificados</li>
            <li>Múltiplas carteiras (até 5)</li>
            <li class="nd">Export CSV/JSON</li>
        </ul>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.page_link("pages/1_Iniciante.py", label="🟢  Aceder ao Iniciante", use_container_width=True)

with col2:
    st.markdown("""
    <div class="cs-plan-card">
        <span class="cs-plan-badge badge-private">Privado</span>
        <div class="cs-plan-title">Intermediário</div>
        <div class="cs-plan-desc">Performance detalhada com estatísticas avançadas. Acesso por senha.</div>
        <ul class="cs-plan-feat">
            <li>Tudo do Iniciante</li>
            <li>Performance por token</li>
            <li>Lucro realizado e não realizado</li>
            <li>Volume de compra / venda</li>
            <li>Slippage estimado</li>
            <li>ROI médio global</li>
            <li>Export CSV</li>
            <li class="nd">Histórico de transacções</li>
        </ul>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.page_link("pages/2_Intermediario.py", label="🔵  Aceder ao Intermediário", use_container_width=True)

with col3:
    st.markdown("""
    <div class="cs-plan-card">
        <span class="cs-plan-badge badge-pro">Profissional</span>
        <div class="cs-plan-title">Contador</div>
        <div class="cs-plan-desc">Relatório fiscal completo para contadores e utilizadores avançados. Acesso por token.</div>
        <ul class="cs-plan-feat">
            <li>Tudo do Intermediário</li>
            <li>Relatório fiscal detalhado</li>
            <li>Histórico de transacções</li>
            <li>Slippage estimado</li>
            <li>Variação 7d e 30d</li>
            <li>Custos de aquisição manuais</li>
            <li>Export CSV e JSON</li>
            <li>Total movimentado (USD)</li>
        </ul>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.page_link("pages/3_Profissional.py", label="⚫  Aceder ao Profissional", use_container_width=True)

# ── Nota de privacidade ────
st.markdown("---")
st.markdown("""
<div class="cs-aviso">
🔒 <strong>Privacidade:</strong> Nenhum endereço de carteira, custo ou dado do utilizador é armazenado, registado ou partilhado.
Todos os cálculos são realizados em memória durante o pedido e descartados imediatamente após a resposta.
CreamSol.io não constitui assessoria financeira ou fiscal.
</div>""", unsafe_allow_html=True)