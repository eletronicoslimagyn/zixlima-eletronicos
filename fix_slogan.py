import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Encontra os blocos da imagem (tanto no topo quanto no rodapé)
padrao = r'<div style="text-align: center;[^>]*>\s*<img[^>]*>\s*</div>'
blocos = list(re.finditer(padrao, html))

# Se achou mais de um, remove o do rodapé (o último)
if len(blocos) >= 2:
    bloco_rodape = blocos[-1]
    html = html[:bloco_rodape.start()] + html[bloco_rodape.end():]
    print("🧹 Imagem do rodapé removida com sucesso!")

# Cria a nova tag com a imagem reduzida em 50%
nova_tag = '<div style="text-align: center; padding: 10px; width: 100%; box-sizing: border-box;"><img src="novo_slogan.jpg" alt="Zixlima" style="width: 50%; max-width: 300px; height: auto; display: block; margin: 0 auto; border-radius: 8px;"></div>'

# Substitui a imagem do topo
if blocos:
    html = html.replace(blocos[0].group(0), nova_tag, 1)
    print("✅ Imagem do topo substituída e ajustada para 50%!")

# Salva o arquivo
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
