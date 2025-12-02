from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Book,Author
from .serializers import BookSerializer
from rest_framework.exceptions import ValidationError

# List View
class BookListView(generics.ListAPIView):
    '''
    returns a list of all books.
    this view is read-only, so permissions allow anyone to access it.
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny] #everyone can read

    def get_queryset(self):
        '''
        allow filtering by year
        '''
        queryset=Book.objects.all()
        year = self.request.query_params.get("year")
        if year:
            queryset = queryset.filter(publication_year=year)
        return queryset


# DetailView
class BookDetailView(generics.RetrieveAPIView):
    '''
    returns a single book by ID/pk.
    also read-only for general access.
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny] #everyone can read


class BookCreateView(generics.CreateAPIView):
    """
    Creates a new book.
    Only authenticated users can create books.
    Additional validation is automatically handled by the serializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        '''
        Hook to modify creation behavior if needed.
        For now, it just saves the serializer.
        '''
        title = serializer.validated_data['title']
        if Book.objects.filter(title=title).exists():
            raise ValidationError('A book with this title already exists.')
        serializer.save()


# <-------------------UPDATE VIEW ------------------->
class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing book.
    Only authenticated users can update.
    Supports PUT and PATCH.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        '''
        for custom update logic
        '''
        serializer.save()

# <------------DELETE VIEW---------->
class BookDeleteView(generics.DestroyAPIView):
    '''
    Deletes a book
    onlyb authenticated users can delete
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    

