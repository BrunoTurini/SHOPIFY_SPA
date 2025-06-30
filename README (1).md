# 🛒 Atualização de Estoque e Preços - Shopify via Python

Scripts para automação da atualização de **estoques** e **preços** de produtos na plataforma Shopify, com base em planilhas locais contendo `SKU`.

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
- Biblioteca `pandas`, `requests`, `openpyxl`  
  Instalar com:

```bash
pip install pandas requests openpyxl
```

- Token de acesso privado da Shopify com permissões de:
  - `read_products`
  - `write_products`
  - `read_inventory`
  - `write_inventory`

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
- As requisições respeitam os limites da API (máx. 2 chamadas por segundo);
- Apenas variantes com SKUs exatos são atualizadas.