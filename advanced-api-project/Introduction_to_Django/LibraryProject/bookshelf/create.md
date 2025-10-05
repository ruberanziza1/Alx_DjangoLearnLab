from bookshelf.models import Book

# This code creates a book instance and saves it to the django database

Book.objects.create(title="1984", author="George Orwell", published_year=1949)