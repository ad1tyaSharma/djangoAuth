from django.shortcuts import render,redirect
# Create your views here.
def loginView(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
    return render(request,'users/login.html')
def registerView(request):
    if request.method == 'POST':
        name= request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        print(email,password,name)  
    return render(request,'users/register.html')
def forgotPassView(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email) 
    return render(request,'users/forgotPass.html')
def profileView(request):
    return render(request,'users/profile.html')
def resetPassView(request,id):
    return render(request,'users/resetPass.html')