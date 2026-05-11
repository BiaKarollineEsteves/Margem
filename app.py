import streamlit as st
import pandas as pd
from pathlib import Path
import hashlib

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OrçaPro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Inject CSS ─────────────────────────────────────────────────────────────
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
    st.markdown('<div class="login-wrap cadastro-wrap">', unsafe_allow_html=True)
    st.markdown('<h1 class="logo">OrçaPro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="login-sub">Criar credencial de acesso</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <b>Como funciona em 3 passos:</b><br><br>
        <b>1.</b> Preencha usuário e senha abaixo e clique em <b>Gerar Hash</b><br>
        <b>2.</b> Copie o bloco <code>toml</code> gerado<br>
        <b>3.</b> No Streamlit Cloud → seu app → <b>⚙️ Settings → Secrets</b> → cole e salve
    </div>
    """, unsafe_allow_html=True)

    with st.form("cadastro_form"):
        novo_user  = st.text_input("Nome de usuário", placeholder="ex: joao_vendas")
        nova_senha = st.text_input("Senha", type="password", placeholder="mínimo 6 caracteres")
        confirma   = st.text_input("Confirmar senha", type="password", placeholder="repita a senha")
        gerar      = st.form_submit_button("🔑 Gerar Hash")

    if gerar:
        erros = []
        if not novo_user.strip():
            erros.append("Informe um nome de usuário.")
        if len(nova_senha) < 6:
            erros.append("A senha precisa ter pelo menos 6 caracteres.")
        if nova_senha != confirma:
            erros.append("As senhas não coincidem.")

        if erros:
            for e in erros:
                st.error(e)
        else:
            h = hash_password(nova_senha)
            st.success("✅ Hash gerado com sucesso!")

            st.markdown("---")
            st.markdown("##### Cole isso nos Secrets do Streamlit Cloud:")
            st.code(f'[users]\n{novo_user.strip()} = "{h}"', language="toml")

            st.markdown("""
            <div class="steps-box">
                <b>Para adicionar múltiplos usuários</b>, acumule no mesmo bloco <code>[users]</code>:<br><br>
                <code>[users]<br>
                joao = "hash_do_joao"<br>
                maria = "hash_da_maria"</code>
            </div>
            """, unsafe_allow_html=True)

            st.info("🔒 O hash é calculado só no seu navegador. A senha nunca trafega nem é salva.", icon="🔒")

    st.markdown("---")
    if st.button("← Voltar para login"):
        st.session_state.pagina = "login"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#  PÁGINA DE LOGIN
# ═══════════════════════════════════════════════════════════════════════════
def login_page():
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown('<h1 class="logo">OrçaPro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="login-sub">Sistema interno de orçamentos</p>', unsafe_allow_html=True)

    if not has_any_user_configured():
        st.warning("Nenhum usuário configurado ainda. Crie sua credencial primeiro.")

    with st.form("login_form"):
        user = st.text_input("Usuário", placeholder="seu usuário")
        pw   = st.text_input("Senha", type="password", placeholder="••••••••")
        btn  = st.form_submit_button("Entrar →")

    if btn:
        if not has_any_user_configured():
            st.error("Nenhum usuário cadastrado nos Secrets. Clique em 'Criar credencial' abaixo.")
        elif check_credentials(user, pw):
            st.session_state.logged_in     = True
            st.session_state.usuario_logado = user.strip()
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

    st.markdown('<div style="text-align:center;margin-top:1.5rem;">', unsafe_allow_html=True)
    if st.button("Criar credencial / Gerar hash"):
        st.session_state.pagina = "cadastro"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
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

# ═══════════════════════════════════════════════════════════════════════════
#  APP PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════
def main_app():
    # ── Header ──────────────────────────────────────────────────────────────
    col_logo, col_tabela_sel, col_user, col_logout = st.columns([2, 5, 2, 1])
    with col_logo:
        st.markdown('<span class="logo-sm">OrçaPro</span>', unsafe_allow_html=True)
    with col_tabela_sel:
        tabela_escolha = st.radio(
            "Tabela de preços",
            ["King", "Pisa"],
            horizontal=True,
            key="tabela_radio",
        )
        if tabela_escolha != st.session_state.tabela:
            st.session_state.tabela         = tabela_escolha
            st.session_state.df_tabela      = load_tabela(tabela_escolha)
            st.session_state.itens_orcamento = []
    with col_user:
        st.markdown(
            f'<p class="usuario-tag">👤 {st.session_state.usuario_logado}</p>',
            unsafe_allow_html=True,
        )
    with col_logout:
        if st.button("Sair"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

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
    st.markdown('<h3 class="section-title">🔍 Adicionar Produto</h3>', unsafe_allow_html=True)

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
                mask |= df_filtrado[col].astype(str).str.lower().str.contains(
                    busca.lower(), na=False
                )
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

            if st.button("➕ Adicionar ao orçamento", key="add_btn"):
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
                st.success(f"'{item['descricao']}' adicionado!")
                st.rerun()

    # ── Orçamento ────────────────────────────────────────────────────────────
    st.markdown('<h3 class="section-title">🧾 Orçamento</h3>', unsafe_allow_html=True)

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

                preco_final = preco_apos_item * (1 - dg_pct / 100) if dg_pct > 0 else preco_apos_item

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

    # Desconto geral R$ no total (só se não usou %)
    if dg_pct == 0 and dg_rs > 0:
        total_venda_final = max(0.0, total_venda_final - dg_rs)

    # ── Resumo ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<h3 class="section-title">📊 Resumo do Pedido</h3>', unsafe_allow_html=True)

    margem_orig_geral  = calcular_margem(total_custo, total_venda_original)
    margem_final_geral = calcular_margem(total_custo, total_venda_final)

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric("Total tabela", f"R$ {total_venda_original:,.2f}")
    with r2:
        st.metric(
            "Total com descontos",
            f"R$ {total_venda_final:,.2f}",
            delta=f"R$ {total_venda_final - total_venda_original:,.2f}",
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

    if margem_final_geral < 10:
        st.error("🚨 Margem abaixo de 10%! Revise os descontos antes de enviar.")
    elif margem_final_geral < 20:
        st.warning("⚠️ Margem abaixo de 20%. Cuidado!")

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
