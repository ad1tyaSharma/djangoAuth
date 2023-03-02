from django.shortcuts import render,redirect,HttpResponse
import bcrypt   
from .models import Blogger
import jwt
from datetime import datetime, timedelta
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from django.core.mail import send_mail

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
                token = jwt.encode(payload, os.environ.get('JWT_SECRET_KEY'), algorithm='HS256')
                print(token)
                response =  JsonResponse({'token': token})
                response.set_cookie('token', token, expires=datetime.utcnow() + timedelta(days=15))
                return response
            else:
                response =  JsonResponse({'error': 'Invalid Credentials'},status=403)
                return response
        
        else:
            response= JsonResponse({'error': 'Invalid Credentials'},status=403)
            return response
    return render(request,'users/login.html')

@csrf_exempt
def registerView(request):
    if request.method == 'POST':
        raw_data = request.body
        body_unicode = raw_data.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        password = body['password']
        name= body['name']
        print(body)
        if Blogger.objects.filter(email__exact=email):
            response =  JsonResponse({'error': 'Email already registered'},status=400)
            return response
        else:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            blogger = Blogger(name = name,email = email,password= hashed.decode('utf-8'))
            blogger.save()
            return redirect('login')
    return render(request,'users/register.html')

@csrf_exempt
def forgotPassView(request):
    if request.method == 'POST':
        raw_data = request.body
        body_unicode = raw_data.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        if Blogger.objects.filter(email__exact=email):
            payload = {
                    'email': email,
                    'exp': datetime.utcnow() + timedelta(minutes=5),
                }
            token = jwt.encode(payload, os.environ.get('JWT_SECRET_KEY'), algorithm='HS256')
            send_mail('Password Reset Link', f"<div style='font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2'><div style='margin:50px auto;width:70%;padding:20px 0'><div style='border-bottom:1px solid #eee'><a href='{os.environ.get('HOST')}/' style='font-size:1.4em;color: #01D28E;text-decoration:none;font-weight:600'>Webie</a></div><p style='font-size:1.1em'>Hi,</p><p>We received a request to reset your password.Reset link is valid for 5 minutes</p><a href='{os.environ.get('HOST')}/users/resetPass/{token}' style='background: #01D28E; text-decoration: none;margin: 0 auto;width: max-content;padding: 10px 10px;color: #fff;border-radius: 4px;'>Reset Password</a><p style='font-size:0.9em;'>Regards,<br />Your Brand</p><hr style='border:none;border-top:1px solid #eee' /></div></div>", 'mail4trial4@gmail.com', [f'{email}'], fail_silently=False)
            response = JsonResponse({'msg': 'Link Sent'},status=200)
            return response
        else:
            response = JsonResponse({'error': 'User not found!!'},status=400)
            return response
    return render(request,'users/forgotPass.html')
def profileView(request):
    return render(request,'users/profile.html')

@csrf_exempt
def resetPassView(request,id):
    if request.method == 'POST':
        raw_data = request.body
        body_unicode = raw_data.decode('utf-8')
        body = json.loads(body_unicode)
        password= body['password']
        decoded_data = jwt.decode(id, os.environ.get('JWT_SECRET_KEY'), algorithms=['HS256'])
        # Access the decoded data
        email = decoded_data['email']
        blogger = Blogger.objects.get(email__exact=email)
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        blogger.password = hashed.decode('utf-8')
        blogger.save()
        response = JsonResponse({'msg':"Password Updated!"},status=200)
        return response
    elif request.method == 'GET':
        try:
            # Decode the JWT without verifying the signature
            decoded_data = jwt.decode(id, os.environ.get('JWT_SECRET_KEY'), algorithms=['HS256'])

            # Access the expiration time from the decoded data
            expiration_time = datetime.fromtimestamp(decoded_data['exp'])

            # Check if the token has expired
            if expiration_time < datetime.utcnow():
                # Handle expired token error
                return redirect('login')

            else:
                # Token is valid
                return render(request,'users/resetPass.html',{'id':id})

        except jwt.DecodeError:
            # Handle decoding error
            return redirect('login')

        except jwt.ExpiredSignatureError:
            # Handle expired token error
            return redirect('login')

def not_found(request, exception):
    return render(request, '404.html', status=404)    

   