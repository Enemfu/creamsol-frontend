# ====
# app.py — CreamSol.io · Página de Entrada (Streamlit)
# ====

import streamlit as st

st.set_page_config(
    page_title="CreamSol.io",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS Global ────
st.markdown("""
<style>
/* Fundo */
.stApp { background-color: #F5F5F5; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 960px; }

/* Logo */
.cs-logo {
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    color: #1A1A1A;
    margin-bottom: 0.2rem;
}
.cs-logo span { color: #2E7D32; }

/* Subtítulo */
.cs-sub {
    font-size: 1rem;
    color: #757575;
    margin-bottom: 2rem;
}

/* Cartão de plano */
.cs-plan-card {
    background: #FFFF;
    border: 1px solid #E0E0E0;
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    height: 100%;
    transition: box-shadow 0.2s;
}
.cs-plan-card:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.08); }

.cs-plan-badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 4px;
    padding: 3px 10px;
    margin-bottom: 0.8rem;
}
.badge-free    { background: #E8F5E9; color: #2E7D32; }
.badge-private { background: #E3F2FD; color: #1565C0; }
.badge-pro     { background: #EEEE; color: #212121; }

.cs-plan-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #1A1A1A;
    margin-bottom: 0.3rem;
}
.cs-plan-desc {
    font-size: 0.85rem;
    color: #616161;
    margin-bottom: 1rem;
    line-height: 1.5;
}
.cs-plan-feat {
    font-size: 0.82rem;
    color: #424242;
    list-style: none;
    padding: 0;
    margin: 0;
}
.cs-plan-feat li { margin-bottom: 0.4rem; }
.cs-plan-feat li::before { content: "✓  "; color: #2E7D32; font-weight: 700; }
.cs-plan-feat li.nd::before { content: "✗  "; color: #BDBDBD; }

/* Divisor */
hr { border-color: #E0E0E0; margin: 1.5rem 0; }

/* Aviso legal rodapé */
.cs-aviso {
    background: #FAFAFA;
    border-left: 3px solid #BDBDBD;
    padding: 0.6rem 1rem;
    color: #9E9E9E;
    font-size: 0.76rem;
    border-radius: 0 6px 6px 0;
    margin-top: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFFF;
    border-right: 1px solid #E0E0E0;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────
with st.sidebar:
    st.markdown('<div class="cs-logo" style="font-size:1.4rem">Cream<span>Sol</span>.io</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Navigation**")
    st.page_link("app.py",                   label="🏠  Home",             icon=None)
    st.page_link("pages/1_Iniciante.py",      label="🟢  Beginner",         icon=None)
    st.page_link("pages/2_Intermediario.py",  label="🔵  Intermediate",     icon=None)
    st.page_link("pages/3_Profissional.py",   label="⚫  Professional",     icon=None)
    st.markdown("---")
    st.caption("v1.0.0 · creamsol.io")

# ── Header ────
st.markdown('<div class="cs-logo">Cream<span>Sol</span>.io</div>', unsafe_allow_html=True)
st.markdown('<div class="cs-sub">Solana wallet analysis · Real-time data · No data stored</div>', unsafe_allow_html=True)
st.markdown("---")

# ── Cards de plano ────
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="cs-plan-card">
        <span class="cs-plan-badge badge-free">Free</span>
        <div class="cs-plan-title">Beginner</div>
        <div class="cs-plan-desc">
            Wallet overview with no account or authentication required.
        </div>
        <ul class="cs-plan-feat">
            <li>Total portfolio value</li>
            <li>Balance per token</li>
            <li>P&amp;L and average cost</li>
            <li>Composition (Stables / Crypto)</li>
            <li>Dust tokens identified</li>
            <li>Multiple wallets (up to 3)</li>
            <li class="nd">Full report</li>
            <li class="nd">CSV / JSON export</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.page_link("pages/1_Iniciante.py", label="🟢  Go to Beginner", use_container_width=True)

with col2:
    st.markdown("""
    <div class="cs-plan-card">
        <span class="cs-plan-badge badge-private">Private</span>
        <div class="cs-plan-title">Intermediate</div>
        <div class="cs-plan-desc">
            Detailed performance with advanced statistics. Password protected.
        </div>
        <ul class="cs-plan-feat">
            <li>Everything in Beginner</li>
            <li>Performance per token</li>
            <li>Realised and unrealised profit</li>
            <li>Buy / sell volume</li>
            <li>Fees paid (SOL/USD)</li>
            <li>Global average ROI</li>
            <li>CSV export</li>
            <li class="nd">Transaction history</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.page_link("pages/2_Intermediario.py", label="🔵  Go to Intermediate", use_container_width=True)

with col3:
    st.markdown("""
    <div class="cs-plan-card">
        <span class="cs-plan-badge badge-pro">Profissional</span>
        <div class="cs-plan-title">Contador</div>
        <div class="cs-plan-desc">
            Relatório fiscal completo para contadores e utilizadores avançados. Acesso por token.
        </div>
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
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.page_link("pages/3_Profissional.py", label="⚫  Aceder ao Profissional", use_container_width=True)

# ── Nota de privacidade ────
st.markdown("---")
st.markdown("""
<div class="cs-aviso">
🔒 <strong>Privacidade:</strong> Nenhum endereço de carteira, custo ou dado do utilizador é armazenado, registado ou partilhado.
Todos os cálculos são realizados em memória durante o pedido e descartados imediatamente após a resposta.
CreamSol.io não constitui assessoria financeira ou fiscal.
</div>
""", unsafe_allow_html=True)