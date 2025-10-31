# create a Book instance
Book.objects.create(title = '1984', author = 'George Orwell', published_year = 1949)


# confirm
Book.objects.all()
# <QuerySet [<Book: 1984 by George Orwell>]>


