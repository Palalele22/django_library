from functools import wraps
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import  redirect

from library.models import BookInstance

def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('home')  
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def user_has_rented_book(view_func):
    @wraps(view_func)
    def _wrapped_view(request, book_id, *args, **kwargs):
        book_instance = BookInstance.objects.filter(book_id=book_id, borrower=request.user).exists()

        if book_instance:
            return view_func(request, book_id, *args, **kwargs)
        else:
            messages.error(request, ("You do not have permission to leave a review to a book that you didn't rent."))
            return redirect('home')

    return _wrapped_view