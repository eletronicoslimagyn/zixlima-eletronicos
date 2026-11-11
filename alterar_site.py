import os
import re

def alterar_site():
    arquivo = "index.html"
    
    if not os.path.exists(arquivo):
        print("❌ Erro: index.html não encontrado.")
        return

    with open(arquivo, "r", encoding="utf-8") as f:
        html = f.read()

    print("--- 1. MUDAR SLOGAN ---")
    print("Dica: Copie o texto exato do slogan antigo que está no seu site.")
    slogan_antigo = input("Slogan ANTIGO: ")
    slogan_novo = input("Slogan NOVO: ")
    
    if slogan_antigo in html:
        html = html.replace(slogan_antigo, slogan_novo)
        print("✅ Slogan atualizado!")
    else:
        print("⚠️ Slogan antigo não encontrado. Nenhuma alteração feita no texto.")

    print("\n--- 2. DELETAR SEÇÃO IDENTIDADE VISUAL ---")
    # Procura as âncoras para apagar o bloco
    inicio_secao = html.find("Identidade Visual")
    fim_secao = html.find("Publicação Direta no GitHub")

    if inicio_secao != -1 and fim_secao != -1 and inicio_secao < fim_secao:
        # Encontra a tag <div> que abre a seção
        tag_inicio = html.rfind("<div", 0, inicio_secao)
        # Encontra a tag <div> que abre a próxima seção
        tag_fim = html.rfind("<div", 0, fim_secao)
        
        # Corta o HTML para remover o bloco
        html = html[:tag_inicio] + "\n<!-- Seção Identidade Visual removida -->\n" + html[tag_fim:]
        print("✅ Seção 'Identidade Visual & Design' deletada!")
    else:
        print("⚠️ Não foi possível localizar a seção para deletar. Verifique manualmente.")

    print("\n--- 3. ADICIONAR CAMPO FOTO DO SLOGAN ---")
    novo_campo = """
    <div class="form-group" style="margin-bottom: 15px; margin-top: 15px;">
        <label style="font-weight: bold; display: block; margin-bottom: 5px;">URL da Foto do Slogan</label>
        <input type="url" name="foto_slogan" placeholder="https://exemplo.com/sua-foto.jpg" style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
    </div>
    """
    
    # Insere o campo antes da seção do GitHub
    idx_github = html.find("Publicação Direta no GitHub")
    if idx_github != -1:
        tag_insercao = html.rfind("<div", 0, idx_github)
        html = html[:tag_insercao] + novo_campo + html[tag_insercao:]
        print("✅ Campo para 'Foto do Slogan' adicionado!")
    else:
        print("⚠️ Não foi possível achar o local para inserir o campo.")

    # Salvando o arquivo
    with open(arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    print("\n🎉 PRONTO! O arquivo index.html foi atualizado com sucesso.")

if __name__ == "__main__":
    alterar_site()
