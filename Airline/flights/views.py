from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . models import *
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Flight
from .serializers import FlightSerializer



def index(request):

    flights=Flight.objects.all()
    
    return render(request,"flights/index.html",{
        "flights":flights
    })

@login_required
def flight(request,flight_id):
    flight_details=Flight.objects.get(pk=flight_id)

    return render(request,"flights/flight.html",{
        "flight":flight_details,
        "passengers":flight_details.passenger.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight_details).all()
    })

@login_required
def book(request,flight_id):
    if request.method=="POST":
        flight=Flight.objects.get(pk=flight_id)
        passennger=Passenger.objects.get(pk=int(request.POST["passenger"]))
        passennger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight:flight",args=(flight.id,)))
    
@login_required
def delete_flight(request, flight_id):
    if request.method == "POST":
        flight = get_object_or_404(Flight, pk=flight_id)
        flight.delete()
        return HttpResponseRedirect(reverse("flight:index"))



@api_view(['GET', 'POST'])
def flight_list(request):
    if request.method == 'GET':
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE','PATCH'])
def flight_detail(request, pk):
    try:
        flight = Flight.objects.get(pk=pk)
    except Flight.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FlightSerializer(flight)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = FlightSerializer(flight, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

