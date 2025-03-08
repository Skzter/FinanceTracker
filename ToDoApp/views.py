from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Ausgaben
from django.urls import reverse
from .forms import AusgabenForm
from bokeh.plotting import figure
from bokeh.embed import components

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
 
    # Bokeh Test
    #create a plot
    plot = figure(width=400, height=400)

    plot.toolbar_location = None
    plot.tools = []
 
   # add a circle renderer with a size, color, and alpha
    plot.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
 
    script, div = components(plot)
    context = {}
    context["script"] = script
    context["div"] = div   
    return render(request, "home.html", context)
