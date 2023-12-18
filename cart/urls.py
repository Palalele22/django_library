from django.urls import path
from .views import CartSummaryView, CartAddView, CartDeleteView, RentBookView

urlpatterns = [
    path('', CartSummaryView.as_view(), name='cart_summary'),
    path('add/', CartAddView.as_view(), name='cart_add'),
    path('delete/', CartDeleteView.as_view(), name='cart_delete'),
    path('rent-book/', RentBookView.as_view(), name='rent_book'),
]
