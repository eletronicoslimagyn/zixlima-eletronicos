(function() {
  const abas = document.querySelectorAll('.admin-tab');
  const paineis = document.querySelectorAll('.admin-painel');
  function ativarAba(nome) {
    abas.forEach(b => b.classList.toggle('ativo', b.dataset.aba === nome));
    paineis.forEach(p => p.classList.toggle('ativo', p.id === 'aba-' + nome));
    localStorage.setItem('zixlima_aba_ativa', nome);
  }
  abas.forEach(btn => btn.addEventListener('click', () => ativarAba(btn.dataset.aba)));
  const abaSalva = localStorage.getItem('zixlima_aba_ativa');
  if (abaSalva && document.getElementById('aba-' + abaSalva)) ativarAba(abaSalva);

  const formPerfil = document.getElementById('formPerfil');
  const perfilStatus = document.getElementById('perfilStatus');
  const avatarPreview = document.getElementById('avatarPreview');
  const avatarInput = document.getElementById('avatarInput');
  const camposPerfil = { perfilNome:'nome', perfilEmail:'email', perfilTelefone:'telefone', perfilLoja:'loja', perfilBio:'bio' };

  function carregarPerfil() {
    const salvo = JSON.parse(localStorage.getItem('zixlima_perfil') || '{}');
    Object.entries(camposPerfil).forEach(([id, chave]) => {
      const el = document.getElementById(id);
      if (el && salvo[chave]) el.value = salvo[chave];
    });
    if (salvo.avatar) avatarPreview.innerHTML = `<img src="${salvo.avatar}">`;
  }
  formPerfil.addEventListener('submit', (e) => {
    e.preventDefault();
    const dados = {};
    Object.entries(camposPerfil).forEach(([id, chave]) => {
      const el = document.getElementById(id);
      if (el) dados[chave] = el.value.trim();
    });
    const atual = JSON.parse(localStorage.getItem('zixlima_perfil') || '{}');
    if (atual.avatar) dados.avatar = atual.avatar;
    localStorage.setItem('zixlima_perfil', JSON.stringify(dados));
    perfilStatus.textContent = '✅ Perfil salvo!';
    setTimeout(() => perfilStatus.textContent = '', 3000);
  });
  avatarInput.addEventListener('change', (e) => {
    const reader = new FileReader();
    reader.onload = (ev) => {
      avatarPreview.innerHTML = `<img src="${ev.target.result}">`;
      const perfil = JSON.parse(localStorage.getItem('zixlima_perfil') || '{}');
      perfil.avatar = ev.target.result;
      localStorage.setItem('zixlima_perfil', JSON.stringify(perfil));
    };
    reader.readAsDataURL(e.target.files[0]);
  });
  document.getElementById('btnLimparPerfil').addEventListener('click', () => {
    if (confirm('Apagar perfil?')) { localStorage.removeItem('zixlima_perfil'); formPerfil.reset(); avatarPreview.innerHTML = '👤'; }
  });
  carregarPerfil();

  const formConfig = document.getElementById('formConfig');
  const camposConfig = { cfgRepoOwner:'repoOwner', cfgRepoNome:'repoNome', cfgBranch:'branch', cfgPastaFotos:'pastaFotos', cfgTema:'tema' };
  function carregarConfig() {
    const salvo = JSON.parse(localStorage.getItem('zixlima_config') || '{}');
    Object.entries(camposConfig).forEach(([id, chave]) => {
      if (salvo[chave]) document.getElementById(id).value = salvo[chave];
    });
    if (salvo.tema === 'escuro') document.body.classList.add('tema-escuro');
    if (sessionStorage.getItem('zixlima_gh_token')) document.getElementById('cfgToken').value = sessionStorage.getItem('zixlima_gh_token');
  }
  formConfig.addEventListener('submit', (e) => {
    e.preventDefault();
    const dados = {};
    Object.entries(camposConfig).forEach(([id, chave]) => { dados[chave] = document.getElementById(id).value.trim(); });
    localStorage.setItem('zixlima_config', JSON.stringify(dados));
    const token = document.getElementById('cfgToken').value.trim();
    if (token) sessionStorage.setItem('zixlima_gh_token', token);
    document.body.classList.toggle('tema-escuro', dados.tema === 'escuro');
    document.getElementById('configStatus').textContent = '✅ Configurações salvas!';
    setTimeout(() => document.getElementById('configStatus').textContent = '', 3000);
  });
  carregarConfig();
})();

