# retrieve all attributes of the book
Book.objects.all()

# output
<QuerySet [<Book: 1984 by George Orwell>]>

# do display all attributes
for book in Book.objects.all():
    print(book.title, book.author, book.published_year)
