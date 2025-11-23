# Create a Book instance
b1 = Book(title='1984', author='George Orwell', published_year='1949')

# Save the instance
b1.save()

# Confirm creation
Book.objects.all()
# <QuerySet [<Book: 1984 by George Orwell>]>
