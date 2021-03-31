from django.shortcuts import render, redirect
from .models import Book, Author, BookInstance, Genre
from django.views.generic import ListView
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('books')
        else:
            messages.error(request, 'Ощибка регистраций :(')

    else:

        form = UserRegisterForm()

    return render(request, 'catalog/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('books')

    else:
        form = UserLoginForm()

    return render(request, 'catalog/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


class AllBooks(ListView):
    model = Book


def index(request):
    num_books = Book.objects.all()
    num_instances = BookInstance.objects.all()
    num_instances_available = BookInstance.objects.filter(status__exact='a')
    num_authors = Author.objects

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'catalog/index.html', context={'num_books': num_books,
                                                  'num_instances': num_instances,
                                                  'num_instances_available': num_instances_available,
                                                  'num_authors': num_authors,
                                                  'num_visits': num_visits})


def get_books(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    context = {
        'books': books,
        'genres': genres,
    }
    return render(request, 'catalog/books.html', context=context)


def get_genre(request, genre_id):
    books = Book.objects.filter(genre_id=genre_id)
    genres = Genre.objects.all()
    genre = Genre.objects.get(pk=genre_id)
    context = {
        'books': books,
        'genre': genre,
        'genres': genres,
    }
    return render(request, 'catalog/genres.html', context=context)


def get_authors(request):
    authors = Author.objects.all()
    return render(request, 'catalog/authors.html', {'authors': authors})


def get_author(request, author_id):
    author = Author.objects.get(pk=author_id)
    return render(request, 'catalog/author-detail.html', {'author': author})


def get_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    genres = Genre.objects.all()
    return render(request, 'catalog/book.html', {'item': book, 'genres': genres})


def LoanedBooksByUserListView(request):
    bookinstance = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('due_back')
    paginate_by = 10
    return render(request, 'catalog/bookinstance_list_borrowed_user.html', {'bookinstance_list': bookinstance})


def Bookinstance_list_of_all_users(request):
    bookinstances = BookInstance.objects.all()
    bookinstance = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('due_back')
    return render(request, 'catalog/list_of_bookinstances.html', {'list': bookinstances, 'users': bookinstance})


from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '12.10.2016', }


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
