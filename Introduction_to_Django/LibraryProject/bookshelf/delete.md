from bookshelf.models import Book

# Delete book
book.delete()

# confirm deletion
Book.objects.all()
# <QuerySet []>