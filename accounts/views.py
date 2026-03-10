from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from  django.contrib.auth import login, logout
from django import forms



def index(request):

    name = ""
    if request.user.is_authenticated:
        name = request.user.username
        return render(request, 'accounts/index.html',{
        "name":name,
        })

    return render(request, "accounts/base.html")



def register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("accounts:index")
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html',{
        "form" : form,
    })



def login_mine(request):
    flag = False
    if request.method == "POST":
        user = AuthenticationForm(request, data=request.POST)
        if user.is_valid():
            login(request, user.get_user())
            return redirect("accounts:index")
        else:
            flag = True
            form = AuthenticationForm()
            return render(request, 'accounts/login.html',{
            "form" : form,
            "sayno" : flag, 
            })

    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html',{
        "form" : form,
        "sayno" : flag,
        })
    

def logout_view(request):
    logout(request)
    return render(request, 'accounts/base.html')