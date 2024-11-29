from django import forms
from flights.models import Airport,Flight,Passenger 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ['code', 'city'] 

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['origin', 'destination', 'duration'] 

    
    origin = forms.ModelChoiceField(queryset=Airport.objects.all(), required=True, empty_label="Select Origin Airport")
    destination = forms.ModelChoiceField(queryset=Airport.objects.all(), required=True, empty_label="Select Destination Airport")

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first', 'last', 'flights']

    flights = forms.ModelMultipleChoiceField(queryset=Flight.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
