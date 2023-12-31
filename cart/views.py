from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from library.models import Book, BookInstance
from cart.cart import Cart
import datetime

class CartSummaryView(View):
    template_name = 'cart_summary.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_books = cart.get_books
        return render(request, self.template_name, {'cart_books': cart_books})

class CartAddView(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            book_id = int(request.POST.get('book_id'))
            book = get_object_or_404(Book, id=book_id)
            cart.add(book=book)
            cart_quantity = cart.__len__()
            response = JsonResponse({"qty": cart_quantity})
            return response

class CartDeleteView(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            book_id = int(request.POST.get('book_id'))
            cart.delete(book_id)
            response = JsonResponse({'book': book_id})
            return response

class RentBookView(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def can_rent_book(self, user):
        return BookInstance.objects.filter(borrower=user, is_returned=False).count() < 5
    
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            book_id = int(request.POST.get('book_id'))
            book = get_object_or_404(Book, id=book_id)
            
            if not self.can_rent_book(request.user):
                response = JsonResponse({'success': False, 'message': 'You have reached the maximum limit of rented books.'})
                messages.error(request, 'You have reached the maximum limit of rented books.')
                return response

            existing_instance = BookInstance.objects.filter(book=book, borrower=request.user, is_returned=False).first()
            if existing_instance:
                response = JsonResponse({'success': False, 'message': 'You have already rented this book and it is not returned.'})
                messages.error(request, ("You have already rented this book and it is not returned."))
                return response

            if book.quantity > 0:
                BookInstance.objects.create(
                    book=book,
                    start_date=datetime.date.today(),
                    end_date=datetime.date.today() + datetime.timedelta(days=14),
                    borrower=request.user
                )
                cart.delete(book_id)
                messages.success(request, f'You rented {book.title}')
                return redirect('cart:cart_summary')
            else:
                response = JsonResponse({'success': False, 'message': 'The book is not available for rent.'})
                messages.error(request, ('The book is not available for rent.'))
                return response

        return redirect('home')

class RentAllBooksView(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def can_rent_book(self, user):
        return BookInstance.objects.filter(borrower=user, is_returned=False).count() < 5

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        user = request.user
        books = cart.get_books()
        print(books)
        for book in books:
            existing_instance = BookInstance.objects.filter(book=book, borrower=user, is_returned=False).first()

            if not self.can_rent_book(request.user):
                response = JsonResponse({'success': False, 'message': 'You have reached the maximum limit of rented books.'})
                messages.error(request, ('You have reached the maximum limit of rented books.'))
                return response
            
            if not existing_instance:
                if book.quantity > 0:
                    BookInstance.objects.create(
                        book=book,
                        start_date=datetime.date.today(),
                        end_date=datetime.date.today() + datetime.timedelta(days=14),
                        borrower=user
                    )
                    cart.delete(book.id)

        response = JsonResponse({'success': True, 'message': 'All books rented successfully.'})
        messages.success(request, ('All books rented successfully.'))
        return response