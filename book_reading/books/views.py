from django.shortcuts import render
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib import messages
from .forms import BookForm, ReviewForm



# Create your views here.



def book_login(req):
    if 'eazy' in req.session:
        return redirect(manage_books)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['passwd']
        data=authenticate(username=uname,password=password)
        
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['eazy']=uname   #create session
                return redirect(manage_books)
            else:
                
                login(req,data)
                req.session['user']=uname   #create session
                return redirect(book_list)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(book_login)
    else:
        return render(req,'login.html')
    



from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def register(req):
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        confirm_password = req.POST['confirm_password']

        # Check if the password is at least 8 characters long
        if len(password) < 8:
            messages.warning(req, 'Password must be at least 8 characters long.')
            return redirect(register)

        # Check if the passwords match
        if password != confirm_password:
            messages.warning(req, 'Passwords do not match.')
            return redirect(register)

        try:
            # Create the user if all conditions are met
            data = User.objects.create_user(first_name=name, email=email, password=password, username=email)
            data.save()

            # Success message
            messages.success(req, 'Account created successfully. You can now log in.')
            return redirect(book_login)
        except:
            messages.warning(req, 'User already exists.')
            return redirect(register)
    else:
        return render(req, 'user/register.html')
    


def book_logout(req):
    req.session.flush()          #delete session
    logout(req)
    return redirect(book_login)


# Book List View with Pagination
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Book, Review
from .forms import BookForm, ReviewForm
from django.core.paginator import Paginator, EmptyPage, Page


# Book List View with Pagination
def book_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        books = Book.objects.filter(title__icontains=search_query) | Book.objects.filter(author__icontains=search_query)
    else:
        books = Book.objects.all()

    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user/book_list.html', {'page_obj': page_obj, 'search_query': search_query})

# Add Book (Admin)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully.')
            return redirect('manage_books')
        else:
            messages.error(request, 'Failed to add book. Please try again.')
    else:
        form = BookForm()
    return render(request, 'admin/book_add_form.html', {'form': form})

# Manage Books (Admin)
def manage_books(request):
    books = Book.objects.all()
    return render(request, 'admin/manage_books.html', {'books': books})

# Edit Book (Admin)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('manage_books')
        else:
            messages.error(request, 'Failed to update book. Please try again.')
    else:
        form = BookForm(instance=book)
    return render(request, 'admin/book_change_form.html', {'form': form, 'book': book})

# Add Review (for users)
def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            messages.success(request, 'Review added successfully.')
            return redirect('book_list')
    else:
        form = ReviewForm()
    return render(request, 'admin/add_review.html', {'form': form, 'book': book})
