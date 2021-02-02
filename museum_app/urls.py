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
            path('add/', views.add, name='add'),
            path('edit/', views.edit, name='edit'),
            ]
