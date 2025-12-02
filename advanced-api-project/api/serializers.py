from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    '''
    serializes book objects
    include custom validation to ensure that publication_year is not in the future
    '''
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']


        def validate_publication_year(self,value):
            '''
            ensure that a book cannot be published in the future
            '''
            current_year = datetime.now.year
            if value > current_year:
                raise serializers.ValidationError('Publicatoin year cannot be in the future')
            return value
        
class AuthorSerializer(serializers.ModelSerializer):
    '''
    serializes author objects
    includes nested serialization of all related books using BookSerialization
    '''

    books = BookSerializer(many=True, read_only=True)
    # uses related_name = 'books' from the Book model

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

        
