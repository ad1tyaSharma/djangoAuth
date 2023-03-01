from django.shortcuts import render,redirect,HttpResponse
import bcrypt   
from .models import Blogger
import jwt
from datetime import datetime, timedelta
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def loginView(request): 
    if request.method == 'POST':
        raw_data = request.body
        body_unicode = raw_data.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']
        
        if Blogger.objects.filter(email__exact=email):
            blogger = Blogger.objects.get(email__exact=email)
            print(blogger.password)
            if bcrypt.checkpw(password.encode('utf-8'), blogger.password.encode('utf-8')):
                print('Password matches')
                payload = {
                    'email': email,
                    'name': blogger.name,
                    'role': blogger.role,
                    'exp': datetime.utcnow() + timedelta(days=15),
                }
                token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
                print(token)
                response =  JsonResponse({'token': token})
                response.set_cookie('token', token, expires=datetime.utcnow() + timedelta(days=15))
                return response
            else:
                response =  JsonResponse({'error': "Invalid Credentials"},status=403)
                return response
        
        else:
            response= JsonResponse({'error': "Invalid Credentials"},status=403)
            return response
    return render(request,'users/login.html')
def registerView(request):
    if request.method == 'POST':
        name= request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        blogger = Blogger(name = name,email = email,password= hashed.decode('utf-8'))
        blogger.save()
        return redirect('login')
    return render(request,'users/register.html')
def forgotPassView(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email) 
    return render(request,'users/forgotPass.html')
def profileView(request):
    return render(request,'users/profile.html')
def resetPassView(request,id):
    if request.method == 'POST':
        password1= request.POST['password-1']
        password2 = request.POST['password-2']
        print(password1,password2)
    return render(request,'users/resetPass.html')