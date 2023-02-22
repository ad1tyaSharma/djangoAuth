from django.shortcuts import render,redirect
from .forms import userForm
# Create your views here.
def loginView(request):
    return render(request,'users/login.html')
def registerView(request):
    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.likes = []
            post.save()
            return redirect('users/login')
    else:
        form = userForm()

    return render(request,'users/register.html',{'form': form})
def forgotPassView(request):
    return render(request,'users/forgotPass.html')
def profileView(request):
    return render(request,'users/profile.html')
def resetPassView(request,id):
    return render(request,'users/resetPass.html')