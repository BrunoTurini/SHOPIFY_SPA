# 🛒 S.H.O.P. - Shopify Handling & Operations Processor

Scripts para automação da atualização de **estoques** e **preços** de produtos na plataforma Shopify, com base em planilhas locais contendo `SKU`.

Este projeto é composto por dois módulos principais:

- `atualiza_estoque.py`: Atualiza os níveis de estoque por SKU
- `atualiza_precos.py`: Atualiza os preços por SKU

---

## 📁 Estrutura do Projeto

```
/
├── atualiza_estoque.py           # Script que atualiza o estoque por SKU
├── atualiza_precos.py            # Script que atualiza o preço por SKU
├── estoque_atualizado.xlsx       # Planilha com SKUs e quantidades
├── precos_atualizados.xlsx       # Planilha com SKUs e preços
├── executar_estoque.bat          # Executa atualização de estoque com clique duplo
├── executar_precos.bat           # Executa atualização de preços com clique duplo
├── log_estoque_YYYY-MM-DD.txt    # Logs automáticos da execução de estoque
├── log_precos_YYYY-MM-DD.txt     # Logs automáticos da execução de preços
└── README.md                     # Este guia de uso
```

---

## ✅ Requisitos

- Python 3.8+
- Bibliotecas Python necessárias:

```bash
pip install pandas requests openpyxl
```

---

## 🔐 Sobre o Token da Shopify

Para que os scripts funcionem corretamente, é necessário gerar um **Access Token privado da Shopify**, associado a um **app personalizado** com permissões específicas.

### Como gerar:

1. Acesse o admin da Shopify: `https://sualoja.myshopify.com/admin`
2. Vá em **Apps > Desenvolver apps para sua loja**
3. Clique em **Criar um app** ou edite um já existente
4. Adicione as permissões mínimas necessárias:
   - `read_products`
   - `write_products`
   - `read_inventory`
   - `write_inventory`
5. Gere o **Access Token** e copie

> ⚠️ **Importante**: mantenha o token em segurança e não compartilhe publicamente.  
> Inclua-o diretamente nos scripts em tempo de desenvolvimento ou idealmente em um `.env` no futuro.

---

## 📦 Planilha de Estoque

**Arquivo:** `estoque_atualizado.xlsx`  
**Colunas obrigatórias:**

| SKU     | ESTOQUE |
|---------|---------|
| 0101234 | 18      |
| 0104321 | 45      |

---

## 💰 Planilha de Preços

**Arquivo:** `precos_atualizados.xlsx`  
**Colunas obrigatórias:**

| SKU     | PREÇO   |
|---------|---------|
| 0101234 | 39.90   |
| 0104321 | 78.50   |

---

## ▶️ Como executar

### 🔁 Atualizar estoque

```bash
python atualiza_estoque.py
```

Ou com clique duplo:

```bash
executar_estoque.bat
```

### 💵 Atualizar preços

```bash
python atualiza_precos.py
```

Ou com clique duplo:

```bash
executar_precos.bat
```

---

## 📝 Logs

Após cada execução, será gerado um arquivo de log com detalhes:

- `log_estoque_YYYY-MM-DD_HH-MM-SS.txt`
- `log_precos_YYYY-MM-DD_HH-MM-SS.txt`

Esses arquivos mostram o status de cada SKU processado (atualizado, erro ou SKU não encontrado).

---

## ⚠️ Observações

- Os SKUs são normalizados com `zfill(7)` para garantir que todos tenham 7 dígitos (ex: `0012345`);
- As requisições respeitam os limites da API da Shopify (máx. 2 chamadas por segundo);
- Apenas variantes com SKUs exatos são atualizadas;
- Os preços são tratados como `float` com ponto decimal (ex: `49.90`).

---

## 📛 Nome do Projeto: S.H.O.P.

**S.H.O.P.** significa: **Shopify Handling & Operations Processor**

### Acróstico:

- **S** – Sync de dados entre planilhas e Shopify  
- **H** – Handling seguro de estoque e preços  
- **O** – Operações automáticas via scripts Python  
- **P** – Precisão nos SKUs, logs e integração

---
