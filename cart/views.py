import datetime
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from library.models import Book, BookInstance

from .cart import Cart

def cart_summary(request):
    cart = Cart(request)
    cart_books = cart.get_books
    return render(request, 'cart_summary.html', {'cart_books': cart_books})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        book_id = int(request.POST.get('book_id'))
        
        book = get_object_or_404(Book, id=book_id)
        
        cart.add(book=book)
        
        cart_quantity = cart.__len__()
        
        response = JsonResponse({"qty": cart_quantity})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        book_id = int(request.POST.get('book_id'))
        cart.delete(book_id)
        
        response = JsonResponse({'book': book_id})
        return response
    
def rent_book(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        book_id = int(request.POST.get('book_id'))
        book = get_object_or_404(Book, id=book_id)
        
        existing_instance = BookInstance.objects.filter(book=book, borrower=request.user, is_returned=False).first()
        if existing_instance:
            response = JsonResponse({'success': False, 'message': 'You have already rented this book and it is not returned.'})
            messages.error(request, ("You have already rented this book and it is not returned."))
            return response
        
        if book.quantity > 0:
            BookInstance.objects.create(book=book, start_date=datetime.date.today(), end_date=datetime.date.today() + datetime.timedelta(days=14), borrower=request.user)
            cart.delete(book_id)
            messages.success(request, 'You rented {book.title}')
            return redirect('cart_summary')
        else:
            response = JsonResponse({'success': False, 'message': 'The book is not available for rent.'})
            messages.error(request, ('The book is not available for rent.'))
            return response
        
    return redirect('home')




