from __future__ import unicode_literals
from django.db import models
from datetime import date
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        flag = True
        errors = {}
        if len(postData['name']) < 3:
            flag = False
            errors["name"] = "Name should be atleast 3 characters!"
        if len(postData['alias']) < 3:
            flag = False
            errors["alias"] = "Alias should be atleast 3 character!"
        if len(postData['email']) < 1:
            flag = False
            errors["email"] = "Email should not be left blank"
        if not EMAIL_REGEX.match(postData['email']):
            flag = False
            errors["email"] = "Email is not valid!"
        if len(postData['pwd']) < 8:
            flag = False
            errors["pwd"] = "Password should contain atleast 8 characters"
        if postData['pwd'] != postData['confirm_pwd']:
            flag = False
            errors["pwd"] = "Password does not match Confirm Password"
        if postData['dob'] > unicode(date.today()):
            flag = False
            errors["dob"] = "Date of Birth must be before Today's Date!"
        if len(postData['dob']) < 1:
            flag = False
            errors["dob"] = "Date of Birth should not be blank!"
        if User.objects.filter(email=postData['email']).exists(): #checks to see if email is in the database
            flag = False
            errors['email'] = "Email already exists! Login or Register another email"

        if flag:
            hashpwd = bcrypt.hashpw(postData['pwd'].encode('utf-8'), bcrypt.gensalt())
            user = User.objects.create(name=postData['name'], alias=postData['alias'], email=postData['email'], password=hashpwd, dob=postData['dob'])
            return (True, user)
        else:
            return (False, errors)
    
    def login_validator(self, postData):
        flag = True
        errors = {}
        email = postData["email"]
        try:
            user = User.objects.get(email=email)
        except:
            flag = False
            errors["email"] = "Email does not exist in database please register or try again"
            return (False, errors)
        if not EMAIL_REGEX.match(email):
            flag = False
            errors["email"] = "Email is not valid!"
        if len(email) < 1:
            flag = False
            errors["email"] = "Email should not be left blank"

        pwd = User.objects.get(email=email).password
        user_pwd = postData['pwd']
        
        if not bcrypt.checkpw(user_pwd.encode('utf-8'), pwd.encode('utf-8')):
            flag = False
            errors["password"] = "Password does not match please try again"
        
        if flag:
            user = User.objects.get(email=email)
            return (True, user)
        else:
            return (False, errors)

        

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    objects = UserManager()

class QuoteManager(models.Manager):
    def basic_validator(self, postData):
        # flag = True
        errors = {}
        if len(postData['author']) < 3:
            # flag = False
            errors["author"] = "Quoted by must be atleast 3 characters!"
        if len(postData['message']) < 10:
            # flag = False
            errors["message"] = "Message must be atleast 10 characters!"

        return errors

class Quote(models.Model):
    author = models.CharField(max_length=255)
    message = models.TextField()
    poster = models.ForeignKey(User, related_name="posted_quote")
    user_favorited = models.ManyToManyField(User, related_name="favorite")
    objects = QuoteManager()