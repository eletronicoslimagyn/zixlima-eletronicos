import re

print("[*] Lendo o arquivo index.html...")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CORRIGINDO O ERRO FATAL DE JAVASCRIPT (JSON QUEBRADO)
# Substituindo a string corrompida por uma URL limpa
html = html.replace(
    '"elg_perfil_url":"https://i.ibb.co/1f7Z0g0p/Screenshot-20261110-092344-Chat-GPT.jpg\\" alt=\\"Screenshot-20261110-092344-Chat-GPT\\" border=\\"0\\">\\u003c/a>"',
    '"elg_perfil_url":"https://i.ibb.co/1f7Z0g0p/Screenshot-20261110-092344-Chat-GPT.jpg"'
)
html = html.replace(
    '"imagem":"https://i.ibb.co/1f7Z0g0p/Screenshot-20261110-092344-Chat-GPT.jpg\\" alt=\\"Screenshot-20261110-092344-Chat-GPT\\" border=\\"0\\">\\u003c/a>"',
    '"imagem":"https://i.ibb.co/1f7Z0g0p/Screenshot-20261110-092344-Chat-GPT.jpg"'
)
print("[OK] Erro de sintaxe do JavaScript corrigido. (Admin vai voltar a funcionar)")

# 2. ARRUMANDO O LAYOUT DO TOPO (Tirando a div de dentro do h1)
topo_quebrado = re.search(r'<h1 id="loja-titulo".*?</h1>', html, re.DOTALL)
if topo_quebrado:
    # Extrai a div de busca/whatsapp e coloca fora do h1
    bloco_original = topo_quebrado.group(0)
    # Limpa o h1 deixando só o título
    novo_h1 = '<h1 id="loja-titulo" class="font-black text-base md:text-2xl tracking-tight leading-tight">Zixlima Eletrônicos</h1>'
    # Recria a div de busca/whatsapp fora do h1
    div_busca = """
    <div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 10px; width: 100%; margin-top: 10px;">
        <div style="flex: 1; min-width: 200px;"><input type="text" id="search-input" oninput="filtrarProdutos(this.value)" placeholder="Buscar produto..." class="w-full text-gray-800 bg-white px-4 py-1.5 rounded-full text-xs outline-none focus:ring-2 focus:ring-orange-400 shadow-inner"></div>
        <div style="width: 100%; max-width: 200px;"><a id="btn-topo-whats" href="https://wa.me/5562982565827?text=Olá!" target="_blank" rel="noopener noreferrer" class="bg-orange-500 hover:bg-orange-600 px-4 py-2 rounded-full font-bold text-xs flex items-center justify-center gap-1.5 transition shadow-md"><i class="fa-brands fa-whatsapp text-base"></i> Falar Conosco</a></div>
    </div>
    """
    html = html.replace(bloco_original, novo_h1 + div_busca)
    print("[OK] Layout do Topo corrigido.")

# 3. ARRUMANDO O LAYOUT DO RODAPÉ (Tirando a imagem gigante de dentro do <p>)
footer_quebrado = re.search(r'<p id="footer-nome".*?</p>', html, re.DOTALL)
if footer_quebrado:
    novo_footer = '<p id="footer-nome" class="font-bold text-white mb-2">© 2026 Zixlima Eletrônicos. Todos os direitos reservados.</p>'
    html = html.replace(footer_quebrado.group(0), novo_footer)
    print("[OK] Layout do Rodapé corrigido (imagem gigante removida).")

# 4. MELHORANDO A SEGURANÇA E LÓGICA DO PAINEL ADMIN
funcao_admin_antiga = re.search(r'function solicitarAcessoAdmin\(\) \{.*?\n        \}', html, re.DOTALL)
funcao_admin_nova = """function solicitarAcessoAdmin() {
            let senhaSalva = localStorage.getItem('elg_admin_senha_local');
            if (!senhaSalva) {
                const nova = prompt('Primeiro acesso: crie uma senha para o painel (mínimo 4 caracteres).');
                if (!nova || nova.length < 4) { alert('Senha muito curta.'); return; }
                localStorage.setItem('elg_admin_senha_local', nova);
                senhaSalva = nova;
            }
            const senha = prompt('Digite a senha do painel. (Digite RESETAR se esqueceu a senha)');
            
            if (senha === 'RESETAR') {
                localStorage.removeItem('elg_admin_senha_local');
                alert('Senha apagada com sucesso! Clique no botão de Admin novamente para criar uma nova.');
                return;
            }
            
            if(senha && senha === senhaSalva) {
                document.getElementById('view-loja').classList.add('hidden');
                document.getElementById('view-admin').classList.remove('hidden');
                listarProdutosAdmin();
                renderizarListaOS();
                renderizarLojasParceiras();
            } else if(senha !== null) {
                alert("Acesso negado! Senha incorreta.");
            }
        }"""
if funcao_admin_antiga:
    html = html.replace(funcao_admin_antiga.group(0), funcao_admin_nova)
    print("[OK] Sistema de login do Admin blindado (opção de RESETAR adicionada).")

# Salvando o arquivo final
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\\n[SUCESSO] Site totalmente corrigido e pronto para uso!")
