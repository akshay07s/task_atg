from django.urls import path
from myapp import views 

urlpatterns = [
    path("frequency/", views.frequency , name="frequency"),
    path("result/", views.result , name="result")
]
