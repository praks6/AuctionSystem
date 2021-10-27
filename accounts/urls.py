from django.urls import path
from . import views
urlpatterns = [
  path('signup/seller/',views.signuSeller,name='signupseller'),
  path('signup/buyer/',views.signupBuyer,name='signupbuyer'),
  path('signin/',views.signin,name='signin'),
  path('logout/',views.signout,name='logout'),
  path('buyer/dashboard/',views.buyerDashboard,name='buyerDashboard'),
  path('seller/dashboard/',views.sellerDashboard,name='sellerDashboard'),
]