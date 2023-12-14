from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('book/<int:pk>', views.book, name='book'),
    path('category/<str:foo>', views.category, name='category'),
    path('my-books/', views.my_books, name='my_books'),
]