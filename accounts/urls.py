from django.urls import path
from . import views
urlpatterns = [
  path('signup/seller/',views.signupSeller,name='signupseller'),
  path('signup/buyer/',views.signupBuyer,name='signupbuyer'),
  path('signin/',views.signin,name='signin'),
  path('logout/',views.signout,name='logout'),
]