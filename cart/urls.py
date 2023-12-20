from django.urls import path
from cart.views import CartSummaryView, CartAddView, CartDeleteView, RentAllBooksView, RentBookView
app_name = "cart"
urlpatterns = [
    path('', CartSummaryView.as_view(), name='cart_summary'),
    path('add/', CartAddView.as_view(), name='cart_add'),
    path('delete/', CartDeleteView.as_view(), name='cart_delete'),
    path('rent-book/', RentBookView.as_view(), name='rent_book'),
    path('rent-all-books/', RentAllBooksView.as_view(), name='rent_all_books'),
]
