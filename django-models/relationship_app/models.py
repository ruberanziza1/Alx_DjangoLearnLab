# relationship_app/models.py
from django.db import models

class Author(models.Model):
    """
    Author model representing book authors.
    Uses CharField for the author's name.
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    """
    Book model with ForeignKey relationship to Author.
    Demonstrates One-to-Many relationship (One author can have many books).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        help_text="Select the author of this book"
    )
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class Library(models.Model):
    """
    Library model with ManyToManyField relationship to Book.
    Demonstrates Many-to-Many relationship (A library can have many books, 
    and a book can be in many libraries).
    """
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(
        Book, 
        related_name='libraries',
        blank=True,
        help_text="Select books available in this library"
    )
    address = models.TextField(blank=True, help_text="Library address")
    established_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_book_count(self):
        """Returns the total number of books in the library"""
        return self.books.count()
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Library'
        verbose_name_plural = 'Libraries'


class Librarian(models.Model):
    """
    Librarian model with OneToOneField relationship to Library.
    Demonstrates One-to-One relationship (Each library has exactly one librarian,
    and each librarian manages exactly one library).
    """
    name = models.CharField(max_length=100)
    library = models.OneToOneField(
        Library, 
        on_delete=models.CASCADE, 
        related_name='librarian',
        help_text="Select the library this librarian manages"
    )
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.name} - Librarian at {self.library.name}"
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Librarian'
        verbose_name_plural = 'Librarians'


# Additional models to demonstrate more complex relationships

class Publisher(models.Model):
    """
    Publisher model to demonstrate additional ForeignKey relationships
    """
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class BookPublisher(models.Model):
    """
    Through model for Book-Publisher relationship with additional fields
    Demonstrates Many-to-Many relationship with extra fields
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()
    print_run = models.IntegerField(default=1000)
    
    class Meta:
        unique_together = ['book', 'publisher']
        verbose_name = 'Book Publication'
        verbose_name_plural = 'Book Publications'
    
    def __str__(self):
        return f"{self.book.title} published by {self.publisher.name}"


class Genre(models.Model):
    """
    Genre model for categorizing books
    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


# Update Book model to include Genre relationship
# Note: In a real implementation, you would add this field to the Book model above
# This is shown separately for clarity

class BookGenre(models.Model):
    """
    Through model for Book-Genre many-to-many relationship
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genre_books')
    primary_genre = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['book', 'genre']
    
    def __str__(self):
        return f"{self.book.title} - {self.genre.name}"
