from django.shortcuts import render
import boto3
from django.http import HttpResponse
from Crypto.Cipher import AES
import os
import secrets

# Create your views here.


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
