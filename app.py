import streamlit as st
import pandas as pd
from pathlib import Path
import hashlib
import base64

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Grupo LLE — Orçamentos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Cores da identidade Grupo LLE ──────────────────────────────────────────
AMARELO  = "#FAC319"
VERDE    = "#0F8C3B"
AZUL     = "#007FE0"
AZUL_ESC = "#041747"

# ─── Logo ────────────────────────────────────────────────────────────────────
def get_logo_b64():
    p = Path(__file__).parent / "logo.png"
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None

LOGO_B64 = get_logo_b64()

def logo_img(height=38):
    if LOGO_B64:
        return f'<img src="data:image/png;base64,{LOGO_B64}" style="height:{height}px;" />'
    return f'<span style="color:#fff;font-weight:700;font-size:18px;">GRUPO LLE</span>'

def page_header(titulo, subtitulo=""):
    st.markdown(
        f'<div class="hbar">{logo_img(38)}'
        f'<div><div class="hbar-title">{titulo}</div>'
        f'{"<div class=hbar-sub>" + subtitulo + "</div>" if subtitulo else ""}</div></div>',
        unsafe_allow_html=True,
    )

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Global ── */
html, body, [data-testid="stAppViewContainer"] {{
    background: #f4f7fc !important;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    color: #1a1a2e !important;
}}
[data-testid="stHeader"] {{ display:none !important; }}
[data-testid="stToolbar"] {{ display:none !important; }}
#MainMenu {{ visibility:hidden; }}
footer {{ visibility:hidden; }}
.block-container {{ padding: 1.5rem 2.5rem !important; max-width: 1300px !important; }}

/* ── Tipografia ── */
h1, h2, h3 {{ color: {AZUL_ESC} !important; font-weight: 700 !important; }}

