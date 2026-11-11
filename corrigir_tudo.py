import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("⏳ Corrigindo inputs de preços e botões de upload...")

# 1. Permitir vírgula nos preços (muda de type="number" para type="text")
html = html.replace('type="number" id="novo-preco" step="0.01"', 'type="text" inputmode="decimal" id="novo-preco"')
html = html.replace('type="number" id="edit-preco" step="0.01"', 'type="text" inputmode="decimal" id="edit-preco"')
html = html.replace('type="number" step="0.01" id="os-valor"', 'type="text" inputmode="decimal" id="os-valor"')

# 2. Ajustar o JavaScript para aceitar vírgula nos cálculos
html = html.replace(
    "parseFloat(document.getElementById('novo-preco').value)",
    "parseFloat((document.getElementById('novo-preco').value || '0').replace(',', '.'))"
)
html = html.replace(
    "parseFloat(document.getElementById('edit-preco').value)",
    "parseFloat((document.getElementById('edit-preco').value || '0').replace(',', '.'))"
)
html = html.replace(
    "Number(document.getElementById('os-valor').value)",
    "parseFloat((document.getElementById('os-valor').value || '0').replace(',', '.'))"
)

# 3. Injetar botão de upload no formulário "Novo Item"
alvo_novo = r'<input type="url" id="novo-imagem"[^>]*>'
novo_campo = '''<div class="flex gap-2">
            <input type="url" id="novo-imagem" class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm outline-none" placeholder="Cole a URL ou envie do celular..." required="">
            <button type="button" onclick="document.getElementById('novo-imagem-file').click()" class="bg-gray-200 hover:bg-gray-300 px-3 rounded-lg text-sm font-bold text-gray-700 whitespace-nowrap transition shadow-sm"><i class="fa-solid fa-mobile-screen"></i> Enviar</button>
            <input type="file" id="novo-imagem-file" accept="image/*" hidden onchange="uploadFotoLocal(this, 'novo-imagem')">
            </div>
            <div id="novo-imagem-preview" class="mt-2 text-center hidden"><img src="" class="max-h-24 rounded-lg mx-auto border shadow-sm"></div>'''
html = re.sub(alvo_novo, novo_campo, html)

# 4. Injetar botão de upload no formulário "Editar Dispositivo"
alvo_edit = r'<input type="url" id="edit-imagem"[^>]*>'
edit_campo = '''<div class="flex gap-2">
            <input type="url" id="edit-imagem" class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm outline-none" required="">
            <button type="button" onclick="document.getElementById('edit-imagem-file').click()" class="bg-gray-200 hover:bg-gray-300 px-3 rounded-lg text-xs font-bold text-gray-700 whitespace-nowrap transition shadow-sm"><i class="fa-solid fa-mobile-screen"></i> Enviar</button>
            <input type="file" id="edit-imagem-file" accept="image/*" hidden onchange="uploadFotoLocal(this, 'edit-imagem')">
            </div>
            <div id="edit-imagem-preview" class="mt-2 text-center hidden"><img src="" class="max-h-20 rounded-lg mx-auto border shadow-sm"></div>'''
html = re.sub(alvo_edit, edit_campo, html)

# 5. Adicionar a função de Upload Local
js_code = '''
        // --- FUNÇÃO DE UPLOAD LOCAL PARA GITHUB ---
        async function uploadFotoLocal(input, inputId) {
            const file = input.files[0];
            if (!file) return;

            const token = sessionStorage.getItem('zixlima_gh_token') || document.getElementById('gh-token')?.value.trim();
            if (!token) {
                alert('⚠️ Para enviar fotos do celular, digite o Token do GitHub na aba "Configurações" primeiro.');
                return;
            }

            const nomeBase = 'img_' + Date.now();
            const inputUrl = document.getElementById(inputId);
            const previewDiv = document.getElementById(inputId + '-preview');
            const btn = input.previousElementSibling;
            const textoOriginalBtn = btn.innerHTML;

            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
            btn.disabled = true;

            try {
                const img = new Image();
                img.src = URL.createObjectURL(file);
                await new Promise(r => img.onload = r);
                
                const canvas = document.createElement('canvas');
                let w = img.width, h = img.height;
                if (w > 1000) { h = Math.round((h * 1000) / w); w = 1000; }
                canvas.width = w; canvas.height = h;
                canvas.getContext('2d').drawImage(img, 0, 0, w, h);
                const base64 = canvas.toDataURL('image/jpeg', 0.8).split(',')[1];

                const res = await fetch(`https://api.github.com/repos/eletronicoslimagyn/zixlima-eletronicos/contents/images/produtos/${nomeBase}.jpg`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Accept': 'application/vnd.github+json'
                    },
                    body: JSON.stringify({
                        message: `Upload foto: ${nomeBase}`,
                        content: base64,
                        branch: 'main'
                    })
                });

                if (res.ok) {
                    const data = await res.json();
                    inputUrl.value = data.content.download_url;
                    previewDiv.classList.remove('hidden');
                    previewDiv.querySelector('img').src = data.content.download_url;
                } else {
                    const err = await res.json();
                    alert('❌ Erro no GitHub: ' + (err.message || 'Erro desconhecido'));
                }
            } catch (error) {
                alert('❌ Erro ao enviar foto: ' + error.message);
            } finally {
                btn.innerHTML = textoOriginalBtn;
                btn.disabled = false;
                input.value = ''; 
            }
        }
'''
html = html.replace("</script></body></html>", js_code + "\n</script>\n</body>\n</html>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ index.html atualizado com os botões de envio e suporte a vírgula!")
