from bookshelf.models import Book

# Displays a book by title
book = Book.objects.get(title="1984")
print(book)

# Display all attributes
print(book.id, book.title, book.author, book.published_year)