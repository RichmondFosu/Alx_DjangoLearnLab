# retrieve all attributes of the book
book.objects.get()

# output
<QuerySet [<Book: 1984 by George Orwell>]>

# do display all attributes

    print(book.title, book.author, book.published_year)
