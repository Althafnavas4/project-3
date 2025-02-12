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
]










   

