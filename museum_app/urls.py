from django.urls import path

from . import views

urlpatterns = [
            path('main/', views.main, name='main'),
            path('table/oddzialy/', views.oddzialy, name='oddzialy'),
            path('table/dzialy/', views.dzialy, name='dzialy'),
            path('table/dziela/', views.dziela, name='dziela'),
            path('table/artysci/', views.artysci, name='artysci'),
            path('table/bilety/', views.bilety, name='bilety'),
            path('table/pracownicy/', views.pracownicy, name='pracownicy'),
            path('table/harmonogram_zwiedzania/', views.harmonogram_zwiedzania, name='harmonogram_zwiedzania'),
            path('add/oddzial', views.add_oddzial, name='add_oddzial'),
            path('add/dzial', views.add_dzial, name='add_dzial'),
            path('add/obraz', views.add_obraz, name='add_obraz'),
            path('add/rzezba', views.add_rzezba, name='add_rzezba'),
            path('add/artysta', views.add_artysta, name='add_artysta'),
            path('add/bilet', views.add_bilet, name='add_bilet'),
            path('add/rodzaj_biletu', views.add_rodzaj_biletu, name='add_rodzaj_biletu'),
            path('add/pracownik', views.add_pracownik, name='add_pracownik'),
            path('add/harmonogram_zwiedzania', views.add_harmonogram_zwiedzania, name='add_harmonogram_zwiedzania'),
            ]
