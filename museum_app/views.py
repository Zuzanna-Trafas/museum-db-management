from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.db import connection
from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Bar
from museum_app.forms import OddzialForm, DzialForm, ObrazForm, RzezbaForm, ArtystaForm, BiletForm, RodzajBiletuForm, \
    PracownikForm, HarmonogramZwiedzaniaForm, WydarzenieForm, DetailedArtystaForm, DetailedDzialForm, DetailedDzieloForm, DetailedOddzialForm
from museum_app.models import Oddzial, Wydarzenie, Wydarzenie_oddzial, Rodzaj_biletu, Pracownik, Harmonogram_zwiedzania, Bilet, Dzial, Artysta, Obraz, Rzezba


def get_profit(cursor, typ, czy_z_przewodnikiem, oddzial):
    cursor.execute("SELECT policz_dochod(%s, %s, %s)", [typ, czy_z_przewodnikiem, oddzial])
    return cursor.fetchone()[0]

def main(request):
    # TODO searching
    cursor = connection.cursor()
    rodzaj_biletu = Rodzaj_biletu.objects.all()
    x = []
    y = []
    for bilet in rodzaj_biletu:
        y.append(get_profit(cursor, bilet.typ, bilet.czy_z_przewodnikiem, bilet.oddzial_nazwa.nazwa))
        guide = ""
        if bilet.czy_z_przewodnikiem:
            guide = "<br> z przewodnikiem"
        else:
            guide = "<br> bez przewodnika"
        x.append(str(bilet.typ) + "<br>" + str(bilet.oddzial_nazwa.nazwa) + guide)

    plot_div = plot([Bar(x=x, y=y, marker=dict(color='rgb(108,117,125)'))], output_type='div')
    cursor.close()
    return render(request, 'museum_app/main.html', context={'plot_div': plot_div})


# TODO for all table views button ids have to include records primary key. Pass the id to detailed and edit views by url for example detailed/oddzial/10
# TODO for dziela we have to also pass type (obraz/rzeźba) to know which model to use
# TODO fill the table views with data
# TODO somehow handle "usuń" button
# everything done for table views has to be done also for detailed_oddzial for wydarzenia
def oddzialy(request):
    oddzialy = Oddzial.objects.all()
    context = {'oddzialy': oddzialy}
    return render(request, 'museum_app/oddzialy.html', context)


def dzialy(request):
    dzialy = Dzial.objects.all()
    oddzialy = Oddzial.objects.all()
    context = {'dzialy': dzialy, 'oddzialy': oddzialy}
    return render(request, 'museum_app/dzialy.html', context)


def dziela(request):
    obrazy = Obraz.objects.all()
    rzezby = Rzezba.objects.all()
    context = {'obrazy': obrazy, 'rzezby': rzezby}
    return render(request, 'museum_app/dziela.html', context)


def artysci(request):
    artysci = Artysta.objects.all()
    context = {'artysci': artysci}
    return render(request, 'museum_app/artysci.html', context)


def bilety(request):
    bilety = Bilet.objects.all()
    rodzaje_biletow = Rodzaj_biletu.objects.all()
    context = {'bilety': bilety, 'rodzaje_biletow': rodzaje_biletow}
    return render(request, 'museum_app/bilety.html', context)


def pracownicy(request):
    pracownicy = Pracownik.objects.all()
    context = {'pracownicy': pracownicy}
    return render(request, 'museum_app/pracownicy.html', context)


def harmonogram_zwiedzania(request):
    cursor = connection.cursor()
    cursor.execute('CALL podsumowanie_zwiedzania()')
    podsumowanie = cursor.fetchall()
    cursor.close()
    context = {'podsumowanie': podsumowanie}

    return render(request, 'museum_app/harmonogram_zwiedzania.html', context)


# TODO handle adding for all tables (also wydarzenia)
# TODO redirect to table view after submit


def add_oddzial(request):
    form = OddzialForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
    return render(request, 'museum_app/add_oddzial.html', {'form': form})


def add_dzial(request):
    form = DzialForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
    return render(request, 'museum_app/add_dzial.html', {'form': form})


def add_obraz(request):
    # TODO dynamically fill Działy depending on Oddziały or merge both to one select field
    form = ObrazForm(request.POST)
    return render(request, 'museum_app/add_obraz.html', {'form': form})


def add_rzezba(request):
    # TODO dynamically fill Działy depending on Oddziały or merge both to one select field
    form = RzezbaForm(request.POST)
    return render(request, 'museum_app/add_rzezba.html', {'form': form})


def add_artysta(request):
    form = ArtystaForm(request.POST)
    return render(request, 'museum_app/add_artysta.html', {'form': form})


def add_bilet(request):
    form = BiletForm(request.POST)
    return render(request, 'museum_app/add_bilet.html', {'form': form})


def add_rodzaj_biletu(request):
    form = RodzajBiletuForm(request.POST)
    return render(request, 'museum_app/add_rodzaj_biletu.html', {'form': form})


def add_pracownik(request):
    form = PracownikForm(request.POST)
    return render(request, 'museum_app/add_pracownik.html', {'form': form})


