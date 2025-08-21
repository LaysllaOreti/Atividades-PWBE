from django.shortcuts import render #Renderiza
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
 
#Importação do Serializer e Autor
from .models import Autor, Editora, Livro
from .serializers import AutorSerializers, EditoraSerializers,LivroSerializers
 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
 
#Serve como um post, e o list como get
class AutoresView(ListCreateAPIView):
    #query é um tipo de busca
    #set envia
    queryset = Autor.objects.all() #Aquilo que o usuário verá, no caso todos os objetos dentro da classe Autor
    serializer_class = AutorSerializers
 
class AutoresCrud(RetrieveUpdateDestroyAPIView): #Realize o método do CRUD dentro da API
    queryset = Autor.objects.all()
    serializer_class = AutorSerializers #Quando buscados vem em forma de JSON
 
#Método do CRUD dos autores
@api_view(['GET', 'POST'])
def visualizacao_autor(request):
    if request.method == 'GET':
        queryset = Autor.objects.all()
        serializer = AutorSerializers(queryset, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AutorSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
       
 
#Método para GET, PUT e DELETE      
@api_view(['GET', 'PUT', 'DELETE'])
def detalhes_autores(request,pk):
 
    autor = Autor.objects.get(pk=pk)
   
    if request.method == 'GET':
        serializer = AutorSerializers(autor)
        return Response(serializer.data)
   
    elif request.method == 'PUT':
        serializer = AutorSerializers(autor, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
       
    elif request.method == 'DELETE':
        autor.delete()
        if serializer.is_valid():
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
       
 
class EditoraView(ListCreateAPIView):
    queryset = Editora.objects.all()
    serializer_class = EditoraSerializers #Quando buscados vem em forma de JSON
 
class EditoraCrud(RetrieveUpdateDestroyAPIView):
    queryset = Editora.objects.all()
    serializer_class = EditoraSerializers
 
#Método do CRUD dos editora
@api_view(['GET', 'POST'])
def visualizar_editora(request):
    if request.method == 'GET':
        queryset = Editora.objects.all()
        serializer = EditoraSerializers(queryset, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EditoraSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
       
 
#Método para GET, PUT e DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def detalhes_editoras(request,pk):
 
    editora = Editora.objects.get(pk=pk)
   
    if request.method == 'GET':
        serializer = EditoraSerializers(editora)
        return Response(serializer.data)
   
    elif request.method == 'PUT':
        serializer = EditoraSerializers(editora, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
       
    elif request.method == 'DELETE':
        editora.delete()
        if serializer.is_valid():
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
 
 
 
 
class LivroView(ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializers #Quando buscados vem em forma de JSON
 
class LivroCrud(RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializers
 
#Método do CRUD dos autores
@api_view(['GET', 'POST'])
def visualizacao_livro(request):
    if request.method == 'GET':
        queryset = Livro.objects.all()
        serializer = LivroSerializers(queryset, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LivroSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
       
#Método para GET, PUT e DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def detalhes_livros(request,pk):
 
    livro = Livro.objects.get(pk=pk)
   
    if request.method == 'GET':
        serializer = LivroSerializers(livro)
        return Response(serializer.data)
   
    elif request.method == 'PUT':
        serializer = LivroSerializers(livro, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
       
    elif request.method == 'DELETE':
        livro.delete()
        if serializer.is_valid():
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)