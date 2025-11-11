from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Library, Book
from .forms import CustomUserCreationForm

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

# backward-compatible alias expected by some exercises/tests
def list_books(request):
    return book_list(request)

class LibraryListView(ListView):
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'

class LibraryDetailView(DetailView):
        model = Library
        template_name = 'relationship_app/library_detail.html'
        context_object_name = 'library'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context


# ============ AUTHENTICATION VIEWS ============

def register(request):
    """
    User registration view.
    - GET: display the registration form
    - POST: process the form and create a new user
    
    How it works:
    1. User fills out username, email, password, password confirmation
    2. Form validates: passwords must match, username must be unique
    3. If valid, User is created and user is logged in automatically
    4. Redirect to home or dashboard
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            return redirect('book-list')  # redirect to books page
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'relationship_app/register.html', context)


# Django's built-in LoginView with custom template
class LoginView(DjangoLoginView):
    template_name = 'relationship_app/login.html'
    success_url = reverse_lazy('book-list')


# Django's built-in LogoutView with custom template
class LogoutView(DjangoLogoutView):
    template_name = 'relationship_app/logout.html'


