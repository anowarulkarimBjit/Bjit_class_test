from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout 
from .forms import AirportForm, FlightForm, PassengerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm




# Create your views here.

@login_required
def index(request):
    return render(request,"users/user.html")

def login_view(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html",{
                "message":"invalid username or password"
            })

    return render(request,"users/login.html")

@login_required
def changePass(request):
    if request.method == "POST":
        user = request.user
        old_pass = request.POST["old_pass"]
        new_pass = request.POST["new_pass"]
        
        user_check = authenticate(username=user.username, password=old_pass)
        
        if user_check is not None:
            user.set_password(new_pass)
            user.save()
            messages.success(request, "Password successfully updated!")
            return redirect("users:index")
        else:
            messages.error(request, "Old password is incorrect.")
            return render(request, "users/changePass.html")
    
    return render(request, "users/changePass.html")

def logout_view(request):
    logout(request)
    return render(request,"users/login.html",{
        "message":"Logged Out"
    })

@login_required
def add_airport(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"),)
    if request.method == 'POST':
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('users:index') 
    else:
        form = AirportForm()

    return render(request, 'users/addAirport.html', {
        'form': form
    })

@login_required
def add_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('users:index') 
    else:
        form = FlightForm()

    return render(request, 'users/add_flight.html', {'form': form})


@login_required
def add_passenger(request):

    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('users:index')
    else:
        form = PassengerForm()

    return render(request, 'users/add_passenger.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('flight:index') 
        else:
            messages.error(request, 'There was an error during signup. Please try again.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/signup.html', {'form': form})
