from rest_framework import serializers 
from .models import Autor, Editora, Livro


#serializer utilizado para gerar o dicionário JSON de Autor
class AutorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__' 

#serializer utilizado para gerar o dicionário JSON de Editora
class EditoraSerializers(serializers.ModelSerializer):
    class Meta:
        model = Editora
        fields = '__all__'

#serializer utilizado para gerar o dicionário JSON de Livro
class LivroSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Livro
        fields = '__all__'