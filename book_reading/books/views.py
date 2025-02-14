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
    return render(request, 'user/add_review.html', {'form': form, 'book': book})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Book, Review
from .forms import ReviewForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = request.user.profile
        except Profile.DoesNotExist:
            user_profile = None

    reviews = Review.objects.filter(book=book)

    # Create a range for the rating
    star_range = [1, 2, 3, 4, 5]

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = ReviewForm()

    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
        'user_profile': user_profile,
        'star_range': star_range,  # Add this to context
    }

    return render(request, 'user/book_detail.html', context)


# Optionally, you may want to allow authenticated users to delete their reviews:
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    # Ensure the user is deleting their own review
    if review.user != request.user:
        return HttpResponse("You are not authorized to delete this review.", status=403)

    review.delete()
    return redirect('book_detail', book_id=review.book.id)


def pdf_viewer(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'user/pdf_viewer.html', {'book': book})





# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Favorite
from django.contrib import messages

def toggle_favorite(request, book_id):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to be logged in to add a book to your favorites.")
        return redirect('book_list')

    book = get_object_or_404(Book, id=book_id)

    # Check if the book is already in the user's favorites
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)

    if not created:
        # If the book is already in favorites, delete it (removes it from favorites)
        favorite.delete()
        messages.success(request, f"{book.title} has been removed from your favorites.")
    else:
        messages.success(request, f"{book.title} has been added to your favorites.")
    
    return redirect(favorite_books)



# views.py

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Favorite
from django.contrib import messages

def remove_favorite(request, book_id):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to be logged in to remove a book from your favorites.")
        return redirect('book_list')

    book = get_object_or_404(Book, id=book_id)

    # Check if the book is already in the user's favorites
    try:
        favorite = Favorite.objects.get(user=request.user, book=book)
        favorite.delete()
        messages.success(request, f"{book.title} has been removed from your favorites.")
    except Favorite.DoesNotExist:
        messages.warning(request, "This book is not in your favorites.")
    
    return redirect('favorite_books')  # Redirect to the page that shows user's favorites





# views.py

def favorite_books(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to be logged in to view your favorite books.")
        return redirect('book_list')

    favorites = Favorite.objects.filter(user=request.user)
    favorite_books = [favorite.book for favorite in favorites]

    return render(request, 'user/favorite_books.html', {'favorite_books': favorite_books})






from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

# Display User Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Favorite  # Import your models

@login_required
def user_profile(request):
    user = request.user

    # Check if the profile exists, if not, create it
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    # Fetch favorite books for the user
    favorite_books = Favorite.objects.filter(user=user)
    favorite_books_list = [favorite.book for favorite in favorite_books]  # Assuming 'book' is a field in the Favorite model

    # Pass data to the template
    return render(request, 'user/profile.html', {
        'user': user,
        'profile': profile,
        'favorite_books': favorite_books_list,  # Pass the list of favorite books
    })


# Edit User Profile and Upload Profile Picture
@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_profile')  # Redirect to profile view
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'user/edit_profile.html', {'form': form, 'user': user})

# Upload Profile Picture (Separate Form)
@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES['profile_picture']:
        profile = Profile.objects.get(user=request.user)
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        messages.success(request, "Profile picture updated successfully.")
        return redirect('user_profile')  # Redirect to profile page
    return render(request, 'user/upload_profile_picture.html')


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.contrib import messages  # Importing messages for feedback
from .models import Book

def download_book(request, book_id):
    # Get the book by its ID
    book = get_object_or_404(Book, id=book_id)

    # Check if the book has an associated file
    if not book.file:
        messages.error(request, "This book does not have a downloadable file.")
        return render(request, 'book_details.html', {'book': book})  # Redirecting back to the book details page
    
    # Attempt to open and serve the file in binary mode
    try:
        with open(book.file.path, 'rb') as f:
            # Set the appropriate content type
            response = HttpResponse(f.read(), content_type='application/pdf')  # Assuming the file is a PDF
            response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
            
            # Add success message
            messages.success(request, f"Your download of {book.title} has started!")
            return response
    except FileNotFoundError:
        messages.error(request, "The requested book file was not found.")
        return render(request, 'book_details.html', {'book': book})  # Redirect back to the book details page












