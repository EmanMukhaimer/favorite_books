from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def index(request):
    return render(request, "index.html")



def register(request):  
    if error_reg(request):
        return redirect("/")
    else:
        return redirect('/success')

def login(request):
    if error_log(request):
        return redirect("/")
    else: 
        return redirect('/books')


def display_books(request):
    # Don't allow a user who is not logged in to reach the /success route (i.e. by making a GET request in the address bar)
    if 'userid' in request.session:
        context={
            'user':User.objects.get(id=request.session['userid']),
            'books':Book.objects.all(),
        }
        return render(request, "books.html", context)
    return redirect("/")


def add_book(request):
    if error_book(request):
        return redirect("/")
    else: 
        return redirect('/books')


def view_book(request, number):
    context={
        'user':User.objects.get(id=request.session['userid']),
        'book':Book.objects.get(id=number)
    }
    return render(request, "book.html", context)

def add_fav(request, book_id, user_id):
    user=User.objects.get(id=user_id)
    book=Book.objects.get(id=book_id)
    user.liked_books.add(book)
    return redirect('books', number=book_id)


def remove_fav(request, book_id, user_id):
    user=User.objects.get(id=user_id)
    book=Book.objects.get(id=book_id)
    user.liked_books.remove(book)
    return redirect('books', number=book_id)

def update_book(request, number):
    error_update_book(request,number)
    return redirect('books', number=number)

def delete_book(request, number):
    Book.objects.get(id=number).delete()
    return redirect('/books')

def logout(request):
    request.session.clear()	
    return redirect('/')

def display_user_page(request):
    context={
        'user':User.objects.get(id=request.session['userid']),
    }
    return render(request, "user_page.html", context)