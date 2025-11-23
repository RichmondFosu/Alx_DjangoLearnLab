# create a Book instance
book = Book.objects.create(title = '1984', author = 'George Orwell', published_year = 1949)


# confirm
book.objects.all()
# <QuerySet [<Book: 1984 by George Orwell>]>


