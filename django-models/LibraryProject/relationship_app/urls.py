from django.urls import path
from . import views
from .views import (
    list_books, 
    register,
    LoginView,
    LogoutView,
    LibraryListView, 
    LibraryDetailView,
    admin_view,
    librarian_view,
    member_view,
)


urlpatterns = [
    # Library views
    path('books/', list_books, name='book-list'),
    path('library/', LibraryListView.as_view(), name='library-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    
    # Authentication views
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # Role-based access views
    path('admin/', admin_view, name='admin-view'),
    path('librarian/', librarian_view, name='librarian-view'),
    path('member/', member_view, name='member-view'),
]

