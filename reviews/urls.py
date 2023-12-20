from django.urls import path
from reviews.views import ReviewListView, AddReviewView, EditReviewView, DeleteReviewView

app_name = 'reviews'
urlpatterns = [
    path('list/', ReviewListView.as_view(), name='review_list'),
    path('<int:book_id>/add/', AddReviewView.as_view(), name='add_review'),
    path('edit/<int:review_id>/', EditReviewView.as_view(), name='edit_review'),
    path('delete/<int:review_id>/', DeleteReviewView.as_view(), name='delete_review'),
]
