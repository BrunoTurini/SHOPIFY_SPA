@echo off
cd /d %~dp0
echo Iniciando atualização de preços na Shopify...
python atualiza_precos.py
pause
