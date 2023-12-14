from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Book, BookInstance, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

@login_required
def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})

@login_required
def about(request):
    return render(request, 'about.html', {})

@login_required
def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        books = Book.objects.filter(category=category)
        return render(request, 'category.html', {'books': books})
    except:
        messages.error(request, 'That category does not exist')
        return redirect('home')
        
@login_required
def book(request, pk):
    book = Book.objects.get(id=pk)
    return render(request, 'book.html',{'book':book})

def login_user(request):
    if request.method == 'POST':
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
    else:
        return render(request, 'login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('login')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
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
            return render(request, 'register.html', {'form': form})
    else:
        return render(request, 'register.html', {'form': form})
    
def my_books(request):
    rented_books = BookInstance.objects.filter(borrower=request.user, is_returned=False)
    return render(request, 'my_books.html', {'rented_books': rented_books})