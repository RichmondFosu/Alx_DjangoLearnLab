from django.urls import path
from .views import list_books, LibraryListView, LibraryDetailView


urlpatterns = [
    path('books/', list_books, name='book-list'),
    path('library/', LibraryListView.as_view(), name='library-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]

