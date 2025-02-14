from django import forms
from .models import Book, Review




from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'cover_image', 'file', 'published_date']


from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone', 'address', 'bio','profile_picture' , ]  # Including new fields
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }



