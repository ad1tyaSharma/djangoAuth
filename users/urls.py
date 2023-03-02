from django.urls import path
from .views import loginView
from .views import registerView
from .views import profileView
from .views import forgotPassView
from .views import resetPassView
from .views import not_found
urlpatterns =[
    path('login',loginView,name='login'),
    path('register',registerView,name='register'),
    path('profile',profileView),
    path('forgot-password',forgotPassView),
    path('resetPass/<str:id>/',resetPassView)

]
