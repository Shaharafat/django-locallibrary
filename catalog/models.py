import uuid

from django.db import models
from django.urls import reverse


class Author(models.Model):
    """Model representation an author"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Language(models.Model):
    """Model representation of language"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Genre(models.Model):

    """Model representing a book genre"""

    name = models.CharField(max_length=200, help_text="Enter a book genre")

    def __str__(self):
        """String for representing the Model object."""
        return str(self.name)


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)"""

    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book"
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        unique=True,
        help_text="13 character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>",
    )

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField("Genre", help_text="Select a genre for this book")
    language = models.ForeignKey("Language", on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        """Create a string fot the genre, This is required to display genre in admin"""
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific copy of a book"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular book across whole library",
    )
    book = models.ForeignKey("Book", on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        default="m",
        blank=True,
        help_text="Book availablity",
    )

    def display_book(self):
        return self.book.title

    display_book.short_description = "Book"

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return f"{self.id} ({self.book.title})"
