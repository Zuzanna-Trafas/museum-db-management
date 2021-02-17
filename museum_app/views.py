from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db import connection
from museum_app.forms import OddzialForm, DzialForm, ObrazForm, RzezbaForm, ArtystaForm, BiletForm, RodzajBiletuForm, \
    PracownikForm, HarmonogramZwiedzaniaForm, WydarzenieForm, DetailedArtystaForm, DetailedDzialForm, DetailedDzieloForm, DetailedOddzialForm
from museum_app.models import Oddzial, Wydarzenie, Wydarzenie_oddzial, Rodzaj_biletu, Pracownik, Harmonogram_zwiedzania, Bilet, Dzial, Artysta, Obraz, Rzezba

def main(request):
    # TODO searching
    return render(request, 'museum_app/main.html')


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


def detailed_dzial(request):
    initial_values = {
        "name": "Nazwa",
        "oddzial": "Oddzial",
        "floor": 1,
        "epoch": "Epoka"
    }
    form = DetailedDzialForm(initial=initial_values)
    return render(request, 'museum_app/detailed_dzial.html', {'form': form})


def detailed_artysta(request):
    initial_values = {
        "name": "Imię",
        "surname": "Nazwisko",
        "birth_date": "01/01/2000",
        "death_date": "01/01/2020"
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
