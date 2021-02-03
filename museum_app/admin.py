from django.contrib import admin
from .models import Oddzial, Wydarzenie, Wydarzenie_oddzial, Rodzaj_biletu, Pracownik, Harmonogram_zwiedzania, Bilet, Dzial, Artysta, Obraz, Rzezba
# Register your models here.

class OddzialAdmin(admin.ModelAdmin):
        list_display = ['nazwa', 'godzina_otwarcia', 'godzina_zamkniecia', 'adres', 'numer_telefonu']

class WydarzenieAdmin(admin.ModelAdmin):
        list_display = ['nazwa', 'data_rozpoczecia', 'data_zakonczenia']

class Wydarzenie_oddzialAdmin(admin.ModelAdmin):
        list_display = ['oddzial_nazwa', 'wydarzenie_nazwa', 'wydarzenie_data_rozpoczecia']

class Rodzaj_biletuAdmin(admin.ModelAdmin):
        list_display = ['typ', 'czy_z_przewodnikiem', 'cena', 'oddzial_nazwa']

class PracownikAdmin(admin.ModelAdmin):
        list_display = ['pesel', 'imie', 'nazwisko', 'placa', 'etat', 'data_zatrudnienia', 'numer_telefonu', 'oddzial_nazwa']

class Harmonogram_zwiedzaniaAdmin(admin.ModelAdmin):
        list_display = ['id', 'godzina_rozpoczecia', 'data', 'pracownik_pesel']

class BiletAdmin(admin.ModelAdmin):
        list_display = ['id', 'data_zakupu', 'rodzaj_biletu_typ', 'rodzaj_biletu_oddzial_nazwa', 'rodzaj_biletu_czy_z_przewodnikiem', 'harmonogram_zwiedzania_id']

class DzialAdmin(admin.ModelAdmin):
        list_display = ['nazwa', 'pietro', 'epoka', 'oddzial_nazwa']

class ArtystaAdmin(admin.ModelAdmin):
        list_display = ['id', 'imie', 'nazwisko', 'data_urodzenia', 'data_smierci']

class ObrazAdmin(admin.ModelAdmin):
        list_display = ['id', 'nazwa', 'szerokosc', 'wysokosc', 'artysta_id', 'dzial_nazwa', 'dzial_oddzial_nazwa']

class RzezbaAdmin(admin.ModelAdmin):
        list_display = ['id', 'nazwa', 'waga', 'material', 'artysta_id', 'dzial_nazwa', 'dzial_oddzial_nazwa']


admin.site.register(Oddzial, OddzialAdmin)
admin.site.register(Wydarzenie, WydarzenieAdmin)
admin.site.register(Wydarzenie_oddzial, Wydarzenie_oddzialAdmin)
admin.site.register(Rodzaj_biletu, Rodzaj_biletuAdmin)
admin.site.register(Pracownik, PracownikAdmin)
admin.site.register(Harmonogram_zwiedzania, Harmonogram_zwiedzaniaAdmin)
admin.site.register(Bilet, BiletAdmin)
admin.site.register(Dzial, DzialAdmin)
admin.site.register(Artysta, ArtystaAdmin)
admin.site.register(Obraz, ObrazAdmin)
admin.site.register(Rzezba, RzezbaAdmin)
