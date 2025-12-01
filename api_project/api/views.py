from django.shortcuts import render
from .serializers import BookSerializer
from .models import Book
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class BookListAPIView(generics.ListAPIView):
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
    permission_classes = [IsAuthenticated]
