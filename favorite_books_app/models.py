from django.db import models
import re
import bcrypt 
from django.contrib import messages

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        users=User.objects.all()
        # add keys and values to errors dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name must be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        elif users.filter(email=postData['email']).exists():
            errors["email"] = "This email already exist."
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters."
        if postData['password']!=  postData['conf_pass']:
            errors["conf_pass"] = "Passwords do not match."
        return errors
    
    def login_validator(self, postData):
        errors = {}
        users=User.objects.all()
        # add keys and values to errors dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters."
        return errors

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['title']) =="":
            errors["title"] = "Title is required"
        if len(postData['description']) < 2:
            errors["last_name"] = "Description must be at least 2 characters."
        return errors
# Create your models here.
class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    uploaded_by=models.ForeignKey(User, related_name="uploaded_books", on_delete = models.CASCADE)
    users_who_like=models.ManyToManyField(User, related_name="liked_books")
    objects = BookManager()

def register_new_user(request):    
    # include some logic to validate user input before adding them to the database!
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
    print(pw_hash)      # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'    
    # be sure you set up your database so it can store password hashes this long (60 characters)
    # make sure you put the hashed password in the database, not the one from the form!
    user=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'], email=request.POST['email'],  password=pw_hash)  
    return user  

def create_book(request):
    user=User.objects.get(id=request.POST['uploaded_by'])
    book=Book.objects.create(title=request.POST['title'], description=request.POST['description'], uploaded_by=user)
    user.liked_books.add(book)


def error_reg(request):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.register_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return True
    else:
        request.session['userid'] = register_new_user(request).id
        return False

def error_log(request):
# pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.login_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return  True
    else:
        # see if the email provided exists in the database
        user = User.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
        if user: # note that we take advantage of truthiness here: an empty list will return false
            logged_user = user[0] 
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            # if we get True after checking the password, we may put the user id in session
                request.session['userid'] = logged_user.id
            # never render on a post, always redirect!
                return False
    # if we didn't find anything in the database by searching by username or if the passwords don't match, 
    # redirect back to a safe route
        return True
    


def error_book(request):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Book.objects.book_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return True
    else:
        create_book(request)
        return False

def error_update_book(request,number):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Book.objects.book_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return True
    else:
        book=Book.objects.get(id=number)
        book.title=request.POST['title']
        book.description=request.POST['description']
        book.save()
        return False