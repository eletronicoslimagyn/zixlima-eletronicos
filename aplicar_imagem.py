import os

def aplicar_imagem():
    arquivo_html = "index.html"
    nome_imagem = "slogan_oficial.jpg"
    
    if not os.path.exists(arquivo_html):
        print("❌ Erro: O arquivo index.html não foi encontrado.")
        return

    if not os.path.exists(nome_imagem):
        print(f"❌ Erro: A imagem '{nome_imagem}' não está na pasta. Verifique.")
        return

    with open(arquivo_html, "r", encoding="utf-8") as f:
        html = f.read()

    print("\n--- APLICAR IMAGEM COMO SLOGAN TOTAL ---")
    print("Vá no seu site pelo navegador do celular, copie o TEXTO do slogan atual e cole aqui.")
    texto_antigo = input("\nCole aqui o TEXTO ANTIGO exato: ")
    
    # Código que insere a imagem centralizada e adaptável ao tamanho da tela
    tag_imagem = f'''
    <div style="text-align: center; padding: 15px 10px; width: 100%; box-sizing: border-box;">
        <img src="{nome_imagem}" alt="Zixlima Eletrônicos - Tecnologia em Movimento" style="max-width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    </div>
    '''

    # Faz a substituição
    if texto_antigo in html:
        html = html.replace(texto_antigo, tag_imagem)
        
        with open(arquivo_html, "w", encoding="utf-8") as f:
            f.write(html)
            
        print("\n✅ SUCESSO! A imagem foi inserida no topo do seu site.")
    else:
        print("\n⚠️ ATENÇÃO: O texto antigo não foi encontrado no código.")
        print("Dica: Copie o texto exato, com os mesmos acentos e letras.")

if __name__ == "__main__":
    aplicar_imagem()
