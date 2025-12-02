from django.db import models

# Create your models here.
class Author(models.Model):
    '''
    this model represents the writer of a book.
    one author can have many books.
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    '''
    the Book model represents a single book.
    each book belongs to exactly one author, 
    forming a one-to-many relationship: one Author -> Many Books.

    '''
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()

    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
