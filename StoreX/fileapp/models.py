from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage # lib to use aws storage backend to store files
from .validators import validators
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'private'

# By setting the location attribute to 'media', you are specifying that all files uploaded using this storage backend should be stored under a top-level directory called 'media' in the S3 bucket. For example, if you have a file called 'example.pdf' and the upload_to attribute is set to 'files/', the file would be stored in the S3 bucket at the path 'media/files/example.pdf'.
# With this code, you are using the MediaStorage class to configure the file storage backend to use S3, with the specified location and default access control settings.


# we create our own user model rather using the one provided for us by django, 
# the essence of this is to customize our user properties and also enable logging in with the details we want
class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    phone = PhoneNumberField()

    avatar = models.ImageField(null=True, default="avatar.svg") # the avatar will be in the static folder, and inside images

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# User file model
class File(models.Model):
    file_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/', storage=MediaStorage, validators=validators) # here we can use the mediastorage as our storage class
    uploaded = models.DateTimeField(default=timezone.now)
    shared_with = models.ManyToManyField(User, related_name='shared_files', blank=True)
