from django.urls import path

from . import views
app_name="users"
urlpatterns=[
    path("",views.index,name="index"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("changePass/",views.changePass,name="changePass"),
    path('add_airport/', views.add_airport, name='add_airport'),
    path('add_flight/', views.add_flight, name='add_flight'),
    path('add_passenger/', views.add_passenger, name='add_passenger'),
    path('signup/', views.signup, name='signup'),
]