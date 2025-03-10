from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Ausgaben
from django.urls import reverse
from .forms import AusgabenForm
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral5

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
    items = Ausgaben.objects
    einnahmen = []
    ausgaben = []
    for x in range(1,13):
        monat = items.filter(month=x) 
        Ein = [eintrag.amount for eintrag in monat.filter(type='E')]
        einnahmen.append(float(sum(Ein))) 
        Aus = [eintrag.amount for eintrag in monat.filter(type='A')]
        ausgaben.append(float(sum(Aus))) 
    months = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
              'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    type = ['E', 'A']
    data = {'months': months,
            'E': einnahmen,
            'A': ausgaben}

    x = [(m, t) for m in months for t in type]
    counts = sum(zip(data['E'], data['A']), ())
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    plot = figure(x_range=FactorRange(*x), width=1200, height=500,
                  title="Jahresübersicht Einnahmen/Ausgaben",
                  toolbar_location=None, tools="")
    plot.vbar(x='x', top='counts', width=0.9, source=source,
              fill_color=factor_cmap('x', palette=Spectral5, factors=type, start=1, end=2))
    script, div = components(plot)

    context = {}
    context["script"] = script
    context["div"] = div   

    return render(request, "home.html", context)
