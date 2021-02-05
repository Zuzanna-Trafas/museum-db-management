from django.http import HttpResponse
from django.shortcuts import render
from .forms import OddzialForm


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
    return render(request, 'museum_app/add_dzial.html', {'form': form})


def add_obraz(request):
    return render(request, 'museum_app/add_obraz.html', {'form': form})


def add_rzezba(request):
    return render(request, 'museum_app/add_rzezba.html', {'form': form})


def add_artysta(request):
    return render(request, 'museum_app/add_artysta.html', {'form': form})


def add_bilet(request):
    return render(request, 'museum_app/add_bilet.html', {'form': form})


def add_rodzaj_biletu(request):
    return render(request, 'museum_app/add_rodzaj_biletu.html', {'form': form})


def add_pracownik(request):
    return render(request, 'museum_app/add_pracownik.html', {'form': form})


def add_harmonogram_zwiedzania(request):
    return render(request, 'museum_app/add_harmonogram_zwiedzania.html', {'form': form})
