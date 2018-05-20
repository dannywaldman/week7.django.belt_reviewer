from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserManager(models.Manager):

    def validate(self, post):

        errors = {}

        name = post['name']
        if not len(name) >= 2:
            errors['name_len'] = 'Name must be 2 or more characters'

        alias = post['alias']
        if not len(alias) >= 2:
            errors['alias_len'] = 'Alias must be 2 or more characters'

        password = post['password']
        if not password == post['confirm_password']:
            errors['pw_mismatch'] = 'Passwords must match'
        if not len(password) >= 8:
            errors['pw_len'] = 'Password must be 8 or more characters'

        try:
            validate_email(post['email'])
        except ValidationError:
            errors['email_format'] = 'Email must be a valid address'
        else:
            if not errors:
                if User.objects.filter(email = post['email']):
                    errors['email_unique'] = 'User already exists'


        return errors

class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Author(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, related_name = 'books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Review(models.Model):
    comment = models.TextField()
    rating = models.IntegerField()
    book = models.ForeignKey(Book, related_name = 'reviews')
    user = models.ForeignKey(User, related_name = 'reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
