from django import forms
from .models import Book, Review, Profile, Chapter 

# Book Form
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'cover_image', 'file', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author name'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Book description...'}),
            'published_date': forms.DateInput(attrs={'type': 'date'}),
        }

# Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }

# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone', 'address', 'bio', 'profile_picture']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your address'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write about yourself...'}),
        }

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if not profile_picture:
            return "default_profile.png"  # Set default profile image if not uploaded
        return profile_picture


from django import forms
from .models import Chapter

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'content', 'cover_image', 'file']

# Formset to manage multiple chapters dynamically
ChapterFormSet = forms.inlineformset_factory(
    Book, Chapter, form=ChapterForm, extra=1, can_delete=True
)

