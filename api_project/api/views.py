from django.shortcuts import render
from .serializers import BookSerializer
from .models import Book
from rest_framework import generics, viewsets


# Create your views here.
class BookListListAPIView(generics.ListAPIView):
    '''
    gets the list of all books
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    ''' 
    handles all CRUD operations on the Book model
    '''
    quesryset = Book.objects.all()
    serializer_class = BookSerializer
