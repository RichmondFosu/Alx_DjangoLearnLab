from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
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

def register_view(request):
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


def login_view(request):
    """
    User login view.
    - GET: display the login form
    - POST: authenticate user and create a session
    
    How it works:
    1. User submits username and password
    2. Django authenticates the credentials against the database
    3. If valid, a session is created and stored in the database
    4. Session ID is sent to browser as a cookie
    5. On subsequent requests, Django uses the session ID to identify the user
    6. request.user contains the logged-in user object
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate credentials
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # User is valid, log them in (creates session)
            login(request, user)
            return redirect('book-list')
        else:
            # Invalid credentials
            error = "Invalid username or password"
            context = {'error': error}
            return render(request, 'relationship_app/login.html', context)
    
    return render(request, 'relationship_app/login.html')


def logout_view(request):
    """
    User logout view.
    - Deletes the session from the database
    - Clears the session cookie from the browser
    - User is no longer authenticated
    """
    logout(request)
    return redirect('book-list')


