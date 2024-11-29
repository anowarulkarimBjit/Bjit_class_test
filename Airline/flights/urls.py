from django.urls import path
from . import views
app_name="flight"
urlpatterns=[
    path("",views.index,name="index"),
    path("<int:flight_id>",views.flight,name="flight"),
    path("<int:flight_id>/book",views.book,name="book"),
    path("<int:flight_id>/delete/", views.delete_flight, name="delete_flight"),
    path('api/flights/', views.flight_list, name='flight_list'),
    path('api/flights/<int:pk>/', views.flight_detail, name='flight_detail'),
]