import streamlit as st
import pandas as pd
from pathlib import Path
import hashlib
import base64

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OrçaPro — Grupo LLE",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Cores Grupo LLE ─────────────────────────────────────────────────────────
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
html, body, [data-testid="stAppViewContainer"] {{
    background: #f4f7fc !important;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    color: #1a1a2e !important;
}}
[data-testid="stHeader"]  {{ display:none !important; }}
[data-testid="stToolbar"] {{ display:none !important; }}
#MainMenu {{ visibility:hidden; }}
footer    {{ visibility:hidden; }}
.block-container {{ padding: 1.5rem 2.5rem !important; max-width: 1300px !important; }}
h1, h2, h3 {{ color: {AZUL_ESC} !important; font-weight: 700 !important; }}

.hbar {{
    background: {AZUL_ESC}; padding: 14px 22px; border-radius: 12px;
    margin-bottom: 22px; display: flex; align-items: center; gap: 18px;
}}
.hbar-title {{ color: #fff; font-size: 20px; font-weight: 700; }}
.hbar-sub   {{ color: {AMARELO}; font-size: 12px; margin-top: 2px; }}

.login-top {{
    background: {AZUL_ESC}; padding: 32px 28px 24px;
    border-radius: 14px 14px 0 0; text-align: center;
}}
.login-body {{
    background: #fff; border: 1px solid #dde3ef; border-top: none;
    border-radius: 0 0 14px 14px; padding: 24px 28px 30px;
}}
.login-sub {{ text-align:center; color:#666; font-size:13px; margin:0 0 18px; }}

.cadastro-body {{
    max-width: 540px; margin: 4vh auto 0; background: #fff;
    border: 1px solid #dde3ef; border-radius: 14px; padding: 30px 32px 34px;
}}
.cadastro-logo {{ text-align:center; margin-bottom:18px; }}

.info-box {{
    background: #edf4ff; border: 1px solid #b3d0f5;
    border-left: 4px solid {AZUL}; border-radius: 8px;
    padding: 12px 16px; font-size: 13.5px; color: #1a2e50;
    line-height: 1.8; margin-bottom: 20px;
}}
.steps-box {{
    background: #fafbfd; border: 1px solid #dde3ef; border-radius: 8px;
    padding: 12px 16px; font-size: 13px; color: #555;
    line-height: 2; margin-top: 10px;
}}
.steps-box code {{
    background: #f0f2f8; padding: 2px 6px; border-radius: 4px;
    color: {AZUL_ESC}; font-size: .85rem;
}}

[data-testid="baseButton-primary"] {{
    background: {AZUL_ESC} !important; color: #fff !important;
    border: none !important; border-radius: 8px !important; font-weight: 600 !important;
}}
[data-testid="baseButton-primary"]:hover {{ background: {AZUL} !important; }}
[data-testid="baseButton-secondary"] {{
    background: #fff !important; color: {AZUL_ESC} !important;
    border: 1.5px solid {AZUL_ESC} !important; border-radius: 8px !important;
}}

input[type="text"], input[type="password"], input[type="number"] {{
    background: #fff !important; border: 1.5px solid #d0d8ea !important;
    border-radius: 7px !important; color: #1a1a2e !important;
}}
input:focus {{
    border-color: {AZUL} !important;
    box-shadow: 0 0 0 3px rgba(0,127,224,.12) !important;
}}

[data-testid="metric-container"] {{
    background: #fff; border-radius: 10px; padding: 14px 18px;
    border-left: 4px solid {AMARELO};
    box-shadow: 0 1px 4px rgba(4,23,71,.07);
}}
[data-testid="stMetricLabel"] {{ color: #666 !important; font-size: .8rem !important; }}
[data-testid="stMetricValue"] {{ color: {AZUL_ESC} !important; font-weight: 700 !important; }}

[data-testid="stRadio"] label {{
    background: #fff; border: 1.5px solid #d0d8ea; border-radius: 7px;
    padding: 6px 18px !important; color: #555 !important;
    font-weight: 500; cursor: pointer; transition: all .15s;
}}
[data-testid="stRadio"] label:has(input:checked) {{
    border-color: {AMARELO}; background: #fffbec;
    color: {AZUL_ESC} !important; font-weight: 700;
}}

.item-card {{
    background: #fff; border: 1px solid #dde3ef;
    border-left: 4px solid {AMARELO}; border-radius: 10px;
    padding: .9rem 1.2rem; margin-bottom: .6rem;
    box-shadow: 0 1px 3px rgba(4,23,71,.05);
}}

[data-testid="stExpander"] {{
    border: 1px solid #dde3ef !important; border-radius: 9px !important;
    background: #fff !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid #dde3ef !important; border-radius: 9px !important;
}}

.alcada-ok   {{ background:#edf7f1; color:#0a5c31; padding:10px 14px; border-radius:8px; font-size:13px; border-left:4px solid {VERDE}; }}
.alcada-warn {{ background:#fef9e7; color:#7d5c00; padding:10px 14px; border-radius:8px; font-size:13px; border-left:4px solid {AMARELO}; }}
.alcada-err  {{ background:#fdf0f0; color:#8b1a1a; padding:10px 14px; border-radius:8px; font-size:13px; border-left:4px solid #dc3545; }}

[data-testid="stSelectbox"] > div > div {{
    background: #fff !important; border: 1.5px solid #d0d8ea !important;
    border-radius: 7px !important; color: #1a1a2e !important;
}}

.section-title {{
    font-size: 1rem !important; font-weight: 700 !important;
    color: {AZUL_ESC} !important; text-transform: uppercase;
    letter-spacing: 1px; margin: 1.5rem 0 .75rem !important;
    border-bottom: 2px solid {AMARELO}; padding-bottom: 6px;
    display: inline-block;
}}
.usuario-tag {{
    color: #666; font-size: .85rem; margin: 0;
    padding-top: .5rem; text-align: right;
}}
hr {{ border-color: #dde3ef !important; }}

/* ── Item row (compact) ── */
.item-row {{
    background: #fff;
    border: 1px solid #dde3ef;
    border-left: 4px solid #FAC319;
    border-radius: 8px;
    padding: .45rem .9rem;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
}}
.item-row:hover {{ border-left-color: #007FE0; background: #fafbfd; }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  AUTH
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
#  SESSION
# ═══════════════════════════════════════════════════════════════════════════
def init_session():
    defaults = {
        "logged_in":          False,
        "pagina":             "login",
        "usuario_logado":     "",
        "tabela":             None,
        "df_mapao":           None,
        "mapao_path":         None,   # ← caminho do arquivo salvo (sem global)
        "itens_orcamento":    [],
        "desconto_geral_pct": 0.0,
        "desconto_geral_pct": 0.0,
        "acrescimo_geral_pct": 0.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ═══════════════════════════════════════════════════════════════════════════
#  LEITURA DO MAPÃO
# ═══════════════════════════════════════════════════════════════════════════
COL_MAP = {
    "MAP_CODPROD":    "codigo",
    "MAP_DESCRPROD":  "descricao",
    "MAP_MARCA":      "marca",
    "MAP_CUSTOMED":   "custo",
    "MAP_ULTCUSTO":   "custo_ult",
    "MAP_PRECOVENDA": "preco_venda",
    "MAP_EMPRESA":    "empresa",
    "MAP_UN":         "unidade",
    "MAP_EMBALAGEM":  "embalagem",
}

EMPRESA_KING = "LLE KING"
EMPRESA_PISA = "LLE PISA"

def load_mapao_from_path(path: str) -> pd.DataFrame | None:
    """Lê o MAPÃO a partir de um caminho e retorna DataFrame normalizado."""
    if not Path(path).exists():
        return None
    try:
        ext = Path(path).suffix.lower()
        engine = "xlrd" if ext == ".xls" else "openpyxl"
        df = pd.read_excel(path, engine=engine, header=0)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None

    rename = {k: v for k, v in COL_MAP.items() if k in df.columns}
    df = df.rename(columns=rename)

    if "custo" not in df.columns and "custo_ult" in df.columns:
        df["custo"] = df["custo_ult"]
    elif "custo" in df.columns and "custo_ult" in df.columns:
        df["custo"] = df["custo"].fillna(df["custo_ult"])

    for col in ["custo", "preco_venda"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "empresa" in df.columns:
        df["empresa"] = df["empresa"].astype(str).str.strip().str.upper()

    return df

def filtrar_tabela(df: pd.DataFrame, tabela: str) -> pd.DataFrame:
    if df is None or "empresa" not in df.columns:
        return pd.DataFrame()
    empresa = EMPRESA_KING.upper() if tabela == "King" else EMPRESA_PISA.upper()
    return df[df["empresa"] == empresa].copy().reset_index(drop=True)

def salvar_upload(uploaded_file) -> str:
    """Salva o arquivo enviado e retorna o caminho."""
    Path("tabelas").mkdir(exist_ok=True)
    ext  = Path(uploaded_file.name).suffix.lower()
    dest = f"tabelas/mapao{ext}"
    with open(dest, "wb") as fh:
        fh.write(uploaded_file.read())
    return dest

def calcular_margem(custo: float, preco: float) -> float:
    if preco and preco > 0:
        return (preco - custo) / preco * 100
    return 0.0

def brl(v):
    return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")

# ═══════════════════════════════════════════════════════════════════════════
#  PÁGINA DE CADASTRO
# ═══════════════════════════════════════════════════════════════════════════
def cadastro_page():
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown('<div class="cadastro-body">', unsafe_allow_html=True)
        if LOGO_B64:
            st.markdown(
                f'<div class="cadastro-logo">'
                f'<img src="data:image/png;base64,{LOGO_B64}" style="max-width:180px;width:100%;'
                f'background:{AZUL_ESC};padding:12px 18px;border-radius:8px;" /></div>',
                unsafe_allow_html=True,
            )
        st.markdown(f'<h3 style="color:{AZUL_ESC};margin:0 0 4px;">Criar credencial — OrçaPro</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color:#666;font-size:13px;margin-bottom:20px;">Grupo LLE · Sistema de Orçamentos</p>', unsafe_allow_html=True)

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
            if not novo_user.strip():  erros.append("Informe um nome de usuário.")
            if len(nova_senha) < 6:    erros.append("A senha precisa ter pelo menos 6 caracteres.")
            if nova_senha != confirma: erros.append("As senhas não coincidem.")
            if erros:
                for e in erros: st.error(e)
            else:
                h = hash_password(nova_senha)
                st.success("✅ Hash gerado com sucesso!")
                st.markdown("##### Cole isso nos Secrets do Streamlit Cloud:")
                st.code(f'[users]\n{novo_user.strip()} = "{h}"', language="toml")
                st.markdown("""
                <div class="steps-box">
                    Para múltiplos usuários, acumule no mesmo bloco:<br>
                    <code>[users]<br>joao = "hash_joao"<br>maria = "hash_maria"</code>
                </div>
                """, unsafe_allow_html=True)
                st.info("🔒 A senha nunca é armazenada — apenas o hash é gerado.", icon="🔒")

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
        if LOGO_B64:
            st.markdown(
                f'<div class="login-top">'
                f'<img src="data:image/png;base64,{LOGO_B64}" style="max-width:210px;width:100%;" />'
                f'</div>', unsafe_allow_html=True,
            )
        else:
            st.markdown(f'<div class="login-top"><span style="color:#fff;font-size:22px;font-weight:700;">GRUPO LLE</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="login-body">', unsafe_allow_html=True)
        st.markdown('<p class="login-sub">OrçaPro · Sistema de Orçamentos</p>', unsafe_allow_html=True)

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
#  APP PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════
def main_app():
    # ── Header ──────────────────────────────────────────────────────────────
    col_hdr, col_user, col_logout = st.columns([7, 2, 1])
    with col_hdr:
        page_header("OrçaPro", "Grupo LLE · Sistema de Orçamentos")
    with col_user:
        st.markdown(f'<p class="usuario-tag">👤 {st.session_state.usuario_logado}</p>', unsafe_allow_html=True)
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sair", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    # ── Carregamento do MAPÃO ────────────────────────────────────────────────
    # Tenta carregar da session ou do disco (arquivo já salvo anteriormente)
    df_mapao = st.session_state.df_mapao
    mapao_path = st.session_state.mapao_path

    # Se ainda não está na session, tenta achar no disco
    if df_mapao is None:
        for candidate in ["tabelas/mapao.xls", "tabelas/mapao.xlsx"]:
            if Path(candidate).exists():
                mapao_path = candidate
                df_mapao   = load_mapao_from_path(candidate)
                if df_mapao is not None:
                    st.session_state.df_mapao  = df_mapao
                    st.session_state.mapao_path = candidate
                break

    if df_mapao is None:
        st.warning("📂 Nenhum MAPÃO carregado. Faça o upload abaixo.")
        uploaded = st.file_uploader(
            "Upload do MAPÃO (.xls ou .xlsx)", type=["xls", "xlsx"], key="upload_mapao"
        )
        if uploaded:
            dest    = salvar_upload(uploaded)
            novo_df = load_mapao_from_path(dest)
            if novo_df is not None:
                st.session_state.df_mapao   = novo_df
                st.session_state.mapao_path = dest
                st.success(f"✅ MAPÃO carregado! {len(novo_df):,} produtos.")
                st.rerun()
            else:
                st.error("Não foi possível ler o arquivo. Verifique o formato.")
        return

    # ── Seleção de tabela ────────────────────────────────────────────────────
    col_tab, col_info = st.columns([4, 6])
    with col_tab:
        tabela_escolha = st.radio("Tabela de preços", ["King", "Pisa"], horizontal=True, key="tabela_radio")

    if tabela_escolha != st.session_state.tabela:
        st.session_state.tabela          = tabela_escolha
        st.session_state.itens_orcamento = []

    df_tab = filtrar_tabela(df_mapao, tabela_escolha)
    n_prod = len(df_tab)
    empresa_label = EMPRESA_KING if tabela_escolha == "King" else EMPRESA_PISA

    with col_info:
        if n_prod > 0:
            st.markdown(
                f'<div style="margin-top:.6rem;padding:8px 14px;background:#edf7f1;'
                f'border-left:4px solid {VERDE};border-radius:7px;font-size:13px;color:#0a5c31;">'
                f'✅ <b>{empresa_label}</b> — <b>{n_prod:,}</b> produtos carregados</div>',
                unsafe_allow_html=True,
            )
        else:
            empresas = df_mapao["empresa"].unique().tolist() if "empresa" in df_mapao.columns else []
            st.markdown(
                f'<div style="margin-top:.6rem;padding:8px 14px;background:#fdf0f0;'
                f'border-left:4px solid #dc3545;border-radius:7px;font-size:13px;color:#8b1a1a;">'
                f'⚠️ Nenhum produto para <b>{empresa_label}</b>. '
                f'Disponíveis: {", ".join(empresas)}</div>',
                unsafe_allow_html=True,
            )

    # Trocar MAPÃO
    with st.expander("🔄 Trocar MAPÃO"):
        novo_upload = st.file_uploader("Novo MAPÃO (.xls ou .xlsx)", type=["xls", "xlsx"], key="reupload_mapao")
        if novo_upload:
            dest    = salvar_upload(novo_upload)
            novo_df = load_mapao_from_path(dest)
            if novo_df is not None:
                st.session_state.df_mapao        = novo_df
                st.session_state.mapao_path      = dest
                st.session_state.itens_orcamento = []
                st.success(f"✅ MAPÃO atualizado! {len(novo_df):,} produtos.")
                st.rerun()
            else:
                st.error("Não foi possível ler o arquivo.")

    if n_prod == 0:
        return

    st.markdown("---")
    st.markdown('<span class="section-title">➕ Adicionar Produtos</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    aba_manual, aba_excel = st.tabs(["🔍 Busca manual", "📥 Importar pedido (Excel)"])

    with aba_manual:
        c1, c2, c3 = st.columns([3, 2, 1])
        with c1:
            busca = st.text_input(
                "Código ou nome do produto",
                placeholder="Ex: 39394 ou CABO...",
                key="busca_manual",
            )
        with c2:
            marcas = (["Todas"] + sorted(df_tab["marca"].dropna().unique().tolist())
                      if "marca" in df_tab.columns else ["Todas"])
            marca_filtro = st.selectbox("Filtrar por marca", marcas, key="marca_filtro")
        with c3:
            qtd = st.number_input("Quantidade", min_value=1, value=1, step=1, key="busca_qtd")

        busca_val  = st.session_state.get("busca_manual", "").strip()
        marca_val  = st.session_state.get("marca_filtro", "Todas")

        # Filtra o dataframe
        df_f = df_tab.copy()
        if marca_val != "Todas" and "marca" in df_f.columns:
            df_f = df_f[df_f["marca"] == marca_val]
        if busca_val:
            mask = pd.Series(False, index=df_f.index)
            for col in ["codigo", "descricao"]:
                if col in df_f.columns:
                    mask |= df_f[col].astype(str).str.upper().str.contains(busca_val.upper(), na=False)
            df_f = df_f[mask]

        tem_filtro = busca_val or marca_val != "Todas"

        if not tem_filtro:
            st.caption("Digite um código/nome ou selecione uma marca para buscar.")
        elif df_f.empty:
            st.warning("Nenhum produto encontrado.")
        else:
            cols_show = [c for c in ["codigo", "descricao", "marca", "unidade"] if c in df_f.columns]
            st.dataframe(
                df_f[cols_show].head(50).reset_index(drop=True),
                use_container_width=True,
                hide_index=True,
                height=min(380, 36 * min(len(df_f), 50) + 38),
            )
            st.caption(f"{len(df_f)} produto(s) — mostrando até 50")

            cod_list = df_f["codigo"].astype(str).tolist()

            def fmt(c):
                r = df_f[df_f["codigo"].astype(str) == c]
                if r.empty: return c
                desc = r.iloc[0].get("descricao", "")
                return f"{c}  —  {str(desc)[:60]}"

            cod_sel = st.selectbox("Selecionar produto", cod_list, format_func=fmt, key="cod_sel")

            if st.button("➕ Adicionar ao orçamento", type="primary", key="add_btn"):
                r = df_f[df_f["codigo"].astype(str) == cod_sel].iloc[0]
                item = {
                    "codigo":        str(r.get("codigo", "")),
                    "descricao":     str(r.get("descricao", "")),
                    "marca":         str(r.get("marca", "")) if "marca" in r.index else "",
                    "unidade":       str(r.get("unidade", "")) if "unidade" in r.index else "",
                    "custo_unit":    float(r.get("custo", 0) or 0),
                    "preco_unit":    float(r.get("preco_venda", 0) or 0),
                    "qtd":           int(st.session_state.get("busca_qtd", 1)),
                    "desc_item_pct": 0.0,
                    "acrescimo_pct": 0.0,
                }
                st.session_state.itens_orcamento.append(item)
                st.success(f"✅ **{item['descricao'][:55]}** adicionado! (Qtd: {item['qtd']})")

    with aba_excel:
        import io
        st.markdown('''
        <div class="info-box">
            <b>Formato esperado do Excel (colunas obrigatórias):</b><br>
            <code>codigo</code> &nbsp;·&nbsp; <code>qtd</code> &nbsp;·&nbsp; <code>preco_venda</code><br><br>
            O sistema cruza pelo código com o MAPÃO e puxa o custo automaticamente.<br>
            O preço de venda do Excel é o preço negociado com o cliente.
        </div>
        ''', unsafe_allow_html=True)

        modelo_df = pd.DataFrame([
            {"codigo": "39394", "qtd": 10, "preco_venda": 1.50},
            {"codigo": "39395", "qtd": 5,  "preco_venda": 2.00},
        ])
        buf = io.BytesIO()
        modelo_df.to_excel(buf, index=False)
        st.download_button("⬇️ Baixar modelo Excel", data=buf.getvalue(),
            file_name="modelo_pedido.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        pedido_upload = st.file_uploader("Upload do pedido (.xlsx ou .xls)", type=["xlsx", "xls"], key="upload_pedido")

        if pedido_upload:
            try:
                ext_p    = Path(pedido_upload.name).suffix.lower()
                engine_p = "xlrd" if ext_p == ".xls" else "openpyxl"
                df_pedido = pd.read_excel(pedido_upload, engine=engine_p, dtype=str)
                df_pedido.columns = [c.lower().strip().replace(" ", "_") for c in df_pedido.columns]

                alias_cod   = ["codigo", "cod", "code", "sku", "codprod", "map_codprod"]
                alias_qtd   = ["qtd", "quantidade", "qty", "quantity"]
                alias_preco = ["preco_venda", "preco", "venda", "price", "valor", "valor_venda", "preco_cliente"]

                def find_col(df, aliases):
                    for a in aliases:
                        if a in df.columns:
                            return a
                    return None

                col_cod   = find_col(df_pedido, alias_cod)
                col_qtd   = find_col(df_pedido, alias_qtd)
                col_preco = find_col(df_pedido, alias_preco)

                erros_col = []
                if not col_cod:   erros_col.append("código (`codigo`, `cod`, `sku`…)")
                if not col_qtd:   erros_col.append("quantidade (`qtd`, `quantidade`…)")
                if not col_preco: erros_col.append("preço de venda (`preco_venda`, `preco`…)")

                if erros_col:
                    st.error(f"Coluna(s) não encontrada(s): {', '.join(erros_col)}\n\nColunas no arquivo: `{list(df_pedido.columns)}`")
                else:
                    df_pedido["_cod"]   = df_pedido[col_cod].astype(str).str.strip()
                    df_pedido["_qtd"]   = pd.to_numeric(df_pedido[col_qtd], errors="coerce").fillna(1).astype(int)
                    df_pedido["_preco"] = pd.to_numeric(
                        df_pedido[col_preco].astype(str)
                            .str.replace(r"[R$\s]", "", regex=True)
                            .str.replace(",", ".", regex=False),
                        errors="coerce").fillna(0.0)
                    df_pedido = df_pedido[df_pedido["_cod"].notna() & (df_pedido["_cod"] != "")].copy()

                    df_mapao_idx = df_tab.copy()
                    df_mapao_idx["_cod_idx"] = df_mapao_idx["codigo"].astype(str).str.strip()

                    encontrados     = []
                    nao_encontrados = []

                    for _, row in df_pedido.iterrows():
                        cod = row["_cod"]
                        match = df_mapao_idx[df_mapao_idx["_cod_idx"] == cod]
                        if match.empty:
                            nao_encontrados.append(cod)
                            continue
                        m = match.iloc[0]
                        encontrados.append({
                            "codigo":        cod,
                            "descricao":     str(m.get("descricao", "")),
                            "marca":         str(m.get("marca", "")) if "marca" in m else "",
                            "unidade":       str(m.get("unidade", "")) if "unidade" in m else "",
                            "custo_unit":    float(m.get("custo", 0) or 0),
                            "preco_unit":    float(row["_preco"]),
                            "qtd":           int(row["_qtd"]),
                            "desc_item_pct": 0.0,
                            "acrescimo_pct": 0.0,
                        })

                    if encontrados:
                        st.success(f"✅ {len(encontrados)} produto(s) encontrado(s) no MAPÃO.")
                        preview_rows = []
                        for it in encontrados:
                            custo_t = it["custo_unit"] * it["qtd"]
                            preco_t = it["preco_unit"] * it["qtd"]
                            preview_rows.append({
                                "Código":      it["codigo"],
                                "Produto":     it["descricao"][:50],
                                "Qtd":         it["qtd"],
                                "Preço unit.": brl(it["preco_unit"]),
                                "Total":       brl(preco_t),
                                "Margem":      f"{calcular_margem(custo_t, preco_t):.1f}%",
                            })
                        st.dataframe(pd.DataFrame(preview_rows), use_container_width=True, hide_index=True)

                    if nao_encontrados:
                        st.warning(f"⚠️ {len(nao_encontrados)} código(s) não encontrado(s): `{', '.join(nao_encontrados)}`")

                    if encontrados:
                        if st.button(f"📥 Carregar {len(encontrados)} produto(s) no orçamento", type="primary", key="confirmar_pedido"):
                            st.session_state.itens_orcamento = encontrados
                            st.rerun()

            except Exception as e:
                st.error(f"Erro ao processar o arquivo: {e}")

    # ── Orçamento ────────────────────────────────────────────────────────────
    st.markdown('<span class="section-title">🧾 Orçamento</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    itens = st.session_state.itens_orcamento
    if not itens:
        st.info("Nenhum item adicionado ainda.")
        return

    with st.expander("💸 Desconto / Acréscimo Geral (aplica em todos os itens)"):
        dg1, dg2 = st.columns(2)
        with dg1:
            st.session_state.desconto_geral_pct = st.number_input(
                "Desconto geral (%)", min_value=0.0, max_value=100.0,
                value=float(st.session_state.desconto_geral_pct), step=0.5, format="%.2f",
            )
        with dg2:
            st.session_state.acrescimo_geral_pct = st.number_input(
                "Acréscimo geral (%)", min_value=0.0, max_value=100.0,
                value=float(st.session_state.get("acrescimo_geral_pct", 0.0)), step=0.5, format="%.2f",
            )

    dg_pct  = float(st.session_state.desconto_geral_pct)
    dg_acre = float(st.session_state.get("acrescimo_geral_pct", 0.0))

    # ── Cabeçalho da tabela ──────────────────────────────────────────────────
    st.markdown(f"""
    <div style="display:flex;align-items:center;padding:6px 10px;background:#e8edf5;
                border-radius:7px;font-size:12px;font-weight:700;color:#041747;
                text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;">
        <span style="flex:4">Produto</span>
        <span style="flex:1;text-align:center">Qtd</span>
        <span style="flex:1.5;text-align:center">Desc %</span>
        <span style="flex:1.5;text-align:center">Acrésc %</span>
        <span style="flex:1.2;text-align:center">Margem</span>
        <span style="flex:0.4"></span>
    </div>
    """, unsafe_allow_html=True)

    to_remove            = []
    total_custo          = 0.0
    total_venda_original = 0.0
    total_venda_final    = 0.0

    for i, item in enumerate(itens):
        # Calcula preços/margens para este item
        custo_total = item["custo_unit"] * item["qtd"]
        preco_orig  = item["preco_unit"] * item["qtd"]
        d_pct  = item["desc_item_pct"]
        a_pct  = item.get("acrescimo_pct", 0.0)
        # Desconto tem prioridade sobre acréscimo no mesmo item
        if d_pct > 0:
            preco_apos_item = preco_orig * (1 - d_pct / 100)
        elif a_pct > 0:
            preco_apos_item = preco_orig * (1 + a_pct / 100)
        else:
            preco_apos_item = preco_orig
        # Aplica geral: desconto tem prioridade sobre acréscimo
        if dg_pct > 0:
            preco_final = preco_apos_item * (1 - dg_pct / 100)
        elif dg_acre > 0:
            preco_final = preco_apos_item * (1 + dg_acre / 100)
        else:
            preco_final = preco_apos_item
        margem_orig  = calcular_margem(custo_total, preco_orig)
        margem_final = calcular_margem(custo_total, preco_final)
        cor_margem   = "#0a5c31" if margem_final >= 20 else ("#7d5c00" if margem_final >= 10 else "#8b1a1a")
        seta         = "▲" if margem_final >= margem_orig else "▼"
        delta_str    = f"{seta} {abs(margem_final - margem_orig):.1f}pp"

        total_custo          += custo_total
        total_venda_original += preco_orig
        total_venda_final    += preco_final

        with st.container():
            st.markdown('<div class="item-row">', unsafe_allow_html=True)
            ca, cb, cc, cd, ce, cf = st.columns([4, 1, 1.5, 1.5, 1.2, 0.4])
            with ca:
                st.markdown(
                    f'<div style="font-size:13px;font-weight:600;color:#041747;line-height:1.3">{item["descricao"][:65]}</div>'
                    f'<div style="font-size:11px;color:#888;margin-top:2px">Cód: {item["codigo"]} · {item["marca"]} · {item.get("unidade","")}</div>',
                    unsafe_allow_html=True,
                )
            with cb:
                item["qtd"] = st.number_input("Qtd", min_value=1, value=item["qtd"],
                    key=f"qtd_{i}", label_visibility="collapsed")
            with cc:
                item["desc_item_pct"] = st.number_input(
                    "Desc %", min_value=0.0, max_value=100.0,
                    value=float(item["desc_item_pct"]), step=0.5, format="%.1f",
                    key=f"dpct_{i}", label_visibility="collapsed")
            with cd:
                item["acrescimo_pct"] = st.number_input(
                    "Acrésc %", min_value=0.0, max_value=100.0,
                    value=float(item.get("acrescimo_pct", 0.0)), step=0.5, format="%.1f",
                    key=f"acre_{i}", label_visibility="collapsed")
            with ce:
                st.markdown(
                    f'<div style="text-align:center;padding:4px 0">'
                    f'<div style="font-size:18px;font-weight:700;color:{cor_margem}">{margem_final:.1f}%</div>'
                    f'<div style="font-size:11px;color:{cor_margem};opacity:.8">{delta_str}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with cf:
                if st.button("✕", key=f"del_{i}", help="Remover item"):
                    to_remove.append(i)
            st.markdown('</div>', unsafe_allow_html=True)

    for i in reversed(to_remove):
        st.session_state.itens_orcamento.pop(i)
    if to_remove:
        st.rerun()


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
        st.metric("Total com descontos", brl(total_venda_final),
                  delta=brl(total_venda_final - total_venda_original), delta_color="inverse")
    with r3:
        st.metric("Margem tabela", f"{margem_orig_geral:.1f}%")
    with r4:
        st.metric(
            "Margem final", f"{margem_final_geral:.1f}%",
            delta=f"{margem_final_geral - margem_orig_geral:+.1f}%",
            delta_color="normal" if margem_final_geral >= margem_orig_geral else "inverse",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if margem_final_geral < 10:
        st.markdown('<div class="alcada-err">🚨 <b>Margem abaixo de 10%!</b> Revise os descontos antes de enviar.</div>', unsafe_allow_html=True)
    elif margem_final_geral < 20:
        st.markdown('<div class="alcada-warn">⚠️ <b>Margem abaixo de 20%.</b> Atenção antes de fechar o pedido.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alcada-ok">✅ <b>Margem saudável.</b> Orçamento dentro dos parâmetros.</div>', unsafe_allow_html=True)

    # ── Exportar relatório ────────────────────────────────────────────────────
    st.markdown("---")
    import io as _io
    rows_export = []
    for item in itens:
        ct   = item["custo_unit"] * item["qtd"]
        po   = item["preco_unit"] * item["qtd"]
        dpct = item["desc_item_pct"]
        apct = item.get("acrescimo_pct", 0.0)
        if dpct > 0:
            pa = po * (1 - dpct / 100)
        elif apct > 0:
            pa = po * (1 + apct / 100)
        else:
            pa = po
        if dg_pct > 0:
            pf = pa * (1 - dg_pct / 100)
        elif dg_acre > 0:
            pf = pa * (1 + dg_acre / 100)
        else:
            pf = pa
        rows_export.append({
            "Código":             item["codigo"],
            "Produto":            item["descricao"],
            "Marca":              item["marca"],
            "Unidade":            item.get("unidade", ""),
            "Qtd":                item["qtd"],
            "Preço unit. tabela": round(item["preco_unit"], 4),
            "Desc item (%)":      round(dpct, 2),
            "Acrésc item (%)":    round(apct, 2),
            "Desc geral (%)":     round(dg_pct, 2),
            "Preço unit. final":  round(pf / item["qtd"], 4) if item["qtd"] > 0 else 0,
            "Total final":        round(pf, 2),
            "Margem (%)":         round(calcular_margem(ct, pf), 2),
        })

    df_export = pd.DataFrame(rows_export)
    # Linha de totais
    total_row = {
        "Código": "TOTAL", "Produto": "", "Marca": "", "Unidade": "",
        "Qtd": sum(r["Qtd"] for r in rows_export),
        "Preço unit. tabela": "",
        "Desc item (%)": "", "Desc item (R$)": "", "Desc geral (%)": "",
        "Preço unit. final": "",
        "Total final": round(total_venda_final, 2),
        "Margem (%)": round(margem_final_geral, 2),
    }
    df_export = pd.concat([df_export, pd.DataFrame([total_row])], ignore_index=True)

    buf = _io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df_export.to_excel(writer, index=False, sheet_name="Orçamento")
        ws = writer.sheets["Orçamento"]
        # Larguras automáticas
        for col in ws.columns:
            max_len = max((len(str(c.value)) for c in col if c.value), default=10)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 3, 50)

    col_exp, col_clear = st.columns([2, 2])
    with col_exp:
        st.download_button(
            "📥 Exportar relatório (Excel)",
            data=buf.getvalue(),
            file_name="orcamento_grupo_lle.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True,
        )
    with col_clear:
        if st.button("🗑️ Limpar orçamento completo", use_container_width=True):
            st.session_state.itens_orcamento    = []
            st.session_state.desconto_geral_pct  = 0.0
            st.session_state.acrescimo_geral_pct = 0.0
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
