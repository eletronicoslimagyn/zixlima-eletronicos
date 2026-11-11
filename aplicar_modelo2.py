import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("⏳ Aplicando Modelo 2 (Clean & Trust) e novo Slogan...")

# 1. Atualizar o Slogan
html = html.replace("Sua tecnologia em boas mãos.", "Proteção e qualidade para a sua tecnologia.")

# 2. Deixar o topo (Navbar) clean (fundo branco, texto escuro) mantendo a funcionalidade
html = html.replace(
    '<nav class="bg-gradient-lima text-white shadow-lg sticky top-0 z-40 px-4 py-3">',
    '<nav class="bg-white text-slate-800 shadow-sm border-b border-slate-200 sticky top-0 z-40 px-4 py-3">'
)
html = html.replace(
    '<span class="block text-[10px] md:text-xs text-orange-200 font-semibold tracking-wider uppercase mt-0.5">',
    '<span class="block text-[10px] md:text-xs text-orange-500 font-bold tracking-wider uppercase mt-0.5">'
)

# 3. Injetar o Formulário de Orçamento (Modelo 2) logo após o cabeçalho de boas-vindas
alvo_form = r'<!-- BALÃO COMPACTADO -->.*?</header>'
novo_form = '''<!-- BALÃO COMPACTADO -->
            <header class="bg-white/90 backdrop-blur-sm border border-gray-200 py-3 px-3 text-center mx-3 my-3 rounded-lg shadow-sm">
                <div class="max-w-2xl mx-auto">
                    <span class="bg-orange-100 text-orange-700 font-black text-[10px] px-2.5 py-0.5 rounded-full uppercase tracking-wider">Produtos Novos & Usados com Garantia</span>
                    <h2 class="text-xl md:text-2xl font-black text-blue-900 mt-1 mb-0.5">Assistência Técnica e Vendas</h2>
                    <p class="text-gray-600 text-xs leading-tight">Compre via WhatsApp ou solicite orçamento de manutenção para o seu aparelho.</p>
                </div>
            </header>

            <!-- NOVO FORMULÁRIO DE ORÇAMENTO (MODELO 2) -->
            <div class="max-w-2xl mx-auto my-6 px-4">
                <div class="bg-white p-6 rounded-2xl shadow-xl border border-slate-100">
                    <h3 class="text-2xl font-black text-slate-800 mb-4 text-center">Peça seu Orçamento</h3>
                    <form onsubmit="enviarOrcamento(event)" class="space-y-4">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Aparelho</label>
                                <select id="tipo-orcamento" class="w-full bg-slate-50 border border-slate-300 rounded-xl p-3 text-slate-800 outline-none focus:ring-2 focus:ring-blue-500 transition">
                                    <option value="Computador / Notebook">Computador / Notebook</option>
                                    <option value="Celular / Smartphone">Celular / Smartphone</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1">Marca e Modelo</label>
                                <input type="text" id="modelo-orcamento" placeholder="Ex: iPhone 13, Notebook Acer" class="w-full bg-slate-50 border border-slate-300 rounded-xl p-3 text-slate-800 outline-none focus:ring-2 focus:ring-blue-500 transition" required>
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-1">Descreva o problema</label>
                            <textarea id="defeito-orcamento" rows="2" placeholder="Ex: Tela quebrada, não liga, está lento..." class="w-full bg-slate-50 border border-slate-300 rounded-xl p-3 text-slate-800 outline-none focus:ring-2 focus:ring-blue-500 transition" required></textarea>
                        </div>
                        <button type="submit" class="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-xl transition shadow-lg text-md mt-2">
                            <i class="fa-brands fa-whatsapp mr-2"></i>Solicitar Orçamento no WhatsApp
                        </button>
                    </form>
                </div>
            </div>
'''
html = re.sub(alvo_form, novo_form, html, flags=re.DOTALL)

# 4. Adicionar a função JS que envia para o WhatsApp
js_orcamento = '''
        function enviarOrcamento(e) {
            e.preventDefault();
            const tipo = document.getElementById('tipo-orcamento').value;
            const modelo = document.getElementById('modelo-orcamento').value;
            const defeito = document.getElementById('defeito-orcamento').value;
            const texto = `Olá Zixlima! Vim pelo site e gostaria de um orçamento.\\n\\n*Equipamento:* ${tipo}\\n*Marca/Modelo:* ${modelo}\\n*Defeito:* ${defeito}`;
            window.open(`https://wa.me/5562982565827?text=${encodeURIComponent(texto)}`, '_blank');
        }
'''
html = html.replace("</script></body></html>", js_orcamento + "\n</script>\n</body>\n</html>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Site principal atualizado com o Modelo 2 e Slogan B!")
