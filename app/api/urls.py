
from django.urls import path,include
from .views import *
urlpatterns = [
    path('register',RegisterView.as_view(),name='register'),
    path('login',LoginApiView.as_view(),name='login'),
    path('book',BookView.as_view(),name='book'),
    path('cart',BookRegister.as_view(),name='cart')

]