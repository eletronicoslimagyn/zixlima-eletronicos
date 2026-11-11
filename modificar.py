import re
with open('index.html', 'r', encoding='utf-8') as f: html = f.read()

# 1. Inputs GitHub
input_github = """
<div class="mb-3">
    <label class="block text-sm font-medium text-gray-700">Usuário do GitHub</label>
    <input type="text" id="config-github-user" class="mt-1 block w-full border border-gray-300 rounded-md p-2">
</div>
<div class="mb-3">
    <label class="block text-sm font-medium text-gray-700">Repositório do GitHub</label>
    <input type="text" id="config-github-repo" class="mt-1 block w-full border border-gray-300 rounded-md p-2">
</div>
<div class="mb-3">
    <label class="block text-sm font-medium text-gray-700">Token do GitHub</label>
    <input type="password" id="config-github-token" class="mt-1 block w-full border border-gray-300 rounded-md p-2">
</div>
"""
if 'id="config-github-user"' not in html:
    if 'id="config-logo"' in html:
        html = re.sub(r'(<input[^>]*id="config-logo"[^>]*>)', r'\1\n' + input_github, html)
    else:
        html = re.sub(r'(<button[^>]*onclick="salvarConfiguracoes\(\)"[^>]*>)', input_github + r'\n\1', html)

# 2. Input File
novo_input_file = '<input type="file" id="produto-imagem-file" accept="image/*" class="mt-1 block w-full border border-gray-300 rounded-md p-2 bg-white">'
if 'produto-imagem-file' not in html:
    html = re.sub(r'(<label[^>]*>URL da Imagem</label>\s*)<input[^>]*>', r'\1' + novo_input_file, html, flags=re.IGNORECASE)
    if 'produto-imagem-file' not in html:
        html = re.sub(r'<input[^>]*id="produto-imagem"[^>]*>', novo_input_file, html)
        html = re.sub(r'URL da Imagem', 'Foto do Produto', html, flags=re.IGNORECASE)

# 3. Adicionar o Script
if 'upload.js' not in html:
    html = html.replace('</body>', '<script src="upload.js"></script>\n</body>')

with open('index.html', 'w', encoding='utf-8') as f: f.write(html)
print("\n✅ index.html modificado com sucesso! Pode ir para a Parte 3.")
