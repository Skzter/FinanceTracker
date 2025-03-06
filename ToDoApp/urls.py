from django.urls import path
from . import views

app_name = "ToDoApp"

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("add/addrecord/", views.addrecord, name="addrecord"),
    path("finanzen/<int:month>/", views.ausgaben, name="ausgaben"),
]
