# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('add_property/', views.add_property, name='add_property'),
    path('seller/logout/', views.seller_logout, name='seller_logout'),
    path('buyer/listing/', views.listing_view, name='listing_view'),
    path('buyer/logout/', views.buyer_logout, name='buyer_logout'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('property/<int:property_id>/', views.property_details, name='property_details'),
    path('add_comment/<int:listing_id>/', views.add_comment, name='add_comment'),
    path('delete_listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path('book/<int:listing_id>/', views.book_property, name='book_property'),
    # Add other URLs as needed
]