def add_harmonogram_zwiedzania(request):
    form = HarmonogramZwiedzaniaForm(request.POST)
    return render(request, 'museum_app/add_harmonogram_zwiedzania.html', {'form': form})


def add_wydarzenie(request):
    form = WydarzenieForm(request.POST)
    return render(request, 'museum_app/add_wydarzenie.html', {'form': form})

# TODO handle editing for all tables (also wydarzenia) - fill values with initial, like for detailed
# TODO disable primary keys after filling them for editing
# TODO figure out how to fill date and time fields
# TODO redirect to table view after submit

def edit_oddzial(request):
    form = OddzialForm(request.POST)
    return render(request, 'museum_app/add_oddzial.html', {'form': form})


def edit_dzial(request):
    form = DzialForm(request.POST)
    return render(request, 'museum_app/add_dzial.html', {'form': form})


def edit_obraz(request):
    # TODO dynamically fill Działy depending on Oddziały or merge both to one select field
    form = ObrazForm(request.POST)
    return render(request, 'museum_app/add_obraz.html', {'form': form})


def edit_rzezba(request):
    # TODO dynamically fill Działy depending on Oddziały or merge both to one select field
    form = RzezbaForm(request.POST)
    return render(request, 'museum_app/add_rzezba.html', {'form': form})


def edit_artysta(request):
    form = ArtystaForm(request.POST)
    return render(request, 'museum_app/add_artysta.html', {'form': form})


def edit_bilet(request):
    form = BiletForm(request.POST)
    return render(request, 'museum_app/add_bilet.html', {'form': form})


def edit_rodzaj_biletu(request):
    form = RodzajBiletuForm(request.POST)
    return render(request, 'museum_app/add_rodzaj_biletu.html', {'form': form})


def edit_pracownik(request):
    form = PracownikForm(request.POST)
    return render(request, 'museum_app/add_pracownik.html', {'form': form})


def edit_harmonogram_zwiedzania(request):
    form = HarmonogramZwiedzaniaForm(request.POST)
    return render(request, 'museum_app/add_harmonogram_zwiedzania.html', {'form': form})


def edit_wydarzenie(request):
    form = WydarzenieForm(request.POST)
    return render(request, 'museum_app/add_wydarzenie.html', {'form': form})


# TODO fill initial values with values from model

def detailed_oddzial(request, oddzial_nazwa):
    oddzial = get_object_or_404(Oddzial, pk=oddzial_nazwa)
    wydarzenie_oddzial = []
    for i in Wydarzenie_oddzial.objects.all():
        if i.oddzial_nazwa_id == oddzial.nazwa:
            wydarzenie_oddzial.append(i)
    wydarzenia = []
    for wydarzenie in Wydarzenie.objects.all():
        for i in wydarzenie_oddzial:
            if wydarzenie.nazwa == i.wydarzenie_nazwa_id and wydarzenie.data_rozpoczecia == i.wydarzenie_data_rozpoczecia_id:
                wydarzenia.append(wydarzenie)
    initial_values = {'name': oddzial.nazwa, 'opening_hour': oddzial.godzina_otwarcia,
                      'closing_hour': oddzial.godzina_zamkniecia, 'address': oddzial.adres,
                      'number': oddzial.numer_telefonu}
    form = DetailedOddzialForm(initial=initial_values)
    return render(request, 'museum_app/detailed_oddzial.html', {'form': form, 'wydarzenia': wydarzenia})


def detailed_dzial(request, dzial_nazwa, oddzial_nazwa):
    initial_values = {}
    print(oddzial_nazwa)
    for dzial in Dzial.objects.all():
        print(dzial.oddzial_nazwa.)
        if dzial.nazwa == dzial_nazwa and dzial.oddzial_nazwa_id == oddzial_nazwa:
            initial_values = {
                "name": dzial.nazwa,
                "oddzial": dzial.oddzial_nazwa,
                "floor": dzial.pietro,
                "epoch": dzial.epoka
            }
    if initial_values == {}:
        raise Http404("Dział nie istnieje")
    form = DetailedDzialForm(initial=initial_values)
    return render(request, 'museum_app/detailed_dzial.html', {'form': form})


def detailed_artysta(request, artysta_id):
    artysta = get_object_or_404(Artysta, pk=artysta_id)
    initial_values = {
        "name": artysta.imie,
        "surname": artysta.nazwisko,
        "birth_date": artysta.data_urodzenia,
        "death_date": artysta.data_smierci
    }
    form = DetailedArtystaForm(initial=initial_values)
    return render(request, 'museum_app/detailed_artysta.html', {'form': form})


def detailed_dzielo(request):
    # for rzeźba pass -1 in width and height, for obraz pass -1 for weight and material
    initial_values = {
        "name": "Nazwa",
        "branch": "Oddział",
        "department": "Dział",
        "artist": "Artysta",
        "width": -1,
        "height": -1,
        "weight": 1000,
        "material": "Materiał"
    }
    form = DetailedDzieloForm(initial=initial_values)
    return render(request, 'museum_app/detailed_dzielo.html', {'form': form})

