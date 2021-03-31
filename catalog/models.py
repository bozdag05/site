from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    summary = models.TextField(max_length=10000, help_text='Enter a brief description of the book',
                               verbose_name='Резюме')
    genre = models.ManyToManyField('Genre')
    isbn = models.CharField(max_length=13, unique=True, verbose_name='ISBN')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='фото', blank=True)

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book', kwargs={"book_id": self.pk})  # args=[str(self.id)])

    class Meta:
        verbose_name = 'Книгу'
        verbose_name_plural = 'Книги'
        ordering = ['author']


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Жанр', )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, verbose_name='Книга')
    imprint = models.CharField(max_length=200, verbose_name='отпечаток')
    due_back = models.DateField(null=True, blank=True, verbose_name='Дата возврата')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='заемщик')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Поддержка'),
        ('o', 'В кредит'),
        ('a', 'Доступный'),
        ('r', 'Зарезервированный'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Доступность книги',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Копию'
        verbose_name_plural = 'Копий'
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """Строка для представления объекта модели."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Модель, представляющая автора."""
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    date_of_death = models.DateField(null=True, blank=True, verbose_name='Дата смерти')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='фото', blank=True)
    biography = models.TextField(max_length=10000, verbose_name='Биография', blank=True)

    class Meta:
        verbose_name = 'Автора'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author', kwargs={"author_id": self.pk})

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
