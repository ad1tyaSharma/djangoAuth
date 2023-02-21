from django.shortcuts import render

# Create your views here.
def loginView(request):
    return render(request,'users/login.html')
def registerView(request):
    return render(request,'users/register.html')
def forgotPassView(request):
    return render(request,'users/forgotPass.html')
def profileView(request):
    return render(request,'users/profile.html')
def resetPassView(request):
    return render(request,'users/resetPass.html')