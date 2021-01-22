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

def rodzaje_biletow(request):
        return render(request, 'museum_app/rodzaje_biletow.html')

def bilety(request):
        return render(request, 'museum_app/bilety.html')

def pracownicy(request):
        return render(request, 'museum_app/pracownicy.html')

def harmonogram_zwiedzania(request):
        return render(request, 'museum_app/harmonogram_zwiedzania.html')

def add(request):
        return render(request, 'museum_app/add.html')

def edit(request):
        return render(request, 'museum_app/edit.html')
