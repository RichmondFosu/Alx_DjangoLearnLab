from django.core.management.base import BaseCommand
from relationship_app.models import Author, Book, Library, Librarian

class Command(BaseCommand):
    help = 'Create 5 sample objects for each model'

    def handle(self, *args, **options):
        # Create 5 Authors
        authors = [
            Author.objects.create(name='Jane Austen'),
            Author.objects.create(name='Charles Dickens'),
            Author.objects.create(name='Mark Twain'),
            Author.objects.create(name='George Orwell'),
            Author.objects.create(name='Harper Lee'),
        ]
        self.stdout.write(self.style.SUCCESS('Created 5 Authors'))

        # Create 5 Books
        books = [
            Book.objects.create(title='Pride and Prejudice', author=authors[0]),
            Book.objects.create(title='Great Expectations', author=authors[1]),
            Book.objects.create(title='Adventures of Huckleberry Finn', author=authors[2]),
            Book.objects.create(title='1984', author=authors[3]),
            Book.objects.create(title='To Kill a Mockingbird', author=authors[4]),
        ]
        self.stdout.write(self.style.SUCCESS('Created 5 Books'))

        # Create 5 Libraries
        libraries = [
            Library.objects.create(name='Central Library'),
            Library.objects.create(name='City Public Library'),
            Library.objects.create(name='Downtown Library'),
            Library.objects.create(name='Westside Library'),
            Library.objects.create(name='University Library'),
        ]
        self.stdout.write(self.style.SUCCESS('Created 5 Libraries'))

        # Add books to libraries (many-to-many)
        libraries[0].books.add(books[0], books[1])
        libraries[1].books.add(books[2], books[3])
        libraries[2].books.add(books[4], books[0])
        libraries[3].books.add(books[1], books[2])
        libraries[4].books.add(books[3], books[4])
        self.stdout.write(self.style.SUCCESS('Added books to libraries'))

        # Create 5 Librarians
        librarians = [
            Librarian.objects.create(name='Alice Johnson', library=libraries[0]),
            Librarian.objects.create(name='Bob Smith', library=libraries[1]),
            Librarian.objects.create(name='Carol White', library=libraries[2]),
            Librarian.objects.create(name='David Brown', library=libraries[3]),
            Librarian.objects.create(name='Eve Davis', library=libraries[4]),
        ]
        self.stdout.write(self.style.SUCCESS('Created 5 Librarians'))

        self.stdout.write(self.style.SUCCESS('All objects created successfully!'))
