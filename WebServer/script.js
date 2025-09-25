// função para não dar erro na conversão para mostrar no front

function escapeHtml(s) {
  // converter o valor para string
  return String(s).replace(
    /[&<>"']/g, // procurar pelos caracteres &, <, >, " e '
    c => ({// substituir por algumas coisas do HTML
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    })[c]
  );
}

// função para carregar e mostrar os filmes
async function load() {
  try {
    // fazer uma requisição GET para o arquivo filmes.json
    const resposta = await fetch('/api/filmes', { cache: 'no-store' });

    // mostra o erro se tiver algo incorreto
    if (!resposta.ok) throw new Error('Status ' + resposta.status);

    // converter o conteúdo da resposta dada para um arquivo JSON
    const filmes = await resposta.json();

    // pegar a div onde a lista será renderizada
    const div = document.getElementById('listarFilmes');

    // aparece caso não tiver nenhum filme cadastrado
    if (!filmes.length) {
      div.innerHTML = '<p>Nenhum filme cadastrado.</p>';
      return;
    }

    // formatação que os dados serão exibidos
    let html = `
      <table>
        <thead>
          <tr>
            <th>Título</th>
            <th>Atores</th>
            <th>Diretor</th>
            <th>Ano</th>
            <th>Gênero</th>
            <th>Produtora</th>
            <th>Sinopse</th>
          </tr>
        </thead>
        <tbody>
    `;

    // perocrrer cada filme e criar uma linha na tabela
    filmes.forEach(dado => {
      html += `
        <tr>
          <td>${escapeHtml(dado.titulo)}</td>
          <td>${escapeHtml(dado.atores || '')}</td>
          <td>${escapeHtml(dado.diretor || '')}</td>
          <td>${escapeHtml(dado.ano || '')}</td>
          <td>${escapeHtml(dado.genero || '')}</td>
          <td>${escapeHtml(dado.produtora || '')}</td>
          <td>${escapeHtml(dado.sinopse || '')}</td>
        </tr>
      `;
    });

    html += `
        </tbody>
      </table>
    `;

    // inserir a tabela pronta dentro da página
    div.innerHTML = html;

  } catch (erro) {
    // se der erro em qualquer parte
    document.getElementById('lista').textContent = 'Erro ao carregar filmes: ' + erro.message;
  }
}

load();