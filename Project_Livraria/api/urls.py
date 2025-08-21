from django.urls import path
from .views import *

# Crio os endpoints
urlpatterns = [
    path('autores/', AutoresView.as_view()),   # CRUD autores
    path('authors/', visualizacao_autor),      # rota extra
    path('editoras/', EditoraView.as_view()),
    path('livros/', LivroView.as_view()),

    path('autor/<int:pk>/', AutoresCrud.as_view()),
    path('editora/<int:pk>/', EditoraCrud.as_view()),
    path('livro/<int:pk>/', LivroCrud.as_view()),
]
