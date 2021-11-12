from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home' ),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('productDetails/<int:id>/', views.productDetails, name='productDetails'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('search/', views.search, name='search'),
    path('bid/<int:id>/', views.bid, name='bid'),
    path('payment/', views.payment, name = 'payment'),
    path('paid/', views.afterPaid, name='paid'),
    path('history/', views.history, name='history'),
    path('sellerhistory/', views.sellerhistory, name='sellerhistory'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('category/', views.get_product_by_category, name='category'),
    path('comment/<int:id>', views.comment, name='comment'),
    path('editcomment/<int:id>',views.editcomment, name='editcomment'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
]