(function() {
  const modal = document.getElementById('uploadModal');
  const btnAbrir = document.getElementById('btnAbrirUpload');
  if (!modal) return;
  btnAbrir.addEventListener('click', () => { modal.style.display = 'flex'; document.getElementById('uploadStatus').textContent = ''; });
  document.getElementById('btnCancelar').addEventListener('click', () => { modal.style.display = 'none'; });
  document.getElementById('fotoInput').addEventListener('change', function(e) {
    const reader = new FileReader();
    reader.onload = (ev) => { document.getElementById('fotoPreview').innerHTML = `<img src="${ev.target.result}" style="max-height:100px;">`; };
    reader.readAsDataURL(e.target.files[0]);
  });
  function comprimir(file, max=1200) {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          let w = img.width, h = img.height;
          if (w > max) { h = Math.round((h * max) / w); w = max; }
          canvas.width = w; canvas.height = h;
          canvas.getContext('2d').drawImage(img, 0, 0, w, h);
          canvas.toBlob((blob) => resolve(blob), 'image/jpeg', 0.8);
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  }
  document.getElementById('btnUpload').addEventListener('click', async function() {
    const file = document.getElementById('fotoInput').files[0];
    const nome = document.getElementById('fotoNome').value.trim();
    const token = document.getElementById('ghToken').value.trim() || sessionStorage.getItem('zixlima_gh_token');
    const status = document.getElementById('uploadStatus');
    if (!file || !nome || !token) { status.textContent = '❌ Preencha tudo.'; return; }
    const cfg = JSON.parse(localStorage.getItem('zixlima_config') || '{}');
    const owner = cfg.repoOwner || 'eletronicoslimagyn';
    const repo = cfg.repoNome || 'zixlima-eletronicos';
    const branch = cfg.branch || 'main';
    const pasta = cfg.pastaFotos || 'images/produtos';
    this.disabled = true; status.textContent = '⏳ Comprimindo...';
    try {
      const blob = await comprimir(file);
      const reader = new FileReader();
      reader.onload = async () => {
        const base64 = reader.result.split(',')[1];
        status.textContent = '⏳ Enviando para o GitHub...';
        const res = await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/${pasta}/${nome}.jpg`, {
          method: 'PUT',
          headers: { 'Authorization': `Bearer ${token}`, 'Accept': 'application/vnd.github+json' },
          body: JSON.stringify({ message: `Add foto: ${nome}`, content: base64, branch: branch })
        });
        if (res.ok) { status.innerHTML = '✅ Enviado!'; modal.style.display = 'none'; }
        else { const err = await res.json(); status.textContent = `❌ Erro: ${err.message}`; }
        this.disabled = false;
      };
      reader.readAsDataURL(blob);
    } catch (e) { status.textContent = '❌ Erro ao processar.'; this.disabled = false; }
  });
})();

