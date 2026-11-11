async function enviarImagemParaGitHub(arquivo) {
    const config = JSON.parse(localStorage.getItem('@zixlima_config') || '{}');
    if (!config.githubToken) throw new Error("Configure o Token do GitHub na aba Configurações!");

    const base64String = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(arquivo);
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = error => reject(error);
    });

    const extensao = arquivo.name.split('.').pop();
    const nomeArquivo = `produto-${Date.now()}.${extensao}`;
    const caminhoNoRepo = `imagens/${nomeArquivo}`;
    const urlAPI = `https://api.github.com/repos/${config.githubUser}/${config.githubRepo}/contents/${caminhoNoRepo}`;

    const resposta = await fetch(urlAPI, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${config.githubToken}`,
            'Accept': 'application/vnd.github+json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: `Upload de imagem: ${nomeArquivo}`,
            content: base64String
        })
    });

    if (!resposta.ok) {
        const erro = await resposta.json();
        throw new Error(erro.message);
    }
    const dados = await resposta.json();
    return dados.content.download_url;
}

document.addEventListener('DOMContentLoaded', () => {
    const originalSalvarConfig = window.salvarConfiguracoes;
    window.salvarConfiguracoes = function() {
        if (originalSalvarConfig) originalSalvarConfig();
        let config = JSON.parse(localStorage.getItem('@zixlima_config') || '{}');
        config.githubUser = document.getElementById('config-github-user')?.value || '';
        config.githubRepo = document.getElementById('config-github-repo')?.value || '';
        config.githubToken = document.getElementById('config-github-token')?.value || '';
        localStorage.setItem('@zixlima_config', JSON.stringify(config));
    };

    const originalSalvarProduto = window.salvarProduto;
    window.salvarProduto = async function() {
        const inputFoto = document.getElementById('produto-imagem-file');
        const arquivoFoto = inputFoto ? inputFoto.files[0] : null;
        let urlDaImagem = "";

        if (arquivoFoto) {
            try {
                const btn = document.querySelector('button[onclick*="salvarProduto"]') || document.querySelector('button[onclick*="salvarOS"]');
                if (btn) { btn.innerText = "Enviando foto..."; btn.disabled = true; }
                
                urlDaImagem = await enviarImagemParaGitHub(arquivoFoto);
                
                if (btn) { btn.innerText = "Salvar"; btn.disabled = false; }
            } catch (erro) {
                alert("Erro ao enviar foto: " + erro.message);
                const btn = document.querySelector('button[onclick*="salvarProduto"]');
                if (btn) { btn.innerText = "Salvar"; btn.disabled = false; }
                return;
            }
        }

        const inputAntigo = document.querySelector('input[id*="imagem"]:not([type="file"])');
        if (inputAntigo) inputAntigo.value = urlDaImagem;
        
        if (originalSalvarProduto) await originalSalvarProduto();
    };
});
