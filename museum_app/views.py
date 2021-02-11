from django.http import HttpResponse
from django.shortcuts import render
from museum_app.forms import OddzialForm, DzialForm, ObrazForm, RzezbaForm, ArtystaForm, BiletForm, RodzajBiletuForm, \
    PracownikForm, HarmonogramZwiedzaniaForm, DetailedArtystaForm


def main(request):
    return render(request, 'museum_app/main.html')


def oddzialy(request):
    return render(request, 'museum_app/oddzialy.html')


def dzialy(request):
    return render(request, 'museum_app/dzialy.html')


def dziela(request):
    return render(request, 'museum_app/dziela.html')


def artysci(request):
    return render(request, 'museum_app/artysci.html')


def bilety(request):
    return render(request, 'museum_app/bilety.html')


def pracownicy(request):
    return render(request, 'museum_app/pracownicy.html')


def harmonogram_zwiedzania(request):
    return render(request, 'museum_app/harmonogram_zwiedzania.html')


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
    form = ObrazForm(request.POST)
    return render(request, 'museum_app/add_obraz.html', {'form': form})


def add_rzezba(request):
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


def edit_oddzial(request):
    form = OddzialForm(request.POST)
    return render(request, 'museum_app/add_oddzial.html', {'form': form})


def edit_dzial(request):
    form = DzialForm(request.POST)
    return render(request, 'museum_app/add_dzial.html', {'form': form})


def edit_obraz(request):
    form = ObrazForm(request.POST)
    return render(request, 'museum_app/add_obraz.html', {'form': form})


def edit_rzezba(request):
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


def detailed_oddzial(request):
    form = OddzialForm(request.POST)
    return render(request, 'museum_app/add_oddzial.html', {'form': form})


def detailed_dzial(request):
    form = DzialForm(request.POST)
    return render(request, 'museum_app/add_dzial.html', {'form': form})


def detailed_obraz(request):
    form = ObrazForm(request.POST)
    return render(request, 'museum_app/add_obraz.html', {'form': form})


def detailed_rzezba(request):
    form = RzezbaForm(request.POST)
    return render(request, 'museum_app/add_rzezba.html', {'form': form})


def detailed_artysta(request):
    initial_values = {
        "name": "Imię",
        "surname": "Nazwisko",
        "birth_date": "01/01/2000",
        "death_date": "01/01/2020"
    }
    form = DetailedArtystaForm(initial=initial_values)
    return render(request, 'museum_app/detailed_artysta.html', {'form': form})


def detailed_bilet(request):
    form = BiletForm(request.POST)
    return render(request, 'museum_app/add_bilet.html', {'form': form})


def detailed_rodzaj_biletu(request):
    form = RodzajBiletuForm(request.POST)
    return render(request, 'museum_app/add_rodzaj_biletu.html', {'form': form})


def detailed_pracownik(request):
    form = PracownikForm(request.POST)
    return render(request, 'museum_app/add_pracownik.html', {'form': form})


def detailed_harmonogram_zwiedzania(request):
    form = HarmonogramZwiedzaniaForm(request.POST)
    return render(request, 'museum_app/add_harmonogram_zwiedzania.html', {'form': form})
