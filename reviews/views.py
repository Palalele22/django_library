from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from reviews.decorators import user_has_rented_book
from reviews.models import Review
from reviews.forms import ReviewForm
from library.models import Book, BookInstance 

class ReviewListView(View):
    template_name = 'review_list.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        reviews = Review.objects.filter(user=request.user).order_by('-id')
        return render(request, self.template_name, {'reviews': reviews})

class AddReviewView(View):
    template_name = 'add_review.html'
    
    @method_decorator(login_required)
    @method_decorator(user_has_rented_book)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        form = ReviewForm()
        return render(request, self.template_name, {'form': form, 'book': book})

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        book_instance = BookInstance.objects.filter(book=book, borrower=request.user)
        
        if not book_instance:
            messages.error(request, ("You have to rent the book to leave a review."))
            return redirect('home') 
        
        existing_review = Review.objects.filter(book=book, user=request.user).exists()
        
        if not existing_review:
            form = ReviewForm(request.POST)

            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                return redirect('home')
        else:
            return redirect('home')

class EditReviewView(View):
    template_name = 'edit_review.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, user=request.user)
        form = ReviewForm(instance=review)
        return render(request, self.template_name, {'form': form, 'review': review})

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, user=request.user)
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            return redirect('reviews:review_list')

        return render(request, self.template_name, {'form': form, 'review': review})


class DeleteReviewView(View):
    template_name = 'delete_review.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, user=request.user)
        return render(request, self.template_name, {'review': review})

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review.delete()
        return redirect('reviews:review_list')
