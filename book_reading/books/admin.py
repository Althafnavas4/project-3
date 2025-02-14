from django.contrib import admin
from .models import Book, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'view_cover_image')
    inlines = [ReviewInline]

    def view_cover_image(self, obj):
        if obj.cover_image:
            return f'<img src="{obj.cover_image.url}" width="100"/>'
        return "No Image"
    view_cover_image.allow_tags = True

admin.site.register(Book, BookAdmin)
admin.site.register(Review)




# admin.py


