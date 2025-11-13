from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Library, Book, Author
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


# ============ ROLE-BASED ACCESS CONTROL ============

# Helper functions to check user roles
def is_admin(user):
    """
    Check if user is authenticated and has 'Admin' role.
    Returns True if user is an Admin, False otherwise.
    """
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'


def is_librarian(user):
    """
    Check if user is authenticated and has 'Librarian' role.
    Returns True if user is a Librarian, False otherwise.
    """
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'


def is_member(user):
    """
    Check if user is authenticated and has 'Member' role.
    Returns True if user is a Member, False otherwise.
    """
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'


# ============ ADMIN VIEW ============

@user_passes_test(is_admin)
def admin_view(request):
    """
    Admin-only view: restricted to users with 'Admin' role.
    
    Only admins can access this view. Other users will be redirected to login.
    This view displays admin controls and information.
    """
    context = {
        'message': 'Welcome Admin! You have full access to all features.',
        'role': request.user.profile.role,
    }
    return render(request, 'relationship_app/admin_view.html', context)


# ============ LIBRARIAN VIEW ============

@user_passes_test(is_librarian)
def librarian_view(request):
    """
    Librarian-only view: restricted to users with 'Librarian' role.
    
    Only librarians can access this view. Other users will be redirected to login.
    This view displays librarian controls and library management options.
    """
    context = {
        'message': 'Welcome Librarian! You can manage library and books.',
        'role': request.user.profile.role,
    }
    return render(request, 'relationship_app/librarian_view.html', context)


# ============ MEMBER VIEW ============

@user_passes_test(is_member)
def member_view(request):
    """
    Member-only view: restricted to users with 'Member' role.
    
    Only members can access this view. Other users will be redirected to login.
    This view displays member information and member-accessible features.
    """
    context = {
        'message': 'Welcome Member! You have read-only access to library resources.',
        'role': request.user.profile.role,
    }
    return render(request, 'relationship_app/member_view.html', context)


# ============ PERMISSION-BASED BOOK MANAGEMENT ============

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    Add a new book - requires 'can_add_book' permission.
    
    GET: Display the form to add a new book
    POST: Process the form and create a new book
    
    Users without the 'can_add_book' permission will get a 403 Forbidden error.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        isbn = request.POST.get('isbn')
        
        try:
            author = Author.objects.get(id=author_id)
            book = Book.objects.create(title=title, author=author, isbn=isbn)
            return redirect('book-list')
        except Author.DoesNotExist:
            context = {
                'error': 'Author not found',
                'authors': Author.objects.all(),
            }
            return render(request, 'relationship_app/add_book.html', context)
    
    authors = Author.objects.all()
    context = {'authors': authors}
    return render(request, 'relationship_app/add_book.html', context)


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """
    Edit an existing book - requires 'can_change_book' permission.
    
    GET: Display the form with current book data
    POST: Process the form and update the book
    
    Users without the 'can_change_book' permission will get a 403 Forbidden error.
    """
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return redirect('book-list')
    
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        author_id = request.POST.get('author')
        book.isbn = request.POST.get('isbn', book.isbn)
        
        try:
            if author_id:
                book.author = Author.objects.get(id=author_id)
            book.save()
            return redirect('book-list')
        except Author.DoesNotExist:
            context = {
                'book': book,
                'authors': Author.objects.all(),
                'error': 'Author not found',
            }
            return render(request, 'relationship_app/edit_book.html', context)
    
    authors = Author.objects.all()
    context = {'book': book, 'authors': authors}
    return render(request, 'relationship_app/edit_book.html', context)


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """
    Delete a book - requires 'can_delete_book' permission.
    
    GET: Display deletion confirmation page
    POST: Delete the book and redirect to book list
    
    Users without the 'can_delete_book' permission will get a 403 Forbidden error.
    """
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return redirect('book-list')
    
    if request.method == 'POST':
        book.delete()
        return redirect('book-list')
    
    context = {'book': book}
    return render(request, 'relationship_app/delete_book.html', context)

