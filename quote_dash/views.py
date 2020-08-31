from django.shortcuts import render, redirect, HttpResponse
from .models import User, Quote
from django.contrib import messages
import bcrypt

#this is the root page for login & reg
def index(request):
    return render (request, 'index.html')

#register new user
def register(request):
    errors = User.objects.regValidator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email'], password = hashed_pw)
        print(hashed_pw)

        request.session['user_name'] = User.objects.last().first_name + ' ' + User.objects.last().last_name
        request.session['user_id'] = User.objects.last().id
        request.session['email'] = User.objects.last().email     #need this in updateUser method below
        # print(request.session['user_name'], request.session['user_id'])
        return redirect ('/quotes')

def login(request):
    request.session.flush() #logout existing user before login
    errors = User.objects.loginValidator(request.POST)
    # print("login erros:____")
    # print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        #username password check logic is in loginValidator method in models.py 
        #get logged in user from db
        this_user = User.objects.get(email=request.POST['email'])
        request.session['user_name'] = this_user.first_name
        request.session['user_id'] = this_user.id
        request.session['email'] = this_user.email     #need this in updateUser method below
        # print("login successful, redirecting to quotes page")
        # print("THIS USER is ", request.session['user_name'], "id = ", request.session['user_id'])
        return redirect ('/quotes')

def quotes(request):
    #Check if request method was GET (!= POST), then redirect to root
    if request.method != "POST":
        #Check if user_name is not in session
        #this allows the user to directly go to '/quotes' if user is in session; if not, redirect to root
        if 'user_name' not in request.session:
            return redirect('/')
    #On successful log/registration, render the quotes page
    context = {
        "all_quotes" : Quote.objects.all(),
    }
    return render(request, 'quotes.html', context)

def logout(request):
        request.session.flush()
        return redirect('/')

#Methods for Quotes
def postQuote(request):
    errors = Quote.objects.quoteValidator(request.POST)
    #check for input errors
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # return redirect('/quotes')
    else:
        Quote.objects.create(author=request.POST['author'], quote=request.POST['quote'], user=User.objects.get(id=request.session['user_id']))
    return redirect ('/quotes')

def postLike(request):
    liker = User.objects.get(id=request.session['user_id'])
    liked_quote = Quote.objects.get(id=request.POST['quote_id'])
    liked_quote.liked_by.add(liker)
    return redirect ('/quotes')

def deleteQuote(request):
    delete_quote = Quote.objects.get(id=request.POST['quote_id'])
    delete_quote.delete()
    return redirect ('/quotes')

#Methods for Users
def viewUser(request, id):
    context = {
        "this_user" : User.objects.get(id=id)
    }
    return render (request, 'user.html', context)

def editAccount(request):
    context = {
        "this_user" : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'account.html', context)

def updateUser(request):
    errors = User.objects.updateValidator(request.POST, request.session['email'])
    #check for input errors
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit_account')
    else:
        #update the user info
        this_user = User.objects.get(id=request.session['user_id'])
        this_user.first_name=request.POST['firstname']
        this_user.last_name=request.POST['lastname'] 
        this_user.email=request.POST['email']
        this_user.save()
    return redirect ('/quotes')
    