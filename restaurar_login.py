import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Restaurar o window.onload original (com verificação de login)
current_onload_pattern = r"window\.onload = \(\) => \{[\s\S]*?// AUTO LOGIN ADMIN \(Sem senha\)[\s\S]*?\};"
original_onload = """window.onload = () => {
            loadConfigToUI();
            populateSelects();
            document.getElementById('loginCompanyName').innerText = config.compName;
            if (currentUser) {
                showApp();
            } else {
                showLogin();
            }
        };"""
html = re.sub(current_onload_pattern, lambda m: original_onload, html)

# 2. Restaurar o botão de Sair (logout) no cabeçalho
if 'onclick="logout()"' not in html:
    logout_btn = """<button onclick="logout()" class="px-3 py-2 rounded-md text-sm font-medium transition text-red-300 hover:bg-red-600 hover:text-white" title="Sair">
                        <i class="fas fa-sign-out-alt"></i>
                    </button>
                </nav>"""
    # Procura o fechamento da tag nav e insere o botão antes
    html = html.replace('</nav>', logout_btn, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("\n✅ Tela de Login do Admin RESTAURADA!")
print("✅ A melhoria de envio da OS pelo WhatsApp foi MANTIDA.")
