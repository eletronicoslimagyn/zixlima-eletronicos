import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remover a tela de login (Auto-login direto para o Dashboard)
old_onload_pattern = r"window\.onload = \(\) => \{[\s\S]*?if \(currentUser\) \{[\s\S]*?showApp\(\);[\s\S]*?\} else \{[\s\S]*?showLogin\(\);[\s\S]*?\}[\s\S]*?\};"
new_onload = """window.onload = () => {
            loadConfigToUI();
            populateSelects();
            // AUTO LOGIN ADMIN (Sem senha)
            currentUser = 'Administrador';
            sessionStorage.setItem('loggedUser', currentUser);
            document.getElementById('headerCompanyName').innerText = config.compName;
            switchTab('dashboard');
            document.getElementById('loginScreen').classList.add('hidden');
            document.getElementById('mainApp').classList.remove('hidden');
        };"""
# Usando lambda para evitar erro de escape (\%)
html = re.sub(old_onload_pattern, lambda m: new_onload, html)

# 2. Remover o botão de logout (Sair) para não bugar a tela
html = re.sub(r'<button onclick="logout\(\)"[^>]*>[\s\S]*?<\/button>', '', html)

# 3. Melhorar a função do WhatsApp
old_wa_pattern = r"function sendWhatsApp\(id\) \{[\s\S]*?window\.open\(url, '_blank'\);\s*\}"
new_wa = """function sendWhatsApp(id) {
            const os = osList.find(o => o.id == id);
            if (!os) return;
            
            const phoneClean = os.phone.replace(/\\D/g, '');
            
            let text = `*${config.compName}*\\n`;
            text += `-----------------------------------\\n`;
            text += `Olá *${os.client}*, aqui está o resumo da sua OS *#${os.id}*:\\n\\n`;
            text += `📱 *Aparelho:* ${os.device}\\n`;
            text += `🔧 *Tipo:* ${os.type}\\n`;
            text += `⚠️ *Defeito:* ${os.problem}\\n`;
            if(os.service) text += `🛠️ *Serviço a Executar:* ${os.service}\\n`;
            text += `🛡️ *Garantia:* ${os.warranty}\\n`;
            text += `📌 *Status:* ${os.status}\\n`;
            text += `💰 *Valor Total:* R$ ${parseFloat(os.total).toFixed(2)}\\n\\n`;
            
            if(config.compPixKey) {
                text += `💳 *Pagamento via Pix:*\\nChave: *${config.compPixKey}*\\n\\n`;
            }
            
            text += `Agradecemos a preferência!\\n`;
            text += `-----------------------------------\\n`;
            text += `*${config.compName}*\\n`;
            text += `📞 Contato: ${config.compPhone || config.compWhatsapp}\\n`;

            const url = `https://api.whatsapp.com/send?phone=55${phoneClean}&text=${encodeURIComponent(text)}`;
            window.open(url, '_blank');
        }"""
html = re.sub(old_wa_pattern, lambda m: new_wa, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("\n✅ Sistema atualizado: Login removido e WhatsApp melhorado!")
