from django.db import models
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    file = models.FileField(upload_to='book_files/', null=True, blank=True)
    published_date = models.DateField()
    
      # If you need to apply custom validations, for example:
    def clean_cover_image(self):
        cover_image = self.cleaned_data.get('cover_image')
        if cover_image and not cover_image.name:
            raise forms.ValidationError("Please upload a cover image.")
        return cover_image

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and not file.name:
            raise forms.ValidationError("Please upload a file.")
        return file

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User
from .models import Book

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Ratings from 1 to 5
    comment = models.TextField()
    reated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review for {self.book.title} by {self.user.username}"



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


class Chapter(models.Model):
    book = models.ForeignKey(Book, related_name="chapters", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='chapter_covers/', blank=True, null=True)
    file = models.FileField(upload_to='chapter_files/', blank=True, null=True)
    number = models.PositiveIntegerField(default=1)  # Auto-number field

    class Meta:
        ordering = ['number']  # Always show chapters in order

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set number when creating a new chapter
            last_chapter = Chapter.objects.filter(book=self.book).order_by('-number').first()
            self.number = last_chapter.number + 1 if last_chapter else 1
        super().save(*args, **kwargs)

# models.py

