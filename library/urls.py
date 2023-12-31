from django.urls import path

from library.views import AboutView, BookView, CategoryView, HomeView, LoginUserView, LogoutUserView, MyBooksView, RegisterUserView, ReportView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('book/<int:pk>', BookView.as_view(), name='book'),
    path('category/<str:foo>', CategoryView.as_view(), name='category'),
    path('my-books/', MyBooksView.as_view(), name='my_books'),
    path('report/', ReportView.as_view(), name='report'),
]