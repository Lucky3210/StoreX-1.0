from django.shortcuts import render, redirect
import boto3
from django.http import HttpResponse
from Crypto.Cipher import AES
import os
import secrets
from django.http import HttpResponse
from .models import User
from .forms import MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def homePage(request):
    # return HttpResponse("Let's go filing")
    return render(request, 'home.html')


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('storePage')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, 'User not found, Proceed to register.')

        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request, user)
            return redirect('storePage')
        
        else:
            messages.error(request, 'Email or Password does not exist.')
    return render(request, 'login.html')


def registerPage(request):

    form = MyUserCreationForm() # create an instance of the form created in forms.py

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST) # the values filled in the form is placed in the post request
        if form.is_valid():
            user = form.save(commit=False)
            user.firstname = user.firstname.lower()
            user.save()
            login(request, user)
            return redirect('storePage')

        else:
            messages.error(request, 'An error occured during registration')
            form = MyUserCreationForm()
        # firstname = request.POST("first_name")
        # lastname = request.POST("last_name")
        # phone_number = request.POST("phone")
        # email = request.POST('email')
    return render(request, 'register.html', {'form': form})

def storePage(request):
    return render(request, 'fileapp/store_home.html')


def add_file(request):
    if request.method == 'POST':
        s3 = boto3.client('s3')
        file = request.FILES['file']

        if file.content_type in []:

            # perform encryption
            key = secrets.token_bytes(16)
            encrypt_file(file, key) # encrypt the file then upload it to s3

            s3.upload_fileobj(file, 'bucket_name', file.name, ExtraArgs={'ContentType': file.content_type})
            return HttpResponse('File Stored Successfully')

        else:
            return HttpResponse('Invalid file type..')
        
    else:
        return HttpResponse('Failed to store file')

def encrypt_file(file, key):
    """
    Encrypt the contents of a file using AES (CBC mode)
    :param file: file-like object to encrypt
    :param key: encryption key - a bytes object of length 16, 24 or 32
    :return: the encrypted data
    """

    iv = os.urandom(16)  # Generate a random initialization vector
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = file.read()
    padded_data = pad(data)  # pad the data to a multiple of 16 bytes
    encrypted_data = cipher.encrypt(padded_data)
    return iv + encrypted_data

def pad(data):
    """
    Pad the data using the PKCS#7 padding scheme
    :param data: the data to pad
    :return: the padded data
    """
    padding_size = AES.block_size - (len(data) % AES.block_size)
    padding = bytes([padding_size]) * padding_size
    return data + padding
