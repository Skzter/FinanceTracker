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
    ausgaben = []
    for x in range(1,13):
        monat = items.filter(month=x) 
        # alle Einnahmen
        Ein = [eintrag.amount for eintrag in monat.filter(type='E')]
        sumE = 0
        for e in Ein:
            sumE+=e
        einnahmen.append(sumE) 

        # alle Ausgaben
        Aus = [eintrag.amount for eintrag in monat.filter(type='A')]
        sumA = 0
        for e in Ein:
            sumA+=e
        ausgaben.append(sumA) 

    months = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
              'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'
              ]
    type = ['Einnahmen', 'Ausgaben']

    data = {'months': months,
            'Einnahmen': einnahmen,
            'Ausgaben': ausgaben
            }

    x = [(m, t) for m in months for t in type]

    counts = sum(zip(data['Einnahmen'], data['Ausgaben']), ())

    source = ColumnDataSource(data=dict(x=x, counts=counts))

    plot = figure(x_range=FactorRange(*x), height=300,
                  title="Jahresübersicht Einnahmen/Ausgaben",
                  toolbar_location=None, tools="")
    plot.vbar(x='x', top='counts', width=0.9, source=source)

    script, div = components(plot)
    """
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    years = ['2015', '2016', '2017']

    data = {'fruits' : fruits,
            '2015'   : [2, 1, 4, 3, 2, 4],
            '2016'   : [5, 3, 3, 2, 4, 6],
            '2017'   : [3, 2, 4, 4, 5, 3]}

    # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
    x = [ (fruit, year) for fruit in fruits for year in years ]
    counts = sum(zip(data['2015'], data['2016'], data['2017']), ()) # like an hstack

    source = ColumnDataSource(data=dict(x=x, counts=counts))

    p = figure(x_range=FactorRange(*x), height=350, title="Fruit Counts by Year",
               toolbar_location=None, tools="")

    p.vbar(x='x', top='counts', width=0.9, source=source)
    script, div = components(p)
    """
    context = {}
    context["script"] = script
    context["div"] = div   
    

    return render(request, "home.html", context)
