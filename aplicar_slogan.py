import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("⏳ Aplicando logo, slogan escolhido e Instagram...")

# 1. Troca a imagem base64 gigante pela sua nova logo local
html = re.sub(r'<img id="loja-perfil-img" src="data:image/jpeg;base64,[^"]+"', '<img id="loja-perfil-img" src="logo.jpg"', html)

# 2. Adiciona o Slogan escolhido (Opção 5) abaixo do nome
alvo_titulo = r'<h1 id="loja-titulo"[^>]*>.*?</h1>'
novo_titulo = '''<h1 id="loja-titulo" class="font-black text-base md:text-2xl tracking-tight leading-tight">ZIXLIMA ELETRÔNICOS</h1>
                            <span class="block text-[10px] md:text-xs text-orange-200 font-semibold tracking-wider uppercase mt-0.5">Sua tecnologia em boas mãos.</span>'''
html = re.sub(alvo_titulo, novo_titulo, html, flags=re.DOTALL)

# 3. Adiciona o Instagram no rodapé
alvo_footer = r'<p id="footer-nome"[^>]*>.*?</p>'
novo_footer = '''<p id="footer-nome" class="font-bold text-white mb-2">© 2026 ZIXLIMA ELETRÔNICOS. Todos os direitos reservados.</p>
                <a href="https://instagram.com/rodrigolima0901" target="_blank" class="inline-flex items-center gap-2 bg-gray-800 hover:bg-gray-700 text-pink-400 px-4 py-2 rounded-full text-xs font-bold transition mb-3 border border-gray-700 shadow-sm">
                    <i class="fa-brands fa-instagram text-base"></i> @rodrigolima0901
                </a>'''
html = re.sub(alvo_footer, novo_footer, html, flags=re.DOTALL)

# 4. Atualiza o título da aba do navegador
html = html.replace('<title>Eletrônicos Lima GYN | Vitrine & Gestão OS</title>', '<title>ZIXLIMA ELETRÔNICOS | Vitrine & Gestão OS</title>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ index.html atualizado com sucesso!")
