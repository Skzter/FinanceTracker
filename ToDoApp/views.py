from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Ausgaben
from django.urls import reverse
from .forms import AusgabenForm
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange

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
    return render(request, "ausgaben.html", context)


def index(request):
    # Barchart mit allen Monaten, wo Ausgaben u Eingaben gesamtheitlich angezeigt werden
    # Monate Jan - Dez
    # Ausgaben/Einnahmen aus DB
    items = Ausgaben.objects
    einnahmen = []
    ausgaben = {}
    for x in range(1,12):
        monat = items.filter(month=x) 
        # alle Einnahmen
        Ein = [eintrag.amount for eintrag in monat.filter(type='E')]
        sum = 0
        for e in Ein:
            sum+=e
        einnahmen.append(sum) 

        # alle Ausgaben
        Aus = [eintrag.amount for eintrag in monat.filter(type='A')]
        ausgaben[x] = Aus
    
    print("Einnahmen\n")
    print(einnahmen)
    print("Ausgaben\n")
    print(ausgaben)
    plot = figure(width=1200, height=200)
    plot.toolbar_location = None
    plot.tools = []
 
    script, div = components(plot)
    context = {}
    context["script"] = script
    context["div"] = div   
    return render(request, "home.html", context)
