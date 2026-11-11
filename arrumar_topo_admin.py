import re

print("[*] Lendo o arquivo index.html...")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. LIMPANDO O LIXO DO JAVASCRIPT (Faz o Admin voltar a funcionar)
# Remove o texto quebrado que estava colado na URL da foto de perfil
html = html.replace('\\" alt=\\"Screenshot-20261110-092344-Chat-GPT\\" border=\\"0\\">\\u003c/a>', '')
html = html.replace('" alt="Screenshot-20261110-092344-Chat-GPT" border="0"></a>', '')
# Remove também a sujeira da imagem da loja parceira
html = html.replace('\\" alt=\\"Screenshot-20261110-092344-Chat-GPT\\" border=\\"0\\">\\u003c/a>', '')
print("[OK] Erro no JavaScript corrigido. O botão Admin voltará a funcionar.")

# 2. RECONSTRUINDO O PAINEL SUPERIOR (Deixando responsivo e alinhado)
novo_topo = '''<nav class="bg-white text-slate-800 shadow-sm border-b border-slate-200 sticky top-0 z-40 px-4 py-3">
                <div class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
                    
                    <!-- Foto, Título e Subtítulo -->
                    <div class="flex items-center gap-3 w-full md:w-auto">
                        <img id="loja-perfil-img" src="logo.jpg" class="profile-img bg-gray-200 shadow-sm" referrerpolicy="no-referrer" style="width: 64px; height: 64px; object-fit: cover; border-radius: 50%; border: 2px solid #e2e8f0;">
                        <div class="min-w-0">
                            <h1 id="loja-titulo" class="font-black text-lg md:text-2xl tracking-tight leading-tight">Zixlima Eletrônicos</h1>
                            <span class="block text-[10px] md:text-xs text-orange-500 font-bold tracking-wider uppercase mt-0.5">Proteção e qualidade para a sua tecnologia.</span>
                            <span id="loja-documento-topo" class="text-[11px] text-gray-500 font-mono block mt-0.5">CNPJ: 54.449.263/0001-01</span>
                        </div>
                    </div>
                    
                    <!-- Barra de Busca e Botão WhatsApp -->
                    <div class="flex flex-wrap items-center gap-2 w-full md:w-auto md:max-w-md">
                        <div class="flex-1 min-w-[150px]">
                            <input type="text" id="search-input" oninput="filtrarProdutos(this.value)" placeholder="Buscar produto..." class="w-full text-gray-800 bg-gray-50 px-4 py-2 rounded-full text-xs outline-none focus:ring-2 focus:ring-orange-400 border border-gray-200 shadow-inner">
                        </div>
                        <div>
                            <a id="btn-topo-whats" href="https://wa.me/5562982565827?text=Olá!" target="_blank" rel="noopener noreferrer" class="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-full font-bold text-xs flex items-center justify-center gap-1.5 transition shadow-md whitespace-nowrap">
                                <i class="fa-brands fa-whatsapp text-base"></i> Falar Conosco
                            </a>
                        </div>
                    </div>
                    
                </div>
            </nav>'''

# Substitui a bagunça antiga pelo novo topo arrumado
html = re.sub(r'<nav class="bg-white.*?</nav>', novo_topo, html, flags=re.DOTALL)
print("[OK] Painel superior reconstruído e alinhado.")

# 3. SALVANDO O ARQUIVO
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n[SUCESSO] Site corrigido com sucesso!")
