from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from django.contrib.auth.decorators import permission_required

# Create your views here.

@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create_book', raise_exception=True)
def create_book(request):
    # view to create a new book
    # requires 'can_create_book' permission

    if request.method == 'POST':
            title = request.POST.get('title')
            author = request.POST.get('author')
            published_year = request.POST.get('published_year')
            Book.objects.create(title=title, author=author, published_year=published_year)
            return redirect('book_list')
    
    return render(request, 'bookshelf/create_book.html')

@permission_required('bookshelf.can_edit_book', raise_exception=True)
def edit_book(request, book_id):

        # view to edit an existing book
        # requires 'can_edit_book' permission

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
            book.title = request.POST.get('title')
            book.author = request.POST.get('author')
            book.published_year = request.POST.get('published_year')
            book.save()
            return redirect('book_list')
    
    return render(request, 'bookshelf/edit_book.html', {'book': book})

@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, book_id):

        # view to delete a book
        # requires 'can_delete_book' permission

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
            book.delete()
            return redirect('book_list')
    
    # return render(request, 'bookshelf/delete_book.html', {'book': book})