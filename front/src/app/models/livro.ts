export interface Livro {
  id: number;
  titulo: string;
  subtitulo: string;
  autor: number; // para puxar o ID
  editor: number; // para puxar o ID
  isbn: string;
  descricao: string;
  idioma: string;
  ano_publicacao: number;
  paginas: string;
  preco: number;
  estoque: number;
  disponivel: boolean;
  dimensoes: string;
  peso: number;
}
