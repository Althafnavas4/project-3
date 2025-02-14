from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    file = models.FileField(upload_to='book_files/', null=True, blank=True)
    published_date = models.DateField()

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.CharField(max_length=255)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()  # Make sure this line exists

    def __str__(self):
        return f'Review for {self.book.title} by {self.user}'
    



# models.py

from django.db import models
from django.contrib.auth.models import User
from .models import Book

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"








from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    name = models.CharField(max_length=255, blank=True, null=True)  # User's name
    address = models.TextField(blank=True, null=True)  # User's address
    phone = models.CharField(max_length=15, blank=True, null=True)  # User's phone number
    email = models.EmailField(blank=True, null=True)  # User's email address
    bio = models.TextField(blank=True, null=True)  # Short bio
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Profile picture

    def __str__(self):
        return f"{self.user.username}'s Profile"




# models.py
