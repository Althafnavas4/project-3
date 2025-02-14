from django.urls import path
from . import views

urlpatterns = [

    path('', views.book_login, name='book_login'),
    path('book_logout',views.book_logout, name='book_logout'),
    path('register/', views.register, name='register'),
    
    # User and Admin URLs
    path('book_lis/', views.book_list, name='book_list'),
    path('add_book/', views.add_book, name='add_book'),
    path('manage_books/', views.manage_books, name='manage_books'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('add_review/<int:pk>/', views.add_review, name='add_review'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/view/', views.pdf_viewer, name='pdf_viewer'),
    path('book/<int:book_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_books, name='favorite_books'),
    path('book/<int:book_id>/remove-favorite/', views.remove_favorite, name='remove_favorite'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('book/download/<int:book_id>/', views.download_book, name='download_book'),
    path('book/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('book/<int:book_id>/manage-chapters/', views.add_chapters_to_book, name='manage_chapters'),
    path("chapter/<int:pk>/", views.chapter_detail, name="chapter_detail"),
   
   


        # New URL for removing a favorite
]










   

