
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Author, Genre, Book, BookInstance


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


class BookInline(admin.TabularInline):
    model = Book


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'display_genre', 'get_photo']
    inlines = [BooksInstanceInline]

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return 'не установлено'

    get_photo.short_description = 'фото'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'date_of_birth', 'date_of_death', 'get_photo']
    fields = ['last_name', 'first_name', ('date_of_birth', 'date_of_death'), 'photo', 'biography']
    inlines = [BookInline]

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="65">')
        else:
            return 'не установлено'

    get_photo.short_description = 'фото'


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'imprint', 'borrower', 'due_back', 'status']
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)

