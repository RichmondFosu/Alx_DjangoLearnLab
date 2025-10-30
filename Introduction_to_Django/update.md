# update title
b1.title = 'Nineteen Eighty-Four'
b1.save()

# confirm update
Book.objects.all()

# output
<QuerySet [<Book: Nineteen Eighty-Four by George Orwell>]>