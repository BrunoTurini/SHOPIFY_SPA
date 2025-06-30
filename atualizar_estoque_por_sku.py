import pandas as pd
import requests
import datetime
import os
import time

# 🔧 Configurações
SHOPIFY_DOMAIN = 'sua-loja.myshopify.com'     # Ex: plenitude.myshopify.com
SHOPIFY_TOKEN = 'seu-token-aqui'              # Token com permissões adequadas
LOCATION_ID = '1234567890'                    # ID do local ativo (Brasil, Portugal, etc)

HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_TOKEN
}

# 📁 Arquivo de log
DATA_LOG = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
LOG_PATH = f'log_estoque_{DATA_LOG}.txt'

def log(mensagem):
    print(mensagem)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(mensagem + '\n')

# 🔍 Buscar todos os SKUs e seus inventory_item_ids da Shopify
def obter_skus_shopify():
    log("🔍 Coletando SKUs e inventory_item_ids da Shopify (com paginação)...")
    sku_map = {}
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/2023-10/products.json?limit=250"

    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            log(f"❌ Erro ao buscar produtos: {response.status_code} - {response.text}")
            break

        produtos = response.json().get('products', [])
        for produto in produtos:
            for variant in produto.get('variants', []):
                sku = variant.get('sku')
                inventory_item_id = variant.get('inventory_item_id')
                if sku:
                    sku_formatado = str(sku).strip().zfill(7)
                    sku_map[sku_formatado] = inventory_item_id

        log(f"✔️ Página processada - {len(produtos)} produtos")

        # Paginação via Link header
        link_header = response.headers.get("Link", "")
        next_url = None
        for part in link_header.split(','):
            if 'rel="next"' in part:
                next_url = part.split(';')[0].strip().strip('<>')
                break

        url = next_url
        time.sleep(0.2)  # respeita o limite total da API

    log(f"✅ Total de SKUs carregados: {len(sku_map)}\n")
    return sku_map

# 🔁 Atualizar estoque com pausa para respeitar limite de requisições
def set_inventory(inventory_item_id, quantity):
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/2023-10/inventory_levels/set.json"
    payload = {
        "location_id": LOCATION_ID,
        "inventory_item_id": inventory_item_id,
        "available": int(quantity)
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.status_code, response.text

# 📦 Execução principal
def atualizar_estoque(planilha):
    if not os.path.exists(planilha):
        log(f"❌ Planilha '{planilha}' não encontrada.")
        return

    try:
        df = pd.read_excel(planilha, dtype={'SKU': str})
    except Exception as e:
        log(f"❌ Erro ao ler a planilha: {str(e)}")
        return

    if 'SKU' not in df.columns or 'Estoque' not in df.columns:
        log("❌ A planilha deve conter as colunas 'SKU' e 'Estoque'.")
        return

    sku_map = obter_skus_shopify()
    total = len(df)
    log(f"📦 Início da atualização de estoque para {total} SKUs ({datetime.datetime.now()})\n")

    for i, row in df.iterrows():
        sku = str(row['SKU']).strip().zfill(7)
        try:
            quantidade = int(row['Estoque'])
        except:
            log(f"⚠️ Estoque inválido para SKU {sku}: '{row['Estoque']}'")
            continue

        log(f"🔄 [{i+1}/{total}] SKU: {sku} → Quantidade: {quantidade}")

        inventory_item_id = sku_map.get(sku)
        if inventory_item_id:
            status, msg = set_inventory(inventory_item_id, quantidade)
            time.sleep(0.6)  # ✅ Pausa entre chamadas para respeitar limite da API
            if status == 200:
                log(f"✅ Estoque atualizado com sucesso.")
            else:
                log(f"❌ Erro ao atualizar estoque: {msg}")
        else:
            log(f"⚠️ SKU {sku} não encontrado no catálogo da Shopify.")

    log(f"\n🏁 Fim da execução: {datetime.datetime.now()}")

# 🚀 Início
atualizar_estoque('estoque_atualizado.xlsx')
