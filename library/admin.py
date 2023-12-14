from django.contrib import admin

from .models import Book, BookInstance, Category, CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_approved', 'is_staff')
    search_fields = ('username', 'email', 'is_approved', 'is_staff')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'quantity')
    search_fields = ('title', 'author', 'category', 'quantity')
    
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'is_returned', 'start_date', 'end_date')
    search_fields = ('book', 'borrower', 'is_returned', 'start_date', 'end_date')
    
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)

