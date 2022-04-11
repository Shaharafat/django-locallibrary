from django.shortcuts import render
from django.views import generic

from .models import Author, Book, BookInstance, Genre


# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()
    num_instance_available = BookInstance.objects.filter(status__exact="a").count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.all().count()
    num_book_with_word = Book.objects.filter(title__icontains="habit").count()

    context = {
        "num_books": num_books,
        "num_instance": num_instance,
        "num_instance_available": num_instance_available,
        "num_authors": num_authors,
        "num_genres": num_genres,
        "num_book_with_word": num_book_with_word,
    }

    return render(request, "catalog/index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    queryset = Book.objects.all()[:5]
    template_name = "book_list.html"
    paginate_by = 5


class BookDetailView(generic.DetailView):
    model = Book
