from django.urls import path
from . import views

app_name = "ToDoApp"

urlpatterns = [
    path("", views.index, name="index"),
    path("month/<int:month>/", views.ausgaben, name="ausgaben"),
]
