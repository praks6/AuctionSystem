from django.urls import path
from . import views
urlpatterns = [
  path('signup/seller/',views.signupSeller,name='signupseller'),
  path('signup/buyer/',views.signupBuyer,name='signupbuyer'),
  path('signin/',views.signin,name='signin'),
  path('logout/',views.signout,name='logout'),
  path('buyer/dashboard/',views.buyerDashboard,name='buyerDashboard'),
  path('seller/dashboard/',views.sellerDashboard,name='sellerDashboard'),
  path('productDetails/<int:id>/', views.productDetails, name='productDetails'),
  path('addProduct/',views.addProduct,name='addProduct'),
]