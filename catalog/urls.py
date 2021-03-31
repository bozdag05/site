from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', index, name='index'),
    path('books/', get_books, name='books'),
    #path('books/', AllBooks.as_view(), name='books'),
    path('books/genre/<int:genre_id>/', get_genre, name='category'),
    path('authors/', get_authors, name='authors'),
    path('author/<int:author_id>', get_author, name='author'),
    path('book/<int:book_id>/', get_book, name='book'),
    path('mybooks/', LoanedBooksByUserListView, name='my-borrowed'),
    path('list/', Bookinstance_list_of_all_users, name='users_list'),
    path('book/<pk>/renew/', renew_book_librarian, name='renew-book-librarian'),

]


urlpatterns += [
    path('author/create/', AuthorCreate.as_view(), name='author_create'),
    path('author/<pk>/update/', AuthorUpdate.as_view(), name='author_update'),
    path('author/<pk>/delete/', AuthorDelete.as_view(), name='author_delete'),
]

