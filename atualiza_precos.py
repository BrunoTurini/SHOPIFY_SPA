import pandas as pd
import requests
import datetime
import os
import time

# 🔧 Configurações da Shopify
SHOPIFY_DOMAIN = 'sua-loja.myshopify.com'
SHOPIFY_TOKEN = 'seu-token-aqui'
HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_TOKEN
}

# 📁 Arquivo de log
DATA_LOG = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
LOG_PATH = f'log_precos_{DATA_LOG}.txt'

def log(msg):
    print(msg)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

# 🔍 Coletar todos os SKUs e variant_ids
def obter_skus_e_variantes():
    log("🔍 Coletando SKUs e variant_ids da Shopify...")
    sku_map = {}
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/2023-10/products.json?limit=250"

    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            log(f"❌ Erro na requisição: {response.status_code} - {response.text}")
            break

        produtos = response.json().get('products', [])
        for produto in produtos:
            for variant in produto.get('variants', []):
                sku = variant.get('sku')
                variant_id = variant.get('id')
                if sku:
                    sku_formatado = str(sku).strip().zfill(7)
                    sku_map[sku_formatado] = variant_id

        # Verifica se há próxima página
        link_header = response.headers.get("Link", "")
        next_url = None
        for part in link_header.split(','):
            if 'rel="next"' in part:
                next_url = part.split(';')[0].strip().strip('<>')
                break

        url = next_url
        time.sleep(0.2)

    log(f"✅ Total de SKUs coletados: {len(sku_map)}\n")
    return sku_map

# 🔁 Atualiza o preço de uma variante
def atualizar_preco_variant(variant_id, preco):
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/2023-10/variants/{variant_id}.json"
    payload = {
        "variant": {
            "id": variant_id,
            "price": str(preco).replace(',', '.')  # garante formato decimal
        }
    }
    response = requests.put(url, headers=HEADERS, json=payload)
    return response.status_code, response.text

# 📦 Execução principal
def atualizar_precos(planilha):
    if not os.path.exists(planilha):
        log(f"❌ Planilha '{planilha}' não encontrada.")
        return

    try:
        df = pd.read_excel(planilha, dtype={'SKU': str})
    except Exception as e:
        log(f"❌ Erro ao ler a planilha: {str(e)}")
        return

    if 'SKU' not in df.columns or 'PREÇO' not in df.columns:
        log("❌ A planilha deve conter as colunas 'SKU' e 'PREÇO'.")
        return

    sku_map = obter_skus_e_variantes()
    total = len(df)
    log(f"📦 Início da atualização de preços para {total} SKUs ({datetime.datetime.now()})\n")

    for i, row in df.iterrows():
        sku = str(row['SKU']).strip().zfill(7)
        try:
            preco = float(str(row['PREÇO']).replace(',', '.'))
        except:
            log(f"⚠️ Preço inválido para SKU {sku}: '{row['PREÇO']}'")
            continue

        log(f"🔄 [{i+1}/{total}] SKU: {sku} → Preço: R$ {preco:.2f}")

        variant_id = sku_map.get(sku)
        if variant_id:
            status, msg = atualizar_preco_variant(variant_id, preco)
            time.sleep(0.6)  # respeita limite de chamadas da API
            if status == 200:
                log("✅ Preço atualizado com sucesso.")
            else:
                log(f"❌ Erro ao atualizar preço: {msg}")
        else:
            log("⚠️ SKU não encontrado na Shopify.")

    log(f"\n🏁 Fim da execução: {datetime.datetime.now()}")

# 🚀 Rodar com planilha padrão
atualizar_precos('precos_atualizados.xlsx')
