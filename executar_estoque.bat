@echo off
cd /d %~dp0
echo Iniciando atualização de estoque na Shopify...
python atualizar_estoque_por_sku.py
pause
