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
            path('add/wydarzenie', views.add_wydarzenie, name='add_wydarzenie'),
            path('edit/oddzial', views.edit_oddzial, name='edit_oddzial'),
            path('edit/dzial', views.edit_dzial, name='edit_dzial'),
            path('edit/obraz', views.edit_obraz, name='edit_obraz'),
            path('edit/rzezba', views.edit_rzezba, name='edit_rzezba'),
            path('edit/artysta', views.edit_artysta, name='edit_artysta'),
            path('edit/bilet', views.edit_bilet, name='edit_bilet'),
            path('edit/rodzaj_biletu', views.edit_rodzaj_biletu, name='edit_rodzaj_biletu'),
            path('edit/pracownik', views.edit_pracownik, name='edit_pracownik'),
            path('edit/harmonogram_zwiedzania', views.edit_harmonogram_zwiedzania, name='edit_harmonogram_zwiedzania'),
            path('edit/wydarzenie', views.edit_wydarzenie, name='edit_wydarzenie'),
            path('detailed/<str:oddzial_nazwa>/oddzial', views.detailed_oddzial, name='detailed_oddzial'),
            path('detailed/dzial', views.detailed_dzial, name='detailed_dzial'),
            path('detailed/artysta', views.detailed_artysta, name='detailed_artysta'),
            path('detailed/dzielo', views.detailed_dzielo, name='detailed_dzielo')
            ]
