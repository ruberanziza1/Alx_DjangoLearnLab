# relationship_app/query_samples.py
"""
Sample queries demonstrating Django ORM operations with model relationships.
Run this script in Django shell: python manage.py shell
Then: exec(open('relationship_app/query_samples.py').read())
"""

from relationship_app.models import Author, Book, Library, Librarian, Publisher, BookPublisher, Genre, BookGenre
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


def create_sample_data():
    """
    Create sample data for testing relationships
    """
    print("Creating sample data...")
    
    # Create Authors
    author1, created = Author.objects.get_or_create(name="George Orwell")
    author2, created = Author.objects.get_or_create(name="Harper Lee")
    author3, created = Author.objects.get_or_create(name="J.K. Rowling")
    
    # Create Books with ForeignKey relationships to Authors
    book1, created = Book.objects.get_or_create(
        title="1984", 
        author=author1,
        defaults={'isbn': '9780451524935'}
    )
    book2, created = Book.objects.get_or_create(
        title="Animal Farm", 
        author=author1,
        defaults={'isbn': '9780451526342'}
    )
    book3, created = Book.objects.get_or_create(
        title="To Kill a Mockingbird", 
        author=author2,
        defaults={'isbn': '9780061120084'}
    )
    book4, created = Book.objects.get_or_create(
        title="Harry Potter and the Philosopher's Stone", 
        author=author3,
        defaults={'isbn': '9780747532699'}
    )
    
    # Create Libraries
    library1, created = Library.objects.get_or_create(
        name="Central Public Library",
        defaults={'address': '123 Main Street, Downtown'}
    )
    library2, created = Library.objects.get_or_create(
        name="University Library",
        defaults={'address': '456 Campus Drive, University District'}
    )
    
    # Add books to libraries (ManyToMany relationship)
    library1.books.add(book1, book2, book3)
    library2.books.add(book1, book3, book4)
    
    # Create Librarians with OneToOne relationships to Libraries
    librarian1, created = Librarian.objects.get_or_create(
        library=library1,
        defaults={
            'name': "Alice Johnson",
            'employee_id': 'LIB001',
            'phone_number': '555-0123'
        }
    )
    librarian2, created = Librarian.objects.get_or_create(
        library=library2,
        defaults={
            'name': "Bob Smith",
            'employee_id': 'LIB002',
            'phone_number': '555-0456'
        }
    )
    
    print("Sample data created successfully!")


def query_all_books_by_author():
    """
    Query all books by a specific author using ForeignKey relationship.
    Demonstrates forward relationship traversal.
    """
    print("\n=== QUERY 1: All books by a specific author ===")
    
    try:
        # Method 1: Using filter on Book model
        author_name = "George Orwell"
        author = Author.objects.get(name=author_name)
        books_by_author = Book.objects.filter(author=author)
        
        print(f"Books by {author_name} (Method 1 - Forward lookup):")
        for book in books_by_author:
            print(f"  - {book.title}")
        
        # Method 2: Using reverse relationship (related_name)
        books_by_author_reverse = author.books.all()
        
        print(f"\nBooks by {author_name} (Method 2 - Reverse lookup):")
        for book in books_by_author_reverse:
            print(f"  - {book.title}")
        
        # Method 3: Using double underscore lookup
        books_direct = Book.objects.filter(author__name=author_name)
        print(f"\nBooks by {author_name} (Method 3 - Double underscore):")
        for book in books_direct:
            print(f"  - {book.title}")
        
        # Additional: Get book count for author
        book_count = author.books.count()
        print(f"\nTotal books by {author_name}: {book_count}")
        
    except ObjectDoesNotExist:
        print(f"Author '{author_name}' not found.")
    except Exception as e:
        print(f"Error querying books by author: {e}")


def query_all_books_in_library():
    """
    List all books in a library using ManyToMany relationship.
    Demonstrates ManyToMany field traversal.
    """
    print("\n=== QUERY 2: All books in a library ===")
    
    try:
        library_name = "Central Public Library"
        library = Library.objects.get(name=library_name)
        
        # Method 1: Direct access to ManyToMany field
        books_in_library = library.books.all()
        
        print(f"Books in {library_name}:")
        for book in books_in_library:
            print(f"  - {book.title} by {book.author.name}")
        
        # Method 2: Using reverse lookup
        books_reverse = Book.objects.filter(libraries=library)
        print(f"\nBooks in {library_name} (Reverse lookup):")
        for book in books_reverse:
            print(f"  - {book.title}")
        
        # Method 3: Using double underscore lookup
        books_by_library_name = Book.objects.filter(libraries__name=library_name)
        print(f"\nBooks in {library_name} (Double underscore):")
        for book in books_by_library_name:
            print(f"  - {book.title}")
        
        # Additional: Get book count and other library stats
        book_count = library.books.count()
        print(f"\nTotal books in {library_name}: {book_count}")
        
        # Get unique authors in this library
        authors_in_library = Author.objects.filter(books__libraries=library).distinct()
        print(f"Authors with books in this library:")
        for author in authors_in_library:
            print(f"  - {author.name}")
            
    except ObjectDoesNotExist:
        print(f"Library '{library_name}' not found.")
    except Exception as e:
        print(f"Error querying books in library: {e}")


