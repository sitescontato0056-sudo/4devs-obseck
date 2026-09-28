#!/data/data/com.termux/files/usr/bin/bash
echo "[*] Instalando 4devs-obseck..."

pkg update -y && pkg upgrade -y
pkg install -y python git

chmod +x painel.py
cp painel.py $PREFIX/bin/obseck-tool

echo "[✓] Instalado! Digite: obseck-tool"
