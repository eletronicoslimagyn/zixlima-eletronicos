#!/bin/bash
clear
echo "=== CRIADOR AUTOMÁTICO DO ZIXLIMA V2 ==="
read -p "👉 Digite seu nome de usuário do GitHub (ex: eletronicoslimagyn): " GH_USER
read -s -p "👉 Cole seu Token do GitHub (não vai aparecer na tela) e aperte Enter: " GH_TOKEN
echo ""

echo "⏳ Tentando criar o repositório zixlima-v2 no GitHub..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GH_TOKEN" https://api.github.com/user/repos -d "{\"name\":\"zixlima-v2\", \"private\": false}")

if [ "$STATUS" -eq 201 ]; then
    echo "✅ Repositório zixlima-v2 criado com sucesso!"
elif [ "$STATUS" -eq 422 ]; then
    echo "✅ Repositório zixlima-v2 já existe. Continuando..."
else
    echo "⚠️ Erro ao criar repositório. Verifique se o Token tem permissão 'repo'."
    echo "⚠️ Vá no site do GitHub e crie um repositório vazio chamado 'zixlima-v2' manualmente."
    read -p "Pressione Enter quando o repositório estiver criado no site..."
fi

echo "⏳ Baixando o projeto moderno (Singitronic)..."
cd ~
rm -rf zixlima-v2
git clone https://github.com/Kuzma02/Electronics-eCommerce-Shop-With-Admin-Dashboard-NextJS-NodeJS.git zixlima-v2

echo "⏳ Enviando código para o seu GitHub..."
cd zixlima-v2
git remote remove origin
git remote add origin https://$GH_TOKEN@github.com/$GH_USER/zixlima-v2.git
git branch -M main
git push -u origin main

echo ""
echo "✅ TUDO PRONTO! O código está no seu GitHub."
