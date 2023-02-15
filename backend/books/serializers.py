from rest_framework import serializers
from .models import Book, BookRank

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRank
        fields = '__all__'
        read_only_fields = ['isbn']