/* ── Header bar ── */
.hbar {{
    background: {AZUL_ESC};
    padding: 14px 22px;
    border-radius: 12px;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 18px;
}}
.hbar-title {{ color: #fff; font-size: 20px; font-weight: 700; }}
.hbar-sub   {{ color: {AMARELO}; font-size: 12px; margin-top: 2px; }}

/* ── Login card ── */
.login-outer {{
    max-width: 420px;
    margin: 6vh auto 0;
}}
.login-top {{
    background: {AZUL_ESC};
    padding: 32px 28px 24px;
    border-radius: 14px 14px 0 0;
    text-align: center;
}}
.login-body {{
    background: #fff;
    border: 1px solid #dde3ef;
    border-top: none;
    border-radius: 0 0 14px 14px;
    padding: 24px 28px 30px;
}}
.login-sub {{
    text-align: center;
    color: #666;
    font-size: 13px;
    margin: 0 0 18px;
}}

/* ── Cadastro card ── */
.cadastro-body {{
    max-width: 540px;
    margin: 4vh auto 0;
    background: #fff;
    border: 1px solid #dde3ef;
    border-radius: 14px;
    padding: 30px 32px 34px;
}}
.cadastro-logo {{
    text-align: center;
    margin-bottom: 18px;
}}

/* ── Info / steps box ── */
.info-box {{
    background: #edf4ff;
    border: 1px solid #b3d0f5;
    border-left: 4px solid {AZUL};
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 13.5px;
    color: #1a2e50;
    line-height: 1.8;
    margin-bottom: 20px;
}}
.steps-box {{
    background: #fafbfd;
    border: 1px solid #dde3ef;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 13px;
    color: #555;
    line-height: 2;
    margin-top: 10px;
}}
.steps-box code {{
    background: #f0f2f8;
    padding: 2px 6px;
    border-radius: 4px;
    color: {AZUL_ESC};
    font-size: .85rem;
}}

/* ── Botões ── */
[data-testid="baseButton-primary"] {{
    background: {AZUL_ESC} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}}
[data-testid="baseButton-primary"]:hover {{
    background: {AZUL} !important;
}}
[data-testid="baseButton-secondary"] {{
    background: #fff !important;
    color: {AZUL_ESC} !important;
    border: 1.5px solid {AZUL_ESC} !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}}

/* ── Inputs ── */
input[type="text"], input[type="password"], input[type="number"] {{
    background: #fff !important;
    border: 1.5px solid #d0d8ea !important;
    border-radius: 7px !important;
    color: #1a1a2e !important;
}}
input:focus {{
    border-color: {AZUL} !important;
    box-shadow: 0 0 0 3px rgba(0,127,224,.12) !important;
}}

/* ── Métricas ── */
[data-testid="metric-container"] {{
    background: #fff;
    border-radius: 10px;
    padding: 14px 18px;
    border-left: 4px solid {AMARELO};
    box-shadow: 0 1px 4px rgba(4,23,71,.07);
}}
[data-testid="stMetricLabel"] {{ color: #666 !important; font-size: .8rem !important; }}
[data-testid="stMetricValue"] {{ color: {AZUL_ESC} !important; font-weight: 700 !important; }}

/* ── Radio (tabela) ── */
[data-testid="stRadio"] label {{
    background: #fff;
    border: 1.5px solid #d0d8ea;
    border-radius: 7px;
    padding: 6px 18px !important;
    color: #555 !important;
    font-weight: 500;
    cursor: pointer;
    transition: all .15s;
}}
[data-testid="stRadio"] label:has(input:checked) {{
    border-color: {AMARELO};
    background: #fffbec;
    color: {AZUL_ESC} !important;
    font-weight: 700;
}}

/* ── Item card ── */
.item-card {{
    background: #fff;
    border: 1px solid #dde3ef;
    border-left: 4px solid {AMARELO};
    border-radius: 10px;
    padding: .9rem 1.2rem;
    margin-bottom: .6rem;
    box-shadow: 0 1px 3px rgba(4,23,71,.05);
}}

/* ── Expander ── */
[data-testid="stExpander"] {{
    border: 1px solid #dde3ef !important;
    border-radius: 9px !important;
    background: #fff !important;
}}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {{
    border: 1px solid #dde3ef !important;
    border-radius: 9px !important;
}}

/* ── Alertas de alçada ── */
.alcada-ok   {{ background:#edf7f1; color:#0a5c31; padding:10px 14px; border-radius:8px; font-size:13px; border-left:4px solid {VERDE}; }}
.alcada-warn {{ background:#fef9e7; color:#7d5c00; padding:10px 14px; border-radius:8px; font-size:13px; border-left:4px solid {AMARELO}; }}
.alcada-err  {{ background:#fdf0f0; color:#8b1a1a; padding:10px 14px; border-radius:8px; font-size:13px; border-left:4px solid #dc3545; }}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {{
    background: #fff !important;
    border: 1.5px solid #d0d8ea !important;
    border-radius: 7px !important;
    color: #1a1a2e !important;
}}

/* ── Section title ── */
.section-title {{
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: {AZUL_ESC} !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 1.5rem 0 .75rem !important;
    border-bottom: 2px solid {AMARELO};
    padding-bottom: 6px;
    display: inline-block;
}}

/* ── Usuario tag ── */
.usuario-tag {{
    color: #666;
    font-size: .85rem;
    margin: 0;
    padding-top: .5rem;
    text-align: right;
}}

/* ── Divider ── */
hr {{ border-color: #dde3ef !important; }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  AUTH HELPERS
# ═══════════════════════════════════════════════════════════════════════════
def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def check_credentials(user: str, pw: str) -> bool:
    try:
        users = st.secrets.get("users", {})
    except Exception:
        users = {}
    return users.get(user.strip(), "") == hash_password(pw)

def has_any_user_configured() -> bool:
    try:
        return bool(st.secrets.get("users", {}))
    except Exception:
        return False

# ═══════════════════════════════════════════════════════════════════════════
#  SESSION DEFAULTS
# ═══════════════════════════════════════════════════════════════════════════
def init_session():
    defaults = {
        "logged_in":          False,
        "pagina":             "login",
        "usuario_logado":     "",
        "tabela":             None,
        "df_tabela":          None,
        "itens_orcamento":    [],
        "desconto_geral_pct": 0.0,
        "desconto_geral_rs":  0.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ═══════════════════════════════════════════════════════════════════════════
#  PÁGINA DE CADASTRO — GERADOR DE HASH
# ═══════════════════════════════════════════════════════════════════════════
def cadastro_page():
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown('<div class="cadastro-body">', unsafe_allow_html=True)
        if LOGO_B64:
            st.markdown(
                f'<div class="cadastro-logo">'
                f'<img src="data:image/png;base64,{LOGO_B64}" style="max-width:180px;width:100%;background:{AZUL_ESC};padding:12px 18px;border-radius:8px;" />'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown(f'<h3 style="color:{AZUL_ESC};margin:0 0 4px;">Criar credencial de acesso</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color:#666;font-size:13px;margin-bottom:20px;">Sistema de Orçamentos — Grupo LLE</p>', unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
            <b>Como funciona em 3 passos:</b><br>
            <b>1.</b> Preencha usuário e senha abaixo e clique em <b>Gerar Hash</b><br>
            <b>2.</b> Copie o bloco <code>toml</code> gerado<br>
            <b>3.</b> No Streamlit Cloud → seu app → <b>⚙️ Settings → Secrets</b> → cole e salve
        </div>
        """, unsafe_allow_html=True)

        with st.form("cadastro_form"):
            novo_user  = st.text_input("Nome de usuário", placeholder="ex: joao_vendas")
            nova_senha = st.text_input("Senha", type="password", placeholder="mínimo 6 caracteres")
            confirma   = st.text_input("Confirmar senha", type="password", placeholder="repita a senha")
            gerar      = st.form_submit_button("🔑 Gerar Hash", type="primary", use_container_width=True)

        if gerar:
            erros = []
            if not novo_user.strip():         erros.append("Informe um nome de usuário.")
            if len(nova_senha) < 6:           erros.append("A senha precisa ter pelo menos 6 caracteres.")
            if nova_senha != confirma:        erros.append("As senhas não coincidem.")
            if erros:
                for e in erros: st.error(e)
            else:
                h = hash_password(nova_senha)
                st.success("✅ Hash gerado com sucesso!")
                st.markdown("##### Cole isso nos Secrets do Streamlit Cloud:")
                st.code(f'[users]\n{novo_user.strip()} = "{h}"', language="toml")
                st.markdown("""
                <div class="steps-box">
                    <b>Para múltiplos usuários</b>, acumule no mesmo bloco:<br>
                    <code>[users]<br>joao = "hash_joao"<br>maria = "hash_maria"</code>
                </div>
                """, unsafe_allow_html=True)
                st.info("🔒 O hash é calculado só no seu navegador. A senha nunca é armazenada.", icon="🔒")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Voltar para login", use_container_width=True):
            st.session_state.pagina = "login"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  PÁGINA DE LOGIN
# ═══════════════════════════════════════════════════════════════════════════
def login_page():
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("<br>", unsafe_allow_html=True)
        # Topo azul com logo
        if LOGO_B64:
            st.markdown(
                f'<div class="login-top">'
                f'<img src="data:image/png;base64,{LOGO_B64}" style="max-width:210px;width:100%;" />'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="login-top"><span style="color:#fff;font-size:22px;font-weight:700;">GRUPO LLE</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="login-body">', unsafe_allow_html=True)
        st.markdown('<p class="login-sub">Sistema de Orçamentos</p>', unsafe_allow_html=True)

        if not has_any_user_configured():
            st.warning("Nenhum usuário configurado ainda. Crie sua credencial primeiro.")

        with st.form("login_form"):
            user = st.text_input("Usuário", placeholder="seu usuário")
            pw   = st.text_input("Senha", type="password", placeholder="••••••••")
            btn  = st.form_submit_button("Entrar →", type="primary", use_container_width=True)

        if btn:
            if not has_any_user_configured():
                st.error("Nenhum usuário nos Secrets. Clique em 'Criar credencial' abaixo.")
            elif check_credentials(user, pw):
                st.session_state.logged_in      = True
                st.session_state.usuario_logado = user.strip()
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Criar credencial / Gerar hash", use_container_width=True):
            st.session_state.pagina = "cadastro"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  HELPERS DE TABELA
# ═══════════════════════════════════════════════════════════════════════════
TABELA_FILES = {
    "King": "tabelas/tabela_king.xlsx",
    "Pisa": "tabelas/tabela_pisa.xlsx",
}

REQUIRED_COLS = {
    "codigo":      ["codigo", "cod", "code", "sku"],
    "descricao":   ["descricao", "produto", "description", "nome", "item"],
    "marca":       ["marca", "brand", "fabricante"],
    "custo":       ["custo", "preco_custo", "cost", "valor_custo", "preco custo"],
    "preco_venda": ["preco_venda", "preco", "venda", "price", "valor_venda", "preco venda"],
}

def normalize_col(df: pd.DataFrame) -> pd.DataFrame:
    rename = {}
    cols_lower = {c.lower().strip().replace(" ", "_"): c for c in df.columns}
    for std, aliases in REQUIRED_COLS.items():
        for alias in aliases:
            if alias in cols_lower:
                rename[cols_lower[alias]] = std
                break
    return df.rename(columns=rename)

def load_tabela(tabela: str):
    path = TABELA_FILES.get(tabela)
    if not path or not Path(path).exists():
        return None
    df = pd.read_excel(path, dtype=str)
    df = normalize_col(df)
    for col in ["custo", "preco_venda"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .str.replace(r"[R$\s]", "", regex=True)
                .str.replace(",", ".", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def calcular_margem(custo: float, preco: float) -> float:
    if preco and preco > 0:
        return (preco - custo) / preco * 100
    return 0.0

def brl(v):
    return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")

# ═══════════════════════════════════════════════════════════════════════════
#  APP PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════
def main_app():
    # ── Header ──────────────────────────────────────────────────────────────
    col_tabela_sel, col_user, col_logout = st.columns([6, 2, 1])
    with col_tabela_sel:
        page_header("Sistema de Orçamentos", "Grupo LLE")
    with col_user:
        st.markdown(
            f'<p class="usuario-tag">👤 {st.session_state.usuario_logado}</p>',
            unsafe_allow_html=True,
        )
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sair", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    # Seleção de tabela
    tabela_escolha = st.radio(
        "Tabela de preços",
        ["King", "Pisa"],
        horizontal=True,
        key="tabela_radio",
    )
    if tabela_escolha != st.session_state.tabela:
        st.session_state.tabela          = tabela_escolha
        st.session_state.df_tabela       = load_tabela(tabela_escolha)
        st.session_state.itens_orcamento = []

    st.markdown("---")
    df = st.session_state.df_tabela

    # ── Upload se tabela não existir ─────────────────────────────────────────
    if df is None:
        tabela_atual = st.session_state.tabela or "King"
        st.warning(f"Tabela **{tabela_atual}** não encontrada. Faça o upload abaixo.")
        uploaded = st.file_uploader(
            f"Upload tabela {tabela_atual} (.xlsx)",
            type=["xlsx"],
            key="upload_tabela",
        )
        if uploaded:
            Path("tabelas").mkdir(exist_ok=True)
            dest = TABELA_FILES[tabela_atual]
            with open(dest, "wb") as fh:
                fh.write(uploaded.read())
            st.session_state.df_tabela = load_tabela(tabela_atual)
            st.success("Tabela carregada com sucesso!")
            st.rerun()
        return

    # ── Busca de produto ──────────────────────────────────────────────────────
    st.markdown('<span class="section-title">🔍 Adicionar Produto</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([3, 2, 1])
    with c1:
        busca = st.text_input("Código ou nome do produto", placeholder="Ex: 1234 ou Parafuso...")
    with c2:
        marcas = (
            ["Todas"] + sorted(df["marca"].dropna().unique().tolist())
            if "marca" in df.columns else ["Todas"]
        )
        marca_filtro = st.selectbox("Filtrar por marca", marcas)
    with c3:
        qtd = st.number_input("Quantidade", min_value=1, value=1, step=1)

    df_filtrado = df.copy()
    if marca_filtro != "Todas" and "marca" in df.columns:
        df_filtrado = df_filtrado[df_filtrado["marca"] == marca_filtro]
    if busca:
        mask = pd.Series([False] * len(df_filtrado), index=df_filtrado.index)
        for col in ["codigo", "descricao"]:
            if col in df_filtrado.columns:
                mask |= df_filtrado[col].astype(str).str.lower().str.contains(busca.lower(), na=False)
        df_filtrado = df_filtrado[mask]

    if busca or marca_filtro != "Todas":
        if df_filtrado.empty:
            st.info("Nenhum produto encontrado.")
        else:
            cols_show = [c for c in ["codigo", "descricao", "marca"] if c in df_filtrado.columns]
            st.dataframe(
                df_filtrado[cols_show].head(20).reset_index(drop=True),
                use_container_width=True,
                hide_index=True,
            )
            cod_options = df_filtrado["codigo"].astype(str).tolist() if "codigo" in df_filtrado.columns else []
            cod_sel = st.selectbox("Selecionar produto pelo código", options=cod_options, key="cod_sel")

            if st.button("➕ Adicionar ao orçamento", type="primary", key="add_btn"):
                row = df_filtrado[df_filtrado["codigo"].astype(str) == cod_sel].iloc[0]
                item = {
                    "codigo":        str(row.get("codigo", "")),
                    "descricao":     str(row.get("descricao", "")),
                    "marca":         str(row.get("marca", "")) if "marca" in row else "",
                    "custo_unit":    float(row.get("custo", 0) or 0),
                    "preco_unit":    float(row.get("preco_venda", 0) or 0),
                    "qtd":           int(qtd),
                    "desc_item_pct": 0.0,
                    "desc_item_rs":  0.0,
                }
                st.session_state.itens_orcamento.append(item)
                st.success(f"✅ '{item['descricao']}' adicionado!")
                st.rerun()

    # ── Orçamento ────────────────────────────────────────────────────────────
    st.markdown('<span class="section-title">🧾 Orçamento</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    itens = st.session_state.itens_orcamento
    if not itens:
        st.info("Nenhum item adicionado ainda.")
        return

    # Desconto geral
    with st.expander("💸 Desconto Geral (aplica em todos os itens)"):
        dg1, dg2 = st.columns(2)
        with dg1:
            st.session_state.desconto_geral_pct = st.number_input(
                "Desconto geral (%)", min_value=0.0, max_value=100.0,
                value=float(st.session_state.desconto_geral_pct), step=0.5, format="%.2f",
            )
        with dg2:
            st.session_state.desconto_geral_rs = st.number_input(
                "Desconto geral (R$)", min_value=0.0,
                value=float(st.session_state.desconto_geral_rs), step=1.0, format="%.2f",
            )

    dg_pct = float(st.session_state.desconto_geral_pct)
    dg_rs  = float(st.session_state.desconto_geral_rs)

    to_remove            = []
    total_custo          = 0.0
    total_venda_original = 0.0
    total_venda_final    = 0.0

    for i, item in enumerate(itens):
        with st.container():
            st.markdown('<div class="item-card">', unsafe_allow_html=True)
            ca, cb, cc, cd, ce, cf = st.columns([3, 1, 2, 2, 2, 0.5])

            with ca:
                st.markdown(f"**{item['descricao']}**")
                st.caption(f"Cód: {item['codigo']}  ·  {item['marca']}")
            with cb:
                item["qtd"] = st.number_input(
                    "Qtd", min_value=1, value=item["qtd"],
                    key=f"qtd_{i}", label_visibility="collapsed",
                )
            with cc:
                item["desc_item_pct"] = st.number_input(
                    "Desc %", min_value=0.0, max_value=100.0,
                    value=float(item["desc_item_pct"]), step=0.5, format="%.2f",
                    key=f"dpct_{i}", label_visibility="collapsed",
                )
            with cd:
                item["desc_item_rs"] = st.number_input(
                    "Desc R$", min_value=0.0,
                    value=float(item["desc_item_rs"]), step=0.5, format="%.2f",
                    key=f"drs_{i}", label_visibility="collapsed",
                )
            with ce:
                custo_total = item["custo_unit"] * item["qtd"]
                preco_orig  = item["preco_unit"] * item["qtd"]

                d_pct = item["desc_item_pct"]
                d_rs  = item["desc_item_rs"]
                if d_pct > 0:
                    preco_apos_item = preco_orig * (1 - d_pct / 100)
                elif d_rs > 0:
                    preco_apos_item = max(0.0, preco_orig - d_rs)
                else:
                    preco_apos_item = preco_orig

                preco_final  = preco_apos_item * (1 - dg_pct / 100) if dg_pct > 0 else preco_apos_item
                margem_orig  = calcular_margem(custo_total, preco_orig)
                margem_final = calcular_margem(custo_total, preco_final)

                st.metric(
                    label="Margem item",
                    value=f"{margem_final:.1f}%",
                    delta=f"{margem_final - margem_orig:+.1f}%",
                    delta_color="normal" if margem_final >= margem_orig else "inverse",
                )

                total_custo          += custo_total
                total_venda_original += preco_orig
                total_venda_final    += preco_final

            with cf:
                if st.button("🗑️", key=f"del_{i}"):
                    to_remove.append(i)

            st.markdown('</div>', unsafe_allow_html=True)

    for i in reversed(to_remove):
        st.session_state.itens_orcamento.pop(i)
    if to_remove:
        st.rerun()

    if dg_pct == 0 and dg_rs > 0:
        total_venda_final = max(0.0, total_venda_final - dg_rs)

    # ── Resumo ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<span class="section-title">📊 Resumo do Pedido</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    margem_orig_geral  = calcular_margem(total_custo, total_venda_original)
    margem_final_geral = calcular_margem(total_custo, total_venda_final)

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric("Total tabela", brl(total_venda_original))
    with r2:
        st.metric(
            "Total com descontos",
            brl(total_venda_final),
            delta=f"R$ {total_venda_final - total_venda_original:,.2f}".replace(",","X").replace(".",",").replace("X","."),
            delta_color="inverse",
        )
    with r3:
        st.metric("Margem tabela", f"{margem_orig_geral:.1f}%")
    with r4:
        st.metric(
            "Margem final",
            f"{margem_final_geral:.1f}%",
            delta=f"{margem_final_geral - margem_orig_geral:+.1f}%",
            delta_color="normal" if margem_final_geral >= margem_orig_geral else "inverse",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if margem_final_geral < 10:
        st.markdown('<div class="alcada-err">🚨 <b>Margem abaixo de 10%!</b> Revise os descontos antes de enviar o orçamento.</div>', unsafe_allow_html=True)
    elif margem_final_geral < 20:
        st.markdown('<div class="alcada-warn">⚠️ <b>Margem abaixo de 20%.</b> Atenção antes de fechar o pedido.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alcada-ok">✅ <b>Margem saudável.</b> Orçamento dentro dos parâmetros.</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Limpar orçamento completo"):
        st.session_state.itens_orcamento    = []
        st.session_state.desconto_geral_pct = 0.0
        st.session_state.desconto_geral_rs  = 0.0
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
#  ROTEADOR
# ═══════════════════════════════════════════════════════════════════════════
if st.session_state.logged_in:
    main_app()
elif st.session_state.pagina == "cadastro":
    cadastro_page()
else:
    login_page()
