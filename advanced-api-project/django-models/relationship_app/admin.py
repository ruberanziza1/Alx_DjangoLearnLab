from django.contrib import admin
from .models import Author, Book, Library, Librarian, Publisher, Genre, BookPublisher, BookGenre

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn']
    list_filter = ['author', 'publication_date']
    search_fields = ['title', 'author__name', 'isbn']

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_book_count']
    filter_horizontal = ['books']

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ['name', 'library', 'employee_id']
    list_filter = ['hire_date']

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']
    search_fields = ['name']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(BookPublisher)
class BookPublisherAdmin(admin.ModelAdmin):
    list_display = ['book', 'publisher', 'publication_date', 'print_run']
    list_filter = ['publication_date']

@admin.register(BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    list_display = ['book', 'genre', 'primary_genre']
    list_filter = ['primary_genre']
