from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, TemplateView

from library.decorators import staff_required
from .models import Book, BookInstance, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

# @login_required
# def home(request):
#     books = Book.objects.all()
#     return render(request, 'home.html', {'books': books})


class HomeView(TemplateView):
    template_name = 'home.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return context

# @login_required
# def about(request):
#     return render(request, 'about.html', {})

class AboutView(TemplateView):
    template_name = 'about.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
class CategoryView(TemplateView):
    template_name = 'category.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        category_name = kwargs.get('foo').replace('-', ' ')
        try:
            category = Category.objects.get(name=category_name)
            books = Book.objects.filter(category=category)
            return render(request, self.template_name, {'books': books})
        except Category.DoesNotExist:
            messages.error(request, 'That category does not exist')
            return redirect('home')


# @login_required
# def category(request, foo):
#     foo = foo.replace('-', ' ')
#     try:
#         category = Category.objects.get(name=foo)
#         books = Book.objects.filter(category=category)
#         return render(request, 'category.html', {'books': books})
#     except:
#         messages.error(request, 'That category does not exist')
#         return redirect('home')
        
class BookView(DetailView):
    model = Book
    template_name = 'book.html'
    context_object_name = 'book'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

# @login_required
# def book(request, pk):
#     book = Book.objects.get(id=pk)
#     return render(request, 'book.html',{'book':book})

class LoginUserView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_approved:
                login(request, user)
                messages.success(request, ("You have been logged in"))
                return redirect('home')
            else:
                messages.error(request, "Your account is not approved. Please wait for approval.")
                return redirect('login')
        else:
            messages.error(request, ("Invalid username or password"))
            return redirect('login')


class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    
class RegisterUserView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            messages.success(request, ("You have registered successfully! You have to wait for an admin to approve the sign up process!"))
            return redirect('home')
        else:
            error_messages = form.errors.as_text()
            messages.error(request, f"There was an error signing up: {error_messages}")
            return render(request, self.template_name, {'form': form})


# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.is_approved:
#                 login(request, user)
#                 messages.success(request, ("You have been logged in"))
#                 return redirect('home')
#             else:
#                 messages.error(request, "Your account is not approved. Please wait for approval.")
#                 return redirect('login')
#         else:
#             messages.error(request, ("Invalid username or password"))
#             return redirect('login')
#     else:
#         return render(request, 'login.html', {})



    
# def logout_user(request):
#     logout(request)
#     messages.success(request, ("You have been logged out"))
#     return redirect('login')

# def register_user(request):
#     form = SignUpForm()
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             messages.success(request, ("You have registered successfully! You have to wait for an admin to approve the sign up process!"))
#             return redirect('home')
#         else:
#             error_messages = form.errors.as_text()
#             messages.error(request, f"There was an error signing up: {error_messages}")
#             return render(request, 'register.html', {'form': form})
#     else:
#         return render(request, 'register.html', {'form': form})
    
# @login_required
# def my_books(request):
#     rented_books = BookInstance.objects.filter(borrower=request.user, is_returned=False)
#     return render(request, 'my_books.html', {'rented_books': rented_books})


class MyBooksView(TemplateView):
    template_name = 'my_books.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rented_books = BookInstance.objects.filter(borrower=self.request.user, is_returned=False)
        context['rented_books'] = rented_books
        return context


# @staff_required
# def report(request):
#     rented_books = BookInstance.objects.filter(is_returned=False)
#     available_books = Book.objects.filter(quantity__gt=0)
#     return render(request, 'report.html', {'rented_books': rented_books, 'available_books': available_books})

class ReportView(TemplateView):
    template_name = 'report.html'
    
    @method_decorator(staff_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rented_books = BookInstance.objects.filter(is_returned=False)
        available_books = Book.objects.filter(quantity__gt=0)
        context['rented_books'] = rented_books
        context['available_books'] = available_books
        return context