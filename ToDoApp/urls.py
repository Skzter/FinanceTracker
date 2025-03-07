from django.urls import path
from . import views

app_name = "ToDoApp"

urlpatterns = [
    path("", views.index, name="index"),
    path("finanzen/<int:month>/", views.ausgaben, name="ausgaben"),
]
