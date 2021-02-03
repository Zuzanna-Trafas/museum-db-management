from django.http import HttpResponse
from django.shortcuts import render


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
    return render(request, 'museum_app/add_oddzial.html')


def add_dzial(request):
    return render(request, 'museum_app/add_dzial.html')


def add_obraz(request):
    return render(request, 'museum_app/add_obraz.html')


def add_rzezba(request):
    return render(request, 'museum_app/add_rzezba.html')


def add_artysta(request):
    return render(request, 'museum_app/add_artysta.html')


def add_bilet(request):
    return render(request, 'museum_app/add_bilet.html')


def add_rodzaj_biletu(request):
    return render(request, 'museum_app/add_rodzaj_biletu.html')


def add_pracownik(request):
    return render(request, 'museum_app/add_pracownik.html')


def add_harmonogram_zwiedzania(request):
    return render(request, 'museum_app/add_harmonogram_zwiedzania.html')
