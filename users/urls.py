from django.urls import path
from .views import loginView
from .views import registerView
from .views import profileView
from .views import forgotPassView
from .views import resetPassView
urlpatterns =[
    path('login',loginView),
    path('register',registerView),
    path('profile',profileView),
    path('forgotPass',forgotPassView),
    path('resetPass/:id',resetPassView)

]