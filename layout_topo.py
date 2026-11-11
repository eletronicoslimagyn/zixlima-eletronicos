import re

def reestruturar_topo():
    arquivo = "index.html"
    with open(arquivo, "r", encoding="utf-8") as f:
        html = f.read()

    match_busca = re.search(r'<input[^>]*placeholder="[^"]*[Bb]uscar[^"]*"[^>]*>', html)
    busca_html = match_busca.group(0) if match_busca else ''
    
    match_botao = re.search(r'<a[^>]*>.*?Falar Conosco.*?</a>', html, re.DOTALL | re.IGNORECASE)
    if not match_botao:
        match_botao = re.search(r'<button[^>]*>.*?Falar Conosco.*?</button>', html, re.DOTALL | re.IGNORECASE)
    botao_html = match_botao.group(0) if match_botao else ''

    if busca_html: html = html.replace(busca_html, '')
    if botao_html: html = html.replace(botao_html, '')

    novo_bloco = f'''
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; padding: 20px 10px; box-sizing: border-box; gap: 15px; background: white;">
        <img src="novo_slogan.jpg" alt="Zixlima" style="width: 25%; min-width: 120px; max-width: 250px; height: auto; display: block;">
        <div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 10px; width: 100%; max-width: 600px;">
            <div style="flex: 1; min-width: 200px; width: 100%;">{busca_html}</div>
            <div style="width: 100%; max-width: 200px;">{botao_html}</div>
        </div>
    </div>
    '''

    padrao_div = r'<div[^>]*text-align:\s*center;[^>]*>.*?<img[^>]*novo_slogan\.jpg[^>]*>.*?</div>'
    if re.search(padrao_div, html, re.DOTALL):
        html = re.sub(padrao_div, novo_bloco, html, count=1, flags=re.DOTALL)
    else:
        padrao_img = r'<img[^>]*novo_slogan\.jpg[^>]*>'
        html = re.sub(padrao_img, novo_bloco, html, count=1)

    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ Layout atualizado: Foto 25% e busca/WhatsApp embaixo!")

reestruturar_topo()
