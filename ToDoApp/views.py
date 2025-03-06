from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Ausgaben
from django.urls import reverse
from .forms import AusgabenForm


# Create your views here.
def ausgaben(request, month):
    alleAusgaben = Ausgaben.objects.all()
    ausgabenMonth = alleAusgaben.filter(month=month)
    context = {}
    context["ausgaben"] = ausgabenMonth
    form = AusgabenForm(initial={"month": month})
    context["form"] = form
    return render(request, "ausgaben.html", context)


def index(request):
    return render(request, "home.html")


def add(request):
    return render(request, "add.html")


def addrecord(request):
    type = request.POST["type"]
    month = request.POST["month"]
    category = request.POST["category"]
    title = request.POST["title"]
    amount = request.POST["amount"]
    item = Ausgaben(
        type=type, month=month, category=category, title=title, amount=amount
    )
    item.save()

    return HttpResponseRedirect(reverse("ausgaben"))
