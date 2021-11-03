from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home' ),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('productDetails/<int:id>/', views.productDetails, name='productDetails'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('search/', views.search, name='search'),
]