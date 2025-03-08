from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Ausgaben
from django.urls import reverse
from .forms import AusgabenForm


# Create your views here.
def ausgaben(request, month):
    alleAusgaben = Ausgaben.objects.all()
    ausgabenMonth = alleAusgaben.filter(month=month)
    context = {}
    context["monat"] = month
    context["ausgaben"] = ausgabenMonth
    form = AusgabenForm(initial={"month": month})

    if request.method == 'POST':
        if 'save' in request.POST:
            pk = request.POST.get('save')
            if not pk:
                form = AusgabenForm(request.POST)
            else:
                ausgabe = Ausgaben.objects.get(id=pk)
                form = AusgabenForm(request.POST, instance=ausgabe)
            form.save()
            form = AusgabenForm(initial={"month": month})
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            ausgabe = Ausgaben.objects.get(id=pk)
            form = AusgabenForm(instance=ausgabe)

        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            ausgabe = Ausgaben.objects.get(id=pk)
            ausgabe.delete()

    context["form"] = form
    print(context)
    return render(request, "ausgaben.html", context)


def index(request):
    return render(request, "home.html")