def query_librarian_for_library():
    """
    Retrieve the librarian for a library using OneToOne relationship.
    Demonstrates OneToOne field traversal in both directions.
    """
    print("\n=== QUERY 3: Librarian for a library ===")
    
    try:
        library_name = "Central Public Library"
        library = Library.objects.get(name=library_name)
        
        # Method 1: Using related_name (reverse OneToOne)
        librarian = library.librarian
        print(f"Librarian for {library_name}: {librarian.name}")
        print(f"Employee ID: {librarian.employee_id}")
        print(f"Phone: {librarian.phone_number}")
        
        # Method 2: Using forward lookup from Librarian model
        librarian_forward = Librarian.objects.get(library=library)
        print(f"\nLibrarian (Forward lookup): {librarian_forward.name}")
        
        # Method 3: Using double underscore lookup
        librarian_by_library_name = Librarian.objects.get(library__name=library_name)
        print(f"Librarian (Double underscore): {librarian_by_library_name.name}")
        
        # Additional: Get library details from librarian
        print(f"\nLibrary managed by {librarian.name}:")
        print(f"  - Name: {librarian.library.name}")
        print(f"  - Address: {librarian.library.address}")
        print(f"  - Total books: {librarian.library.books.count()}")
        
    except ObjectDoesNotExist:
        print(f"Library '{library_name}' or its librarian not found.")
    except Exception as e:
        print(f"Error querying librarian for library: {e}")


def advanced_relationship_queries():
    """
    Additional complex queries demonstrating advanced ORM usage
    """
    print("\n=== ADVANCED RELATIONSHIP QUERIES ===")
    
    # Query 1: Libraries with more than a specific number of books
    print("Libraries with more than 2 books:")
    libraries_with_many_books = Library.objects.annotate(
        book_count=models.Count('books')
    ).filter(book_count__gt=2)
    
    for library in libraries_with_many_books:
        print(f"  - {library.name}: {library.book_count} books")
    
    # Query 2: Authors with books in multiple libraries
    print("\nAuthors with books in multiple libraries:")
    authors_multi_libraries = Author.objects.annotate(
        library_count=models.Count('books__libraries', distinct=True)
    ).filter(library_count__gt=1)
    
    for author in authors_multi_libraries:
        print(f"  - {author.name}: books in {author.library_count} libraries")
    
    # Query 3: Books available in all queried libraries
    print("\nBooks available in multiple libraries:")
    books_multi_libraries = Book.objects.annotate(
        library_count=models.Count('libraries')
    ).filter(library_count__gt=1)
    
    for book in books_multi_libraries:
        libraries = [lib.name for lib in book.libraries.all()]
        print(f"  - {book.title}: in {', '.join(libraries)}")
    
    # Query 4: Librarians and their library's book statistics
    print("\nLibrarian statistics:")
    librarians = Librarian.objects.select_related('library').prefetch_related('library__books__author')
    
    for librarian in librarians:
        library = librarian.library
        book_count = library.books.count()
        authors = Author.objects.filter(books__libraries=library).distinct().count()
        
        print(f"  - {librarian.name}:")
        print(f"    Library: {library.name}")
        print(f"    Books: {book_count}")
        print(f"    Unique Authors: {authors}")


def demonstrate_relationship_operations():
    """
    Demonstrate various operations on relationships
    """
    print("\n=== RELATIONSHIP OPERATIONS DEMO ===")
    
    # Adding and removing relationships
    try:
        library = Library.objects.get(name="Central Public Library")
        new_author = Author.objects.create(name="Jane Austen")
        new_book = Book.objects.create(title="Pride and Prejudice", author=new_author, isbn="9780141439518")
        
        # Add book to library
        library.books.add(new_book)
        print(f"Added '{new_book.title}' to {library.name}")
        
        # Remove book from library
        library.books.remove(new_book)
        print(f"Removed '{new_book.title}' from {library.name}")
        
        # Clean up
        new_book.delete()
        new_author.delete()
        
    except Exception as e:
        print(f"Error in relationship operations: {e}")


def run_all_queries():
    """
    Execute all query functions
    """
    print("Django ORM Relationship Queries Demo")
    print("=" * 50)
    
    # Ensure we have sample data
    create_sample_data()
    
    # Run all queries
    query_all_books_by_author()
    query_all_books_in_library()
    query_librarian_for_library()
    advanced_relationship_queries()
    demonstrate_relationship_operations()
    
    print("\n" + "=" * 50)
    print("Query demonstration completed!")


# Import models for annotations in advanced queries
from django.db import models

if __name__ == "__main__":
    # This allows the script to be run directly in Django shell
    run_all_queries()
