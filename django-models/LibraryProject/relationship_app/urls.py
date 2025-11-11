from django.urls import path
from .views import (
    list_books, 
    LibraryListView, 
    LibraryDetailView,
    register_view,
    login_view,
    logout_view
)


urlpatterns = [
    # Library views
    path('books/', list_books, name='book-list'),
    path('library/', LibraryListView.as_view(), name='library-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    
    # Authentication views
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

