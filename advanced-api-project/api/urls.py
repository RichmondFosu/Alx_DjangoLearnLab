from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookDeleteView,
    BookUpdateView,
)
from .auth_views import RegisterView, LoginView,LogoutView

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    path("books/<int:pk>/update", BookUpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete", BookDeleteView.as_view(), name='book-delete'),
    path("register/", RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

