# 📊 OrçaPro — Sistema de Orçamentos

Sistema interno para gestão de orçamentos com controle de margens, descontos por item e por pedido, com suporte às tabelas **King** e **Pisa**.

---

## 🚀 Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/orcamento-system.git
cd orcamento-system
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as senhas

```bash
# Gere o hash da sua senha
python gerar_senha.py
```

Depois edite `.streamlit/secrets.toml`:

```toml
[users]
admin  = "HASH_SHA256_AQUI"
vendas = "HASH_SHA256_AQUI"
```

### 4. Adicione suas tabelas de preços

Coloque os arquivos Excel na pasta `tabelas/`:
- `tabelas/tabela_king.xlsx`
- `tabelas/tabela_pisa.xlsx`

> ⚠️ A pasta `tabelas/` está no `.gitignore` — os preços **nunca** serão enviados ao GitHub.

A planilha precisa ter (ao menos) estas colunas (o sistema aceita variações de nome):

| Coluna | Exemplos aceitos |
|--------|-----------------|
| Código | `codigo`, `cod`, `sku` |
| Descrição | `descricao`, `produto`, `nome` |
| Marca | `marca`, `brand`, `fabricante` |
| Custo | `custo`, `preco_custo`, `cost` |
| Preço de venda | `preco_venda`, `preco`, `venda` |

> Alternativamente, use o upload direto dentro do próprio sistema na primeira vez.

### 5. Execute o app

```bash
streamlit run app.py
```

Acesse em: **http://localhost:8501**

---

## ☁️ Deploy no Streamlit Cloud

1. Suba o repositório no GitHub (sem `secrets.toml` e sem `tabelas/`)
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o repositório e defina `app.py` como arquivo principal
4. Em **Settings → Secrets**, cole o conteúdo do `secrets.toml` com os hashes das senhas
5. Para as tabelas: use o upload dentro do sistema (primeira vez) **ou** configure um volume persistente

---

## 🔒 Segurança

| Camada | Proteção |
|--------|----------|
| Login | Usuário + senha com hash SHA-256 |
| Tabelas | Fora do repositório (`.gitignore`) |
| Preços | **Nunca exibidos** na tela — só margens |
| Secrets | Armazenados em `secrets.toml` (local) ou Streamlit Cloud Secrets |

---

## 📁 Estrutura do projeto

```
orcamento-system/
├── app.py                    # Aplicação principal
├── style.css                 # Tema visual
├── requirements.txt          # Dependências
├── gerar_senha.py            # Utilitário de hash de senha
├── criar_tabelas_exemplo.py  # Gera planilhas de teste
├── .gitignore                # Protege arquivos sensíveis
├── .streamlit/
│   ├── config.toml           # Configuração do Streamlit
│   └── secrets.toml          # ⚠️ NÃO commitar — senhas aqui
└── tabelas/                  # ⚠️ NÃO commitar — preços aqui
    ├── tabela_king.xlsx
    └── tabela_pisa.xlsx
```

---

## 💡 Funcionalidades

- ✅ Login seguro com múltiplos usuários
- ✅ Seleção entre tabela **King** e **Pisa**
- ✅ Busca por código ou nome do produto
- ✅ Filtro por marca
- ✅ Desconto por item (% ou R$)
- ✅ Desconto geral no pedido (% ou R$)
- ✅ Margem original vs. margem com desconto em tempo real
- ✅ Alerta automático de margem baixa (< 10% e < 20%)
- ✅ Preços de custo **nunca expostos** — apenas margens
