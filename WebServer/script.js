function sanitizeInput(data) {
  return String(data).replace(/[&<>"']/g, c => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  })[c]);
}

async function displayMovieCatalog() {
  try {
    const response = await fetch('/api/filmes', { cache: 'no-store' });
    if (!response.ok) throw new Error(`Erro de rede: ${response.status}`);

    const movies = await response.json();
    const container = document.getElementById('listaFilmesContainer');

    if (!movies.length) {
      container.innerHTML = '<p>Nenhum filme cadastrado.</p>';
      return;
    }

    let tableHtml = `<table>
      <thead>
        <tr>
          <th>Título</th><th>Atores</th><th>Diretor</th><th>Ano</th><th>Gênero</th><th>Produtora</th><th>Sinopse</th><th>Ações</th>
        </tr>
      </thead>
      <tbody>`;

    movies.forEach((movie, i) => {
      tableHtml += `<tr>
        <td>${sanitizeInput(movie.nomeFilme)}</td>
        <td>${sanitizeInput(movie.atores||'')}</td>
        <td>${sanitizeInput(movie.diretor||'')}</td>
        <td>${sanitizeInput(movie.ano||'')}</td>
        <td>${sanitizeInput(movie.genero||'')}</td>
        <td>${sanitizeInput(movie.produtora||'')}</td>
        <td>${sanitizeInput(movie.sinopse||'')}</td>
        <td>
          <button class="button" onclick="window.location.href='/editar_filme.html?index=${i}'">Editar</button>
          <button class="buttonCancel" onclick="deleteMovie(${i})">Excluir</button>
        </td>
      </tr>`;
    });

    tableHtml += `</tbody></table>`;
    container.innerHTML = tableHtml;
  } catch (e) {
    document.getElementById('listaFilmesContainer').textContent = `Falha ao carregar: ${e.message}`;
  }
}

async function deleteMovie(index) {
  if (!confirm('Deseja excluir este filme?')) return;
  try {
    const res = await fetch(`/api/filmes/${index}`, { method: 'DELETE' });
    if (!res.ok) throw new Error(`Erro: ${res.status}`);
    displayMovieCatalog();
  } catch (e) {
    alert(`Erro ao excluir: ${e.message}`);
  }
}

async function handleEditPage() {
  const index = new URLSearchParams(window.location.search).get('index');
  const form = document.getElementById('formularioEdicao');
  if (!form || index === null) return window.location.href='/listar_filmes.html';

  try {
    const res = await fetch(`/api/filmes/${index}`);
    if (!res.ok) throw new Error(`Erro ao carregar: ${res.status}`);
    const movie = await res.json();

    document.getElementById('movieIndex').value = index;
    ['nomeFilme','atores','diretor','ano','genero','produtora','sinopse'].forEach(id=>{
      const el = document.getElementById(id);
      if(el) el.value = movie[id]||'';
    });

    form.addEventListener('submit', async e=>{
      e.preventDefault();
      const data = {};
      ['nomeFilme','atores','diretor','ano','genero','produtora','sinopse'].forEach(id=>{
        data[id] = document.getElementById(id).value;
      });

      try {
        const putRes = await fetch(`/api/filmes/${index}`,{
          method:'PUT',
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify(data)
        });
        if(!putRes.ok) throw new Error(`Erro: ${putRes.status}`);
        window.location.href='/listar_filmes.html';
      } catch(err){ alert(err.message); }
    });

  } catch(e){ window.location.href='/listar_filmes.html'; }
}

document.addEventListener('DOMContentLoaded', ()=>{
  if(document.getElementById('listaFilmesContainer')) displayMovieCatalog();
  if(document.getElementById('formularioEdicao')) handleEditPage();
});
