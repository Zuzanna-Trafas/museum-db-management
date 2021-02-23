from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import FieldDoesNotExist
from django.core.exceptions import ValidationError
from django.http import Http404
from django.db import connection
from plotly.offline import plot
from plotly.graph_objs import Bar
import datetime
import unicodedata
from museum_app.forms import OddzialForm, DzialForm, ObrazForm, RzezbaForm, ArtystaForm, BiletForm, RodzajBiletuForm, \
    PracownikForm, HarmonogramZwiedzaniaForm, WydarzenieForm, DetailedArtystaForm, DetailedDzialForm, \
    DetailedDzieloForm, DetailedOddzialForm, TableOddzialForm, TableDzialForm, TableArtystaForm, TableBiletyForm, \
    TableHarmonogramZwiedzaniaForm, TableDzieloForm, TablePracownikForm, TableRodzajeBiletowForm, TableWydarzeniaForm, \
    MainForm
from museum_app.models import Oddzial, Wydarzenie, Wydarzenie_oddzial, Rodzaj_biletu, Pracownik, Harmonogram_zwiedzania, \
    Bilet, Dzial, Artysta, Obraz, Rzezba
import sys
import json


# TODO walidacja pól unique
def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')


def number_validator(number):
    if len(number) == 0:
        return ""
    number = number.strip().replace(" ", "").replace("-", "")

    if number[0] == "+" and len(number) == 12 and number[1:].isdecimal():
        return number
    elif len(number) == 9 and number.isdecimal():
        return number
    else:
        return -1


def get_profit(cursor, typ, czy_z_przewodnikiem, oddzial):
    cursor.execute("SELECT policz_dochod(%s, %s, %s)", [typ, czy_z_przewodnikiem, oddzial])
    return cursor.fetchone()[0]


def main(request):
    form = MainForm(request.POST)

    cursor = connection.cursor()
    cursor.execute("SET NAMES 'utf8mb3';")  # or utf8 or any other charset you want to handle

    cursor.execute("SET CHARACTER SET 'utf8mb3';")  # same as above

    cursor.execute("SET character_set_connection='utf8mb3';")  # same as above

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

    plot_div = plot([Bar(x=x, y=y, marker=dict(color='rgb( 255, 223, 65 )'))], output_type='div')
    cursor.close()

    # TODO searching
    kolumny = {"Oddział": ["Nazwa", "Godzina otwarcia", "Godzina zamknięcia", "Adres", "Numer telefonu"],
               "Wydarzenie": ["Nazwa", "Data rozpoczęcia", "Data zakończenia"],
               "Dział": ["Nazwa", "Piętro", "Epoka", "Nazwa oddziału"],
               "Dzieło": ["Nazwa", "Artysta", "Dział"],
               "Artysta": ["Imię", "Nazwisko", "Data urodzenia", "Data śmierci"],
               "Rodzaj biletu": ["Typ", "Czy z przewodnikiem", "Cena", "Oddział"],
               "Bilet": ["Data zakupu", "Typ biletu", "Cena", "Czy z przewodnikiem"],
               "Pracownik": ["Pesel", "Imię", "Nazwisko", "Płaca", "Etat", "Data zatrudnienia", "Numer telefonu",
                             "Oddział"],
               "Wycieczka": ["Godzina rozpoczęcia", "Data", "Pesel przewodnika"]}

    wyniki = []
    if form.is_valid():
        options1 = form.cleaned_data['options1']
        options2 = form.cleaned_data['options2']
        options3 = form.cleaned_data['options3']
        options4 = form.cleaned_data['options4']
        if options1 == "Oddział":
            if options2 == "Nazwa":
                for i in Oddzial.objects.values():
                    if i["nazwa"] == options4:
                        wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
            elif options2 == "Godzina otwarcia":
                if options3 == "Później niż":
                    for i in Oddzial.objects.values():
                        if str(i["godzina_otwarcia"])[:-3] > str(options4):
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
                elif options3 == "Wcześniej niż":
                    for i in Oddzial.objects.values():
                        if str(i["godzina_otwarcia"])[:-3] < str(options4):
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
                elif options3 == "Równa":
                    for i in Oddzial.objects.values():
                        if str(i["godzina_otwarcia"])[:-3] == str(options4):
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
            elif options2 == "Godzina zamknięcia":
                if options3 == "Później niż":
                    for i in Oddzial.objects.values():
                        print(options4, file=sys.stderr)
                        if str(i["godzina_zamkniecia"])[:-3] > str(options4):
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
                elif options3 == "Wcześniej niż":
                    for i in Oddzial.objects.values():
                        if str(i["godzina_zamkniecia"])[:-3] < str(options4):
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
                elif options3 == "Równa":
                    for i in Oddzial.objects.values():
                        if str(i["godzina_zamkniecia"])[:-3] == str(options4):
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
        elif options1 == "Wydarzenie":
            if options2 == "Nazwa":
                for i in Wydarzenie.objects.values():
                    if i["nazwa"] == options4:
                        print(i.values(), file=sys.stderr)
                        wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Oddział":
                for i in Wydarzenie.objects.values():
                    for j in Wydarzenie_oddzial.objects.values():
                        if j["oddzial_nazwa_id"] == options4 and j["wydarzenie_id_id"] == i["id"]:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Data rozpoczęcia":
                if options3 == "Później niż":
                    for i in Wydarzenie.objects.values():
                        if str(i["data_rozpoczecia"]) >= options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "Wcześniej niż":
                    for i in Wydarzenie.objects.values():
                        if str(i["data_rozpoczecia"]) <= options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "Równa":
                    for i in Wydarzenie.objects.values():
                        if str(i["data_rozpoczecia"]) == options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Data zakończenia":
                if options3 == "Później niż":
                    for i in Wydarzenie.objects.values():
                        if str(i["data_zakonczenia"]) >= options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "Wcześniej niż":
                    for i in Wydarzenie.objects.values():
                        if str(i["data_zakonczenia"]) <= options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "Równa":
                    for i in Wydarzenie.objects.values():
                        if str(i["data_zakonczenia"]) == options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
        elif options1 == "Dział":
            if options2 == "Nazwa":
                for i in Dzial.objects.values():
                    if i["nazwa"] == options4:
                        wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
            elif options2 == "Epoka":
                for i in Dzial.objects.values():
                    if i["epoka"] == options4:
                        wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
            elif options2 == "Oddział":
                for i in Dzial.objects.values():
                    if i["oddzial_nazwa_id"] == options4:
                        wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
        elif options1 == "Dzieło":
            if options2 == "Nazwa":
                for i in Obraz.objects.values():
                    if i["nazwa"] == options4:
                        try:
                            wyniki.append(
                                [i['nazwa'], [x.imie for x in Artysta.objects.all() if x.id == i['artysta_id_id']][0]
                                 + " " + [x.nazwisko for x in Artysta.objects.all() if x.id == i['artysta_id_id']][0],
                                 [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
                        except:
                            wyniki.append(
                                [i['nazwa'], "Anonimowy",
                                 [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
                        print(wyniki, file=sys.stderr)
                for i in Rzezba.objects.values():
                    if i["nazwa"] == options4:
                        try:
                            wyniki.append(
                                [i['nazwa'], [x.imie for x in Artysta.objects.all() if x.id == i['artysta_id_id']][0]
                                 + " " + [x.nazwisko for x in Artysta.objects.all() if x.id == i['artysta_id_id']][0],
                                 [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
                        except:
                            wyniki.append(
                                [i['nazwa'], "Anonimowy",
                                 [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
            elif options2 == "Epoka":
                for j in Dzial.objects.values():
                    for i in Obraz.objects.values():
                        if j["epoka"] == options4 and i["dzial_id_id"] == j["id"]:
                            print("test", file=sys.stderr)
                            try:
                                wyniki.append([i['nazwa'],
                                               [x.imie for x in Artysta.objects.all() if x.id == i['artysta_id_id']][0]
                                               + " " + [x.nazwisko for x in Artysta.objects.all() if
                                                        x.id == i['artysta_id_id']][0],
                                               [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
                            except:
                                wyniki.append(
                                    [i['nazwa'], "Anonimowy",
                                     [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
                    for i in Rzezba.objects.values():
                        if j["epoka"] == options4 and i["dzial_id_id"] == j["id"]:
                            try:
                                wyniki.append([i['nazwa'],
                                               [x.imie for x in Artysta.objects.all() if x.id == i['artysta_id_id']][0]
                                               + " " + [x.nazwisko for x in Artysta.objects.all() if
                                                        x.id == i['artysta_id_id']][0],
                                               [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
                            except:
                                wyniki.append(
                                    [i['nazwa'], "Anonimowy",
                                     [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
            else:
                for j in Artysta.objects.values():
                    for i in Obraz.objects.values():
                        if i["artysta_id_id"] == j["id"] and j["nazwisko"] == options4:
                            try:
                                wyniki.append([i['nazwa'],
                                               [x.imie for x in Artysta.objects.all() if x.id == i['artysta_id_id']][0]
                                               + " " + [x.nazwisko for x in Artysta.objects.all() if
                                                        x.id == i['artysta_id_id']][0],
                                               [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
                            except:
                                wyniki.append(
                                    [i['nazwa'], "Anonimowy",
                                     [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
                    for i in Rzezba.objects.values():
                        if i["artysta_id_id"] == j["id"] and j["nazwisko"] == options4:
                            try:
                                wyniki.append([i['nazwa'],
                                               [x.imie for x in Artysta.objects.all() if x.id == i['artysta_id_id']][0]
                                               + " " + [x.nazwisko for x in Artysta.objects.all() if
                                                        x.id == i['artysta_id_id']][0],
                                               [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
                            except:
                                wyniki.append(
                                    [i['nazwa'], "Anonimowy",
                                     [x.nazwa for x in Dzial.objects.all() if x.id == i['dzial_id_id']][0]])
        elif options1 == "Artysta":
            if options2 == "Imię":
                for i in Artysta.objects.values():
                    if i["imie"] == options4:
                        wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Nazwisko":
                for i in Artysta.objects.values():
                    if i["nazwisko"] == options4:
                        wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Data urodzenia":
                if options3 == "Później niż":
                    for i in Artysta.objects.values():
                        if str(i["data_urodzenia"]) > options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "Wcześniej niż":
                    for i in Artysta.objects.values():
                        if str(i["data_urodzenia"]) < options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "Równa":
                    for i in Artysta.objects.values():
                        if str(i["data_urodzenia"]) == options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Data śmierci":
                if options3 == "Później niż":
                    for i in Artysta.objects.values():
                        if str(i["data_smierci"]) > options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "Wcześniej niż":
                    for i in Artysta.objects.values():
                        if str(i["data_smierci"]) < options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "Równa":
                    for i in Artysta.objects.values():
                        if str(i["data_smierci"]) == options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
        elif options1 == "Rodzaj biletu":
            if options2 == "Typ":
                for i in Rodzaj_biletu.objects.values():
                    if i["typ"] == options4:
                        wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Cena":
                if options3 == "<":
                    for i in Rodzaj_biletu.objects.values():
                        if i["cena"] < int(options4):
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "<=":
                    for i in Rodzaj_biletu.objects.values():
                        if i["cena"] <= int(options4):
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "=":
                    for i in Rodzaj_biletu.objects.values():
                        if i["cena"] == int(options4):
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == ">=":
                    for i in Rodzaj_biletu.objects.values():
                        if i["cena"] >= int(options4):
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == ">":
                    for i in Rodzaj_biletu.objects.values():
                        if i["cena"] > int(options4):
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
        elif options1 == "Bilet":
            if options2 == "Data zakupu":
                if options3 == "Później niż":
                    for i in Bilet.objects.values():
                        if str(i["data_zakupu"]) > options4:
                            wyniki.append([i['data_zakupu'],
                                           [x.typ for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0],
                                           [x.cena for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0],
                                           [x.czy_z_przewodnikiem for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0]])
                elif options3 == "Wcześniej niż":
                    for i in Bilet.objects.values():
                        if str(i["data_zakupu"]) < options4:
                            wyniki.append([i['data_zakupu'],
                                           [x.typ for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0],
                                           [x.cena for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0],
                                           [x.czy_z_przewodnikiem for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0]])
                elif options3 == "Równa":
                    for i in Bilet.objects.values():
                        if str(i["data_zakupu"]) == options4:
                            wyniki.append([i['data_zakupu'],
                                           [x.typ for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0],
                                           [x.cena for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0],
                                           [x.czy_z_przewodnikiem for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0]])
            elif options2 == "Typ":
                for i in Bilet.objects.values():
                    for j in Rodzaj_biletu.objects.values():
                        if j["typ"] == options4 and i["rodzaj_biletu_id_id"] == j["id"]:
                            wyniki.append([i['data_zakupu'],
                                           [x.typ for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0],
                                           [x.cena for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0],
                                           [x.czy_z_przewodnikiem for x in Rodzaj_biletu.objects.all() if
                                            x.id == i['rodzaj_biletu_id_id']][0]])
        elif options1 == "Pracownik":
            if options2 == "Imię":
                for i in Pracownik.objects.values():
                    if i["imie"] == options4:
                        wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Nazwisko":
                for i in Pracownik.objects.values():
                    if i["nazwisko"] == options4:
                        wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Pesel":
                for i in Pracownik.objects.values():
                    if str(i["pesel"]) == str(options4):
                        wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Etat":
                for i in Pracownik.objects.values():
                    if i["etat"] == options4:
                        wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Płaca":
                if options3 == "<":
                    for i in Pracownik.objects.values():
                        if i["placa"] < int(options4):
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "<=":
                    for i in Pracownik.objects.values():
                        if i["placa"] <= int(options4):
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "=":
                    for i in Pracownik.objects.values():
                        if i["placa"] == int(options4):
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == ">=":
                    for i in Pracownik.objects.values():
                        if i["placa"] >= int(options4):
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == ">":
                    for i in Pracownik.objects.values():
                        if i["placa"] > int(options4):
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
            elif options2 == "Data zatrudnienia":
                if options3 == "Później niż":
                    for i in Pracownik.objects.values():
                        if str(i["data_zatrudnienia"]) > options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "Wcześniej niż":
                    for i in Pracownik.objects.values():
                        if str(i["data_zatrudnienia"]) < options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])
                elif options3 == "Równa":
                    for i in Pracownik.objects.values():
                        if str(i["data_zatrudnienia"]) == options4:
                            wyniki.append([i[x] for x in i.keys() if x != 'id'])

        elif options1 == "Wycieczka":
            if options2 == "Data":
                if options3 == "Później niż":
                    for i in Harmonogram_zwiedzania.objects.values():
                        if str(i["data"]) > options4:
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
                elif options3 == "Wcześniej niż":
                    for i in Harmonogram_zwiedzania.objects.values():
                        if str(i["data"]) < options4:
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
                elif options3 == "Równa":
                    for i in Harmonogram_zwiedzania.objects.values():
                        if str(i["data"]) == options4:
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
            elif options2 == "Godzina rozpoczęcia":
                if options3 == "Później niż":
                    for i in Harmonogram_zwiedzania.objects.values():
                        if str(i["godzina_rozpoczecia"])[:-3] > str(options4):
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
                elif options3 == "Wcześniej niż":
                    for i in Harmonogram_zwiedzania.objects.values():
                        if str(i["godzina_rozpoczecia"])[:-3] < str(options4):
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
                elif options3 == "Równa":
                    for i in Harmonogram_zwiedzania.objects.values():
                        if str(i["godzina_rozpoczecia"])[:-3] == str(options4):
                            wyniki.append([str(i[x]) for x in i.keys() if x != 'id'])
            else:
                for i in Pracownik.objects.values():
                    for j in Harmonogram_zwiedzania.objects.values():
                        if i["nazwisko"] == options4 and str(j["pracownik_pesel_id"]) == str(i["pesel"]):
                            wyniki.append([str(j[x]) for x in j.keys() if x != 'id'])

        """        
        for model in modele[options1]:
            for j in model.objects.values():
                print(j, file=sys.stderr)
                if options2 in keys.keys():
                    if j[keys[options2]] == options4:
                        tmp.append(j)
                elif j[strip_accents(options2.lower().replace(" ", "_").replace("ł", "l"))] == options4:
                    tmp.append(j)
        for i in tmp:
            wyniki.append([i[x] for x in i.keys() if x != 'id'])
        """

        print(wyniki, file=sys.stderr)
        return render(request, 'museum_app/main.html',
                      context={'form': form, 'plot_div': plot_div, 'kolumny': kolumny[options1], 'wyniki': wyniki})

    # TODO jaki format wyników tho = for (obiektow) a w nim for (atrybutow)
    return render(request, 'museum_app/main.html',
                  context={'form': form, 'plot_div': plot_div, 'kolumny': [], 'wyniki': []})


def oddzialy(request):
    form = TableOddzialForm(request.POST)
    error = ""
    if request.method == 'POST' and form.is_valid():
        if 'delete' in request.POST:
            for item in form.cleaned_data['choices']:
                try:
                    item.delete()
                except Exception as e:
                    error = "Nie można usunąć, gdyż oddział jest powiązany z "
                    if "Dzial" in e.args[0]:
                        error += "działami"
                    elif "Pracownik" in e.args[0]:
                        error += "pracownikami"
                    elif "Rodzaj_biletu" in e.args[0]:
                        error += "rodzajami biletów"
                    elif "Wydarzenie_oddzial" in e.args[0]:
                        error += "wydarzeniami"

    oddzialy = Oddzial.objects.all()
    context = {'oddzialy': oddzialy, 'error': error}
    return render(request, 'museum_app/oddzialy.html', context)


def dzialy(request):
    form = TableDzialForm(request.POST)
    error = ""
    if request.method == 'POST' and form.is_valid():
        if 'delete' in request.POST:
            for item in form.cleaned_data['choices']:
                try:
                    item.delete()
                except Exception as e:
                    error = "Nie można usunąć"
                    if "Rzezba" in e.args[0] or "Obraz" in e.args[0]:
                        error = "Nie można usunąć, gdyż dział jest powiązany z dziełami"
    dzialy = Dzial.objects.all()
    oddzialy = Oddzial.objects.all()
    context = {'dzialy': dzialy, 'oddzialy': oddzialy, 'error': error}
    return render(request, 'museum_app/dzialy.html', context)


def dziela(request):
    form = TableDzieloForm(request.POST)
    error = ""
    if request.method == 'POST' and form.is_valid():
        if 'delete' in request.POST:
            for item in form.cleaned_data['choices_obrazy']:
                try:
                    item.delete()
                except Exception as e:
                    error = "Nie można usunąć dzieła"

            for item in form.cleaned_data['choices_rzezby']:
                try:
                    item.delete()
                except Exception as e:
                    error = "Nie można usunąć dzieła"

    obrazy = Obraz.objects.all()
    rzezby = Rzezba.objects.all()
    context = {'obrazy': obrazy, 'rzezby': rzezby, 'error': error}
    return render(request, 'museum_app/dziela.html', context)


def artysci(request):
    form = TableArtystaForm(request.POST)
    error = ""
    if request.method == 'POST' and form.is_valid():
        if 'delete' in request.POST:
            for item in form.cleaned_data['choices']:
                try:
                    item.delete()
                except Exception as e:
                    error = "Nie można usunąć"
                    if "Rzezba" in e.args[0] or "Obraz" in e.args[0]:
                        error = "Nie można usunąć, gdyż artysta jest powiązany z dziełami"

    artysci = Artysta.objects.all()
    context = {'artysci': artysci, 'error': error}
    return render(request, 'museum_app/artysci.html', context)


def bilety(request):
    form = TableBiletyForm(request.POST)
    error = ""
    if request.method == 'POST' and form.is_valid():
        if 'delete' in request.POST:
            for item in form.cleaned_data['choices']:
                try:
                    item.delete()
                except Exception as e:
                    error = "Nie można usunąć"

    bilety = Bilet.objects.all()
    rodzaje_biletow = Rodzaj_biletu.objects.all()
    context = {'bilety': bilety, 'rodzaje_biletow': rodzaje_biletow, 'error': error}
    return render(request, 'museum_app/bilety.html', context)


def pracownicy(request):
    form = TablePracownikForm(request.POST)
    error = ""
    if request.method == 'POST' and form.is_valid():
        if 'delete' in request.POST:
            for item in form.cleaned_data['choices']:
                try:
                    item.delete()
                except Exception as e:
                    error = "Nie można usunąć"
                    if "Harmonogram_zwiedzania" in e.args[0]:
                        error = "Nie można usunąć, gdyż pracownik jest powiązany z wycieczką"

    pracownicy = Pracownik.objects.all()
    context = {'pracownicy': pracownicy, 'error': error}
    return render(request, 'museum_app/pracownicy.html', context)


def harmonogram_zwiedzania(request):
    form = TableHarmonogramZwiedzaniaForm(request.POST)
    error = ""
    if request.method == 'POST' and form.is_valid():
        if 'delete' in request.POST:
            for item in form.cleaned_data['choices']:
                try:
                    item.delete()
                except Exception as e:
                    error = "Nie można usunąć"

    harmonogram_zwiedzania = Harmonogram_zwiedzania.objects.all()
    cursor = connection.cursor()
    cursor.execute('CALL podsumowanie_zwiedzania()')
    podsumowanie = cursor.fetchall()
    cursor.close()
    context = {'podsumowanie': podsumowanie, 'harmonogram_zwiedzania': harmonogram_zwiedzania, 'error': error}
    return render(request, 'museum_app/harmonogram_zwiedzania.html', context)


def rodzaje_biletow(request):
    form = TableRodzajeBiletowForm(request.POST)
    error = ""
    if request.method == 'POST' and form.is_valid():
        if 'delete' in request.POST:
            for item in form.cleaned_data['choices']:
                try:
                    item.delete()
                except Exception as e:
                    error = "Nie można usunąć"
                    if "Bilet" in e.args[0]:
                        error = "Nie można usunąć, gdyż rodzaj biletu jest powiązany z biletami"

    rodzaje_biletow = Rodzaj_biletu.objects.all()

    context = {'rodzaje_biletow': rodzaje_biletow, 'error': error}
    return render(request, 'museum_app/rodzaje_biletow.html', context)


def add_oddzial(request):
    form = OddzialForm(request.POST)
    error = ""
    error_time = ""
    error_number = ""
    if form.is_valid():
        name = form.cleaned_data['name']
        opening_hour = form.cleaned_data['opening_hour']
        closing_hour = form.cleaned_data['closing_hour']
        address = form.cleaned_data['address']
        number = form.cleaned_data['number']

        if opening_hour > closing_hour:
            error_time = "Godzina otwarcia musi być przed godziną zamknięcia!"
            return render(request, 'museum_app/add_oddzial.html',
                          {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error,
                           'tag': "Dodaj"})

        validator = number_validator(number)
        if validator == -1:
            error_number = "Niepoprawny numer telefonu."
            return render(request, 'museum_app/add_oddzial.html',
                          {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error,
                           'tag': "Dodaj"})
        else:
            number = validator
        try:
            Oddzial.objects.create(nazwa=name, godzina_otwarcia=opening_hour, godzina_zamkniecia=closing_hour,
                                   adres=address, numer_telefonu=number)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args[1]:
                error = "Ta nazwa oddziału już istnieje."
            return render(request, 'museum_app/add_oddzial.html',
                          {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error,
                           'tag': "Dodaj"})

        else:
            return redirect('/table/oddzialy')

    return render(request, 'museum_app/add_oddzial.html',
                  {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error,
                   'tag': "Dodaj"})


def add_dzial(request):
    error = ""
    form = DzialForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        floor = form.cleaned_data['floor']
        epoch = form.cleaned_data['epoch']
        oddzial_select = form.cleaned_data['oddzial_select']
        for x in Oddzial.objects.all():
            if str(x.nazwa) == str(oddzial_select):
                oddzial = x
        try:
            Dzial.objects.create(nazwa=name, pietro=floor, epoka=epoch,
                                 oddzial_nazwa=oddzial)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args[1]:
                error = "Dział o tej nazwie już istnieje na wybranym oddziale."
            return render(request, 'museum_app/add_dzial.html',
                          {'form': form, 'error': error, 'tag': "Dodaj"})
        else:
            return redirect('/table/dzialy')
    return render(request, 'museum_app/add_dzial.html', {'form': form, 'error': error, 'tag': "Dodaj"})


def add_obraz(request):
    artysta_choices = [("-", "-")]
    for x in Artysta.objects.all():
        artysta_choices.append((x.id, x.imie + " " + x.nazwisko))
    form = ObrazForm(
        [(str(x.nazwa) + " ; " + str(x.oddzial_nazwa.nazwa), str(x.nazwa) + ", " + str(x.oddzial_nazwa.nazwa)) for x in
         Dzial.objects.all()],
        artysta_choices,
        request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        width = form.cleaned_data['width']
        height = form.cleaned_data['height']
        dzial_select = form.cleaned_data['dzial_select'].split(" ; ")
        artysta_select = form.cleaned_data['artysta_select']
        if artysta_select == "-":
            artysta_select = None

        dzial_id = None
        for x in Dzial.objects.all():
            if x.nazwa == dzial_select[0] and x.oddzial_nazwa.nazwa == dzial_select[1]:
                dzial_id = x

        artysta_id = None
        for x in Artysta.objects.all():
            if str(x.id) == artysta_select:
                artysta_id = x

        Obraz.objects.create(nazwa=name, szerokosc=width, wysokosc=height, dzial_id=dzial_id, artysta_id=artysta_id)
        return redirect('/table/dziela')

    return render(request, 'museum_app/add_obraz.html', {'form': form, 'tag': "Dodaj"})


def add_rzezba(request):
    artysta_choices = [("-", "-")]
    for x in Artysta.objects.all():
        artysta_choices.append((x.id, x.imie + " " + x.nazwisko))
    form = RzezbaForm(
        [(str(x.nazwa) + " ; " + str(x.oddzial_nazwa.nazwa), str(x.nazwa) + ", " + str(x.oddzial_nazwa.nazwa)) for x in
         Dzial.objects.all()],
        artysta_choices,
        request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        weight = form.cleaned_data['weight']
        material = form.cleaned_data['material']
        dzial_select = form.cleaned_data['dzial_select'].split(" ; ")
        artysta_select = form.cleaned_data['artysta_select']
        if artysta_select == "-":
            artysta_select = None

        dzial_id = None
        for x in Dzial.objects.all():
            if x.nazwa == dzial_select[0] and x.oddzial_nazwa.nazwa == dzial_select[1]:
                dzial_id = x

        artysta_id = None
        for x in Artysta.objects.all():
            if str(x.id) == artysta_select:
                artysta_id = x

        Rzezba.objects.create(nazwa=name, waga=weight, material=material, dzial_id=dzial_id, artysta_id=artysta_id)
        return redirect('/table/dziela')

    return render(request, 'museum_app/add_rzezba.html', {'form': form, 'tag': "Dodaj"})


def add_artysta(request):
    error = ""
    error_birth = ""
    error_death = ""
    form = ArtystaForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        surname = form.cleaned_data['surname']
        birth_date = form.cleaned_data['birth_date']
        death_date = form.cleaned_data['death_date']

        birth_year = birth_date.split("-")[0]

        if len(birth_year) > 4:
            error_birth = "Rok nie może być większy od 9999"
            return render(request, 'museum_app/add_artysta.html',
                          {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death,
                           'tag': "Dodaj"})
        if death_date != "":
            death_year = death_date.split("-")[0]
            if len(death_year) > 4:
                error_death = "Rok nie może być większy od 9999"
                return render(request, 'museum_app/add_artysta.html',
                              {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death,
                               'tag': "Dodaj"})
            if death_date < birth_date:
                error = "Data urodzenia musi być wcześniejsza niż data śmierci!"
                return render(request, 'museum_app/add_artysta.html',
                              {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death,
                               'tag': "Dodaj"})

        else:
            death_date = None
        Artysta.objects.create(imie=name, nazwisko=surname, data_urodzenia=birth_date, data_smierci=death_date)
        return redirect('/table/artysci')

    return render(request, 'museum_app/add_artysta.html',
                  {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death,
                   'tag': "Dodaj"})


def add_bilet(request):
    error = ""
    error_oddzial = ""
    error_data = ""
    typ = []
    is_przewodnik = []
    for x in Rodzaj_biletu.objects.all():
        if x.czy_z_przewodnikiem == 0:
            typ.append((x.id, str(x.typ) + " bez przewodnika, " + str(x.oddzial_nazwa.nazwa)))
            is_przewodnik.append((x.id, 0))
        else:
            typ.append((x.id, str(x.typ) + " z przewodnikiem, " + str(x.oddzial_nazwa.nazwa)))
            is_przewodnik.append((x.id, 1))
    json_przewodnik = json.dumps(is_przewodnik)
    form = BiletForm(typ, [
        (x.id, str(x.pracownik_pesel.oddzial_nazwa.nazwa) + ", " + str(x.data) + " " + str(x.godzina_rozpoczecia) +
         ", " + str(x.pracownik_pesel.imie) + " " + str(x.pracownik_pesel.nazwisko)) for x in
        Harmonogram_zwiedzania.objects.all()],
                     request.POST)
    if form.is_valid():
        purchase_date = form.cleaned_data['purchase_date']
        type = form.cleaned_data['type']
        wycieczka = form.cleaned_data['wycieczka']

        if len(purchase_date.split("-")[0]) > 4:
            error_data = "Rok nie może być większy niż 9999"
            return render(request, 'museum_app/add_bilet.html',
                          {'form': form, 'error': error, 'error_oddzial': error_oddzial, 'error_data': error_data,
                           'tag': "Dodaj", "json_przewodnik": json_przewodnik})

        rodzaj_biletu_id = None
        for x in Rodzaj_biletu.objects.all():
            if str(x.id) == str(type):
                rodzaj_biletu_id = x

        harmonogram = None
        for x in Harmonogram_zwiedzania.objects.all():
            if str(x.id) == str(wycieczka):
                harmonogram = x

        if harmonogram is not None:
            if harmonogram.pracownik_pesel.oddzial_nazwa.nazwa != rodzaj_biletu_id.oddzial_nazwa.nazwa:
                error_oddzial = "Ta wycieczka odbywa się na innym oddziale!"
                return render(request, 'museum_app/add_bilet.html',
                              {'form': form, 'error': error, 'error_oddzial': error_oddzial, 'error_data': error_data,
                               'tag': "Dodaj", "json_przewodnik": json_przewodnik})

        Bilet.objects.create(data_zakupu=purchase_date, rodzaj_biletu_id=rodzaj_biletu_id,
                             harmonogram_zwiedzania_id=harmonogram)

        return redirect('/table/bilety')

    return render(request, 'museum_app/add_bilet.html',
                  {'form': form, 'error': error, 'error_oddzial': error_oddzial, 'error_data': error_data,
                   'tag': "Dodaj", "json_przewodnik": json_przewodnik})


def add_rodzaj_biletu(request):
    error = ""
    form = RodzajBiletuForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], request.POST)
    if form.is_valid():
        przewodnik = form.cleaned_data['przewodnik']
        oddzial = form.cleaned_data['oddzial']
        type = form.cleaned_data['type']
        price = form.cleaned_data['price']
        for x in Oddzial.objects.all():
            if str(x.nazwa) == str(oddzial):
                oddzial = x
        if przewodnik == "tak":
            przewodnik = True
        else:
            przewodnik = False

        try:
            Rodzaj_biletu.objects.create(typ=type, czy_z_przewodnikiem=przewodnik, cena=price, oddzial_nazwa=oddzial)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args[1]:
                error = "Taki rodzaj bilet już istnieje."
            return render(request, 'museum_app/add_rodzaj_biletu.html', {'form': form, 'error': error, 'tag': "Dodaj"})

        return redirect('/table/rodzaje_biletow')

    return render(request, 'museum_app/add_rodzaj_biletu.html', {'form': form, 'error': error, 'tag': "Dodaj"})


def add_pracownik(request):
    error = ""
    error_number = ""
    error_date = ""
    form = PracownikForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], request.POST)
    if form.is_valid():
        pesel = form.cleaned_data['pesel']
        imie = form.cleaned_data['imie']
        nazwisko = form.cleaned_data['nazwisko']
        etat = form.cleaned_data['etat']
        placa = form.cleaned_data['placa']
        data_zatrudnienia = form.cleaned_data['data_zatrudnienia']
        oddzial = form.cleaned_data['oddzial']
        numer_telefonu = form.cleaned_data['numer_telefonu']

        if len(data_zatrudnienia.split("-")[0]) > 4:
            error_date = "Rok nie może być większy od 9999"
            return render(request, 'museum_app/add_pracownik.html',
                          {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date,
                           'tag': "Dodaj"})

        for x in Oddzial.objects.all():
            if str(x.nazwa) == str(oddzial):
                oddzial = x

        validator = number_validator(numer_telefonu)
        if validator == -1:
            error_number = "Niepoprawny numer telefonu."
            return render(request, 'museum_app/add_pracownik.html',
                          {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date,
                           'tag': "Dodaj"})
        else:
            numer_telefonu = validator

        try:
            Pracownik.objects.create(pesel=pesel, imie=imie, nazwisko=nazwisko, etat=etat, placa=placa,
                                     data_zatrudnienia=data_zatrudnienia, oddzial_nazwa=oddzial,
                                     numer_telefonu=numer_telefonu)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args[1]:
                error = "Pracownik o tym peselu już istnieje"
            return render(request, 'museum_app/add_pracownik.html',
                          {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date,
                           'tag': "Dodaj"})
        else:
            return redirect('/table/pracownicy')

    return render(request, 'museum_app/add_pracownik.html',
                  {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date,
                   'tag': "Dodaj"})


def add_harmonogram_zwiedzania(request):
    error_date = ""
    error = ""
    form = HarmonogramZwiedzaniaForm(
        [(x.pesel, x.imie + " " + x.nazwisko + " (" + str(x.pesel) + ")") for x in Pracownik.objects.all()],
        request.POST)
    if form.is_valid():
        godzina = form.cleaned_data['godzina']
        data = form.cleaned_data['data']
        pesel = form.cleaned_data['pesel']

        if len(data.split("-")[0]) > 4:
            error_date = "Rok nie może być większy od 9999"
            return render(request, 'museum_app/add_harmonogram_zwiedzania.html',
                          {'form': form, 'error': error, 'error_date': error_date, 'tag': "Dodaj"})

        for x in Pracownik.objects.all():
            if str(x.pesel) == str(pesel):
                pracownik = x

        try:
            Harmonogram_zwiedzania.objects.create(godzina_rozpoczecia=godzina, data=data, pracownik_pesel=pracownik)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args[1]:
                error = "Taki harmonogram zwiedzania już istnieje"
            return render(request, 'museum_app/add_harmonogram_zwiedzania.html',
                          {'form': form, 'error': error, 'error_date': error_date, 'tag': "Dodaj"})
        else:
            return redirect('/table/harmonogram_zwiedzania')

    return render(request, 'museum_app/add_harmonogram_zwiedzania.html',
                  {'form': form, 'error': error, 'error_date': error_date, 'tag': "Dodaj"})


def add_wydarzenie(request, oddzial_nazwa):
    error = ""
    error_data_rozpoczecia = ""
    error_data_zakonczenia = ""
    error_dates = ""
    form = WydarzenieForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], request.POST)
    if form.is_valid():
        nazwa = form.cleaned_data['nazwa']
        oddzialy_select = form.cleaned_data['oddzial_select']
        data_rozpoczecia = form.cleaned_data['data_rozpoczecia']
        data_zakonczenia = form.cleaned_data['data_zakonczenia']

        if len(data_rozpoczecia.split("-")[0]) > 4:
            error_data_rozpoczecia = "Rok nie może być większy od 9999"
            return render(request, 'museum_app/add_wydarzenie.html',
                          {'form': form, 'error': error, 'error_data_rozpoczecia': error_data_rozpoczecia,
                           'error_data_zakonczenia': error_data_zakonczenia, 'error_dates': error_dates,
                           'tag': "Dodaj"})

        if len(data_zakonczenia.split("-")[0]) > 4:
            error_data_zakonczenia = "Rok nie może być większy od 9999"
            return render(request, 'museum_app/add_wydarzenie.html',
                          {'form': form, 'error': error, 'error_data_rozpoczecia': error_data_rozpoczecia,
                           'error_data_zakonczenia': error_data_zakonczenia, 'error_dates': error_dates,
                           'tag': "Dodaj"})

        if data_rozpoczecia > data_zakonczenia:
            error_dates = "Data rozpoczęcia musi być przed datą zakończenia!"
            return render(request, 'museum_app/add_wydarzenie.html',
                          {'form': form, 'error': error, 'error_data_rozpoczecia': error_data_rozpoczecia,
                           'error_data_zakonczenia': error_data_zakonczenia, 'error_dates': error_dates,
                           'tag': "Dodaj"})

        oddzialy = []
        for x in Oddzial.objects.all():
            if str(x.nazwa) in oddzialy_select:
                oddzialy.append(x)

        try:
            wydarzenie = Wydarzenie.objects.create(nazwa=nazwa, data_rozpoczecia=data_rozpoczecia,
                                                   data_zakonczenia=data_zakonczenia)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args[1]:
                error = "Wydarzenie o takiej nazwie i dacie rozpoczęcia już istnieje"
            return render(request, 'museum_app/add_wydarzenie.html',
                          {'form': form, 'error': error, 'error_data_rozpoczecia': error_data_rozpoczecia,
                           'error_data_zakonczenia': error_data_zakonczenia, 'error_dates': error_dates,
                           'tag': "Dodaj"})

        for oddzial in oddzialy:
            Wydarzenie_oddzial.objects.create(oddzial_nazwa=oddzial, wydarzenie_id=wydarzenie)

        return redirect('/detailed/' + str(oddzial_nazwa) + '/oddzial')

    return render(request, 'museum_app/add_wydarzenie.html',
                  {'form': form, 'error': error, 'error_data_rozpoczecia': error_data_rozpoczecia,
                   'error_data_zakonczenia': error_data_zakonczenia, 'error_dates': error_dates, 'tag': "Dodaj"})


def edit_oddzial(request, oddzial_nazwa):
    oddzial = get_object_or_404(Oddzial, pk=oddzial_nazwa)
    initial_values = {'name': oddzial.nazwa,
                      'opening_hour': oddzial.godzina_otwarcia,
                      'closing_hour': oddzial.godzina_zamkniecia,
                      'address': oddzial.adres,
                      'number': oddzial.numer_telefonu}

    if request.POST:
        form = OddzialForm(request.POST)
    else:
        form = OddzialForm(instance=initial_values)

    error = ""
    error_time = ""
    error_number = ""
    if form.is_valid():
        name = form.cleaned_data['name']
        opening_hour = form.cleaned_data['opening_hour']
        closing_hour = form.cleaned_data['closing_hour']
        address = form.cleaned_data['address']
        number = form.cleaned_data['number']

        if opening_hour > closing_hour:
            error_time = "Godzina otwarcia musi być przed godziną zamknięcia!"
            return render(request, 'museum_app/add_oddzial.html',
                          {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error,
                           'tag': "Edytuj"})

        validator = number_validator(number)
        if validator == -1:
            error_number = "Niepoprawny numer telefonu."
            return render(request, 'museum_app/add_oddzial.html',
                          {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error,
                           'tag': "Edytuj"})

        if oddzial_nazwa != name:
            cursor = connection.cursor()
            cursor.execute("UPDATE museum_app_oddzial SET nazwa = %s WHERE nazwa = %s;", [name, oddzial_nazwa])
            cursor.close()
        oddzial.nazwa = name
        oddzial.godzina_otwarcia = opening_hour
        oddzial.godzina_zamkniecia = closing_hour
        oddzial.adres = address
        oddzial.numer_telefonu = number
        try:
            oddzial.save(force_update=True)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args:
                error = "Ta nazwa oddziału już istnieje."
            return render(request, 'museum_app/add_oddzial.html',
                          {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error,
                           'tag': "Edytuj"})

        else:
            return redirect('/table/oddzialy')
    return render(request, 'museum_app/add_oddzial.html',
                  {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error,
                   'tag': "Edytuj"})


def edit_dzial(request, dzial_id):
    dzial = get_object_or_404(Dzial, pk=dzial_id)
    error = ""
    initial_values = {'name': dzial.nazwa,
                      'floor': dzial.pietro,
                      'epoch': dzial.epoka,
                      'oddzial_select': dzial.oddzial_nazwa.nazwa}

    if request.POST:
        form = DzialForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], request.POST)
    else:
        form = DzialForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], instance=initial_values)
    if form.is_valid():
        name = form.cleaned_data['name']
        floor = form.cleaned_data['floor']
        epoch = form.cleaned_data['epoch']
        oddzial_select = form.cleaned_data['oddzial_select']
        for x in Oddzial.objects.all():
            if str(x.nazwa) == str(oddzial_select):
                oddzial = x

        dzial.nazwa = name
        dzial.pietro = floor
        dzial.epoka = epoch
        dzial.oddzial_nazwa = oddzial

        try:
            dzial.save(force_update=True)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args[1]:
                error = "Dział o tej nazwie już istnieje na wybranym oddziale."
            return render(request, 'museum_app/add_dzial.html',
                          {'form': form, 'error': error, 'tag': "Edytuj"})
        else:
            return redirect('/table/dzialy')
    return render(request, 'museum_app/add_dzial.html', {'form': form, 'error': error, 'tag': "Edytuj"})


def edit_obraz(request, obraz_id):
    obraz = get_object_or_404(Obraz, pk=obraz_id)
    initial_values = {'name': obraz.nazwa,
                      'width': obraz.szerokosc,
                      'height': obraz.wysokosc,
                      'artysta_select': obraz.artysta_id.id,
                      'dzial_select': str(obraz.dzial_id.nazwa) + " ; " + str(obraz.dzial_id.oddzial_nazwa.nazwa)}
    artysta_choices = [("-", "-")]
    for x in Artysta.objects.all():
        artysta_choices.append((x.id, x.imie + " " + x.nazwisko))
    dzial_choices = [(str(x.nazwa) + " ; " + str(x.oddzial_nazwa.nazwa),
                      str(x.nazwa) + ", " + str(x.oddzial_nazwa.nazwa)) for x in
                     Dzial.objects.all()]

    if request.POST:
        form = ObrazForm(dzial_choices, artysta_choices, request.POST)
    else:
        form = ObrazForm(dzial_choices, artysta_choices, instance=initial_values)

    if form.is_valid():
        name = form.cleaned_data['name']
        width = form.cleaned_data['width']
        height = form.cleaned_data['height']
        dzial_select = form.cleaned_data['dzial_select'].split(" ; ")
        artysta_select = form.cleaned_data['artysta_select']
        if artysta_select == "-":
            artysta_select = None

        dzial_id = None
        for x in Dzial.objects.all():
            if x.nazwa == dzial_select[0] and x.oddzial_nazwa.nazwa == dzial_select[1]:
                dzial_id = x

        artysta_id = None
        for x in Artysta.objects.all():
            if str(x.id) == artysta_select:
                artysta_id = x

        obraz.nazwa = name
        obraz.szerokosc = width
        obraz.wysokosc = height
        obraz.dzial_id = dzial_id
        obraz.artysta_id = artysta_id

        obraz.save(force_update=True)
        return redirect('/table/dziela')

    return render(request, 'museum_app/add_obraz.html', {'form': form, 'tag': "Edytuj"})


def edit_rzezba(request, rzezba_id):
    rzezba = get_object_or_404(Rzezba, pk=rzezba_id)
    initial_values = {'name': rzezba.nazwa,
                      'weight': rzezba.waga,
                      'material': rzezba.material,
                      'artysta_select': rzezba.artysta_id.id,
                      'dzial_select': str(rzezba.dzial_id.nazwa) + " ; " + str(rzezba.dzial_id.oddzial_nazwa.nazwa)}
    artysta_choices = [("-", "-")]
    for x in Artysta.objects.all():
        artysta_choices.append((x.id, x.imie + " " + x.nazwisko))
    dzial_choices = [(str(x.nazwa) + " ; " + str(x.oddzial_nazwa.nazwa),
                      str(x.nazwa) + ", " + str(x.oddzial_nazwa.nazwa)) for x in
                     Dzial.objects.all()]

    if request.POST:
        form = RzezbaForm(dzial_choices, artysta_choices, request.POST)
    else:
        form = RzezbaForm(dzial_choices, artysta_choices, instance=initial_values)

    if form.is_valid():
        name = form.cleaned_data['name']
        weight = form.cleaned_data['weight']
        material = form.cleaned_data['material']
        dzial_select = form.cleaned_data['dzial_select'].split(" ; ")
        artysta_select = form.cleaned_data['artysta_select']
        if artysta_select == "-":
            artysta_select = None

        dzial_id = None
        for x in Dzial.objects.all():
            if x.nazwa == dzial_select[0] and x.oddzial_nazwa.nazwa == dzial_select[1]:
                dzial_id = x

        artysta_id = None
        for x in Artysta.objects.all():
            if str(x.id) == artysta_select:
                artysta_id = x

        rzezba.nazwa = name
        rzezba.szerokosc = width
        rzezba.wysokosc = height
        rzezba.dzial_id = dzial_id
        rzezba.artysta_id = artysta_id

        rzezba.save(force_update=True)
        return redirect('/table/dziela')

    return render(request, 'museum_app/add_rzezba.html', {'form': form, 'tag': "Edytuj"})


def edit_artysta(request, artysta_id):
    artysta = get_object_or_404(Artysta, pk=artysta_id)
    initial_values = {'name': artysta.imie,
                      'surname': artysta.nazwisko,
                      'birth_date': artysta.data_urodzenia,
                      'death_date': artysta.data_smierci}
    if request.POST:
        form = ArtystaForm(request.POST)
    else:
        form = ArtystaForm(instance=initial_values)

    error = ""
    error_birth = ""
    error_death = ""
    if form.is_valid():
        name = form.cleaned_data['name']
        surname = form.cleaned_data['surname']
        birth_date = form.cleaned_data['birth_date']
        death_date = form.cleaned_data['death_date']

        birth_year = birth_date.split("-")[0]

        if len(birth_year) > 4:
            error_birth = "Rok nie może być większy od 9999"
            return render(request, 'museum_app/add_artysta.html',
                          {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death,
                           'tag': "Dodaj"})
        if death_date != "":
            death_year = death_date.split("-")[0]
            if len(death_year) > 4:
                error_death = "Rok nie może być większy od 9999"
                return render(request, 'museum_app/add_artysta.html',
                              {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death,
                               'tag': "Dodaj"})
            if death_date < birth_date:
                error = "Data urodzenia musi być wcześniejsza niż data śmierci!"
                return render(request, 'museum_app/add_artysta.html',
                              {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death,
                               'tag': "Dodaj"})

        else:
            death_date = None

        artysta.imie = name
        artysta.nazwisko = surname
        artysta.data_urodzenia = birth_date
        artysta.data_smierci = death_date

        artysta.save(force_update=True)
        return redirect('/table/artysci')

    return render(request, 'museum_app/add_artysta.html',
                  {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death,
                   'tag': "Edytuj"})


def edit_bilet(request, bilet_id):
    error = ""
    error_oddzial = ""
    error_data = ""
    typ = []
    is_przewodnik = []
    for x in Rodzaj_biletu.objects.all():
        if x.czy_z_przewodnikiem == 0:
            typ.append((x.id, str(x.typ) + " bez przewodnika, " + str(x.oddzial_nazwa.nazwa)))
            is_przewodnik.append((x.id, 0))
        else:
            typ.append((x.id, str(x.typ) + " z przewodnikiem, " + str(x.oddzial_nazwa.nazwa)))
            is_przewodnik.append((x.id, 1))
    json_przewodnik = json.dumps(is_przewodnik)

    try:
        harmonogram_zwiedzania_id = bilet.harmonogram_zwiedzania_id.id
    except:
        harmonogram_zwiedzania_id = None
    bilet = get_object_or_404(Bilet, pk=bilet_id)
    initial_values = {'type': bilet.rodzaj_biletu_id.id,
                      'wycieczka': harmonogram_zwiedzania_id,
                      'purchase_date': bilet.data_zakupu}
    if request.POST:
        form = BiletForm(typ, [
            (x.id, str(x.pracownik_pesel.oddzial_nazwa.nazwa) + ", " + str(x.data) + " " + str(x.godzina_rozpoczecia) +
             ", " + str(x.pracownik_pesel.imie) + " " + str(x.pracownik_pesel.nazwisko)) for x in
            Harmonogram_zwiedzania.objects.all()], request.POST)
    else:
        form = BiletForm(typ, [
            (x.id, str(x.pracownik_pesel.oddzial_nazwa.nazwa) + ", " + str(x.data) + " " + str(x.godzina_rozpoczecia) +
             ", " + str(x.pracownik_pesel.imie) + " " + str(x.pracownik_pesel.nazwisko)) for x in
            Harmonogram_zwiedzania.objects.all()], instance=initial_values)

    if form.is_valid():
        purchase_date = form.cleaned_data['purchase_date']
        type = form.cleaned_data['type']
        wycieczka = form.cleaned_data['wycieczka']

        if len(purchase_date.split("-")[0]) > 4:
            error_data = "Rok nie może być większy niż 9999"
            return render(request, 'museum_app/add_bilet.html',
                          {'form': form, 'error': error, 'error_oddzial': error_oddzial, 'error_data': error_data,
                           'tag': "Dodaj", "json_przewodnik": json_przewodnik})

        rodzaj_biletu_id = None
        for x in Rodzaj_biletu.objects.all():
            if str(x.id) == str(type):
                rodzaj_biletu_id = x

        harmonogram = None
        for x in Harmonogram_zwiedzania.objects.all():
            if str(x.id) == str(wycieczka):
                harmonogram = x

        if harmonogram is not None:
            if harmonogram.pracownik_pesel.oddzial_nazwa.nazwa != rodzaj_biletu_id.oddzial_nazwa.nazwa:
                error_oddzial = "Ta wycieczka odbywa się na innym oddziale!"
                return render(request, 'museum_app/add_bilet.html',
                              {'form': form, 'error': error, 'error_oddzial': error_oddzial, 'error_data': error_data,
                               'tag': "Dodaj", "json_przewodnik": json_przewodnik})

        bilet.rodzaj_biletu_id = rodzaj_biletu_id
        bilet.harmonogram_zwiedzania_id = harmonogram
        bilet.data_zakupu = purchase_date

        bilet.save(force_update=True)
        return redirect('/table/bilety')

    return render(request, 'museum_app/add_bilet.html',
                  {'form': form, 'error': error, 'error_oddzial': error_oddzial, 'error_data': error_data,
                   'tag': "Edytuj", "json_przewodnik": json_przewodnik})


def edit_rodzaj_biletu(request, rodzaj_biletu_id):
    rodzaj_biletu = get_object_or_404(Rodzaj_biletu, pk=rodzaj_biletu_id)
    initial_values = {'oddzial': rodzaj_biletu.oddzial_nazwa.nazwa,
                      'przewodnik': rodzaj_biletu.czy_z_przewodnikiem,
                      'type': rodzaj_biletu.typ,
                      'price': rodzaj_biletu.cena}
    if request.POST:
        form = RodzajBiletuForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], request.POST)
    else:
        form = RodzajBiletuForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], instance=initial_values)
    error = ""
    if form.is_valid():
        przewodnik = form.cleaned_data['przewodnik']
        oddzial = form.cleaned_data['oddzial']
        type = form.cleaned_data['type']
        price = form.cleaned_data['price']
        for x in Oddzial.objects.all():
            if str(x.nazwa) == str(oddzial):
                oddzial = x
        if przewodnik == "tak":
            przewodnik = True
        else:
            przewodnik = False

        rodzaj_biletu.typ = type
        rodzaj_biletu.oddzial_nazwa = oddzial
        rodzaj_biletu.czy_z_przewodnikiem = przewodnik
        rodzaj_biletu.cena = price
        try:
            rodzaj_biletu.save(force_update=True)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args[1]:
                error = "Taki rodzaj bilet już istnieje."
            return render(request, 'museum_app/add_rodzaj_biletu.html', {'form': form, 'error': error, 'tag': "Edytuj"})

        return redirect('/table/rodzaje_biletow')

    return render(request, 'museum_app/add_rodzaj_biletu.html', {'form': form, 'error': error, 'tag': "Edytuj"})


def edit_pracownik(request, pracownik_pesel):
    pracownik = get_object_or_404(Pracownik, pk=pracownik_pesel)
    initial_values = {'pesel': pracownik.pesel,
                      'imie': pracownik.imie,
                      'nazwisko': pracownik.nazwisko,
                      'etat': pracownik.etat,
                      'placa': pracownik.placa,
                      'data_zatrudnienia': pracownik.data_zatrudnienia,
                      'numer_telefonu': pracownik.numer_telefonu,
                      'oddzial': pracownik.oddzial_nazwa.nazwa}
    if request.POST:
        form = PracownikForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], request.POST)
    else:
        form = PracownikForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], instance=initial_values)
    error = ""
    error_number = ""
    error_date = ""
    if form.is_valid():
        pesel = form.cleaned_data['pesel']
        imie = form.cleaned_data['imie']
        nazwisko = form.cleaned_data['nazwisko']
        etat = form.cleaned_data['etat']
        placa = form.cleaned_data['placa']
        data_zatrudnienia = form.cleaned_data['data_zatrudnienia']
        oddzial = form.cleaned_data['oddzial']
        numer_telefonu = form.cleaned_data['numer_telefonu']

        if len(data_zatrudnienia.split("-")[0]) > 4:
            error_date = "Rok nie może być większy od 9999"
            return render(request, 'museum_app/add_pracownik.html',
                          {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date,
                           'tag': "Edytuj"})

        for x in Oddzial.objects.all():
            if str(x.nazwa) == str(oddzial):
                oddzial = x

        validator = number_validator(numer_telefonu)
        if validator == -1:
            error_number = "Niepoprawny numer telefonu."
            return render(request, 'museum_app/add_pracownik.html',
                          {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date,
                           'tag': "Edytuj"})
        else:
            numer_telefonu = validator

        if pracownik_pesel != pesel:
            cursor = connection.cursor()
            cursor.execute("UPDATE museum_app_pracownik SET pesel = %s WHERE pesel = %s;", [pesel, pracownik_pesel])
            cursor.close()
        pracownik.pesel = pesel
        pracownik.imie = imie
        pracownik.nazwisko = nazwisko
        pracownik.etat = etat
        pracownik.placa = placa
        pracownik.data_zatrudnienia = data_zatrudnienia
        pracownik.numer_telefonu = numer_telefonu
        try:
            pracownik.save(force_update=True)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args[1]:
                error = "Pracownik o tym peselu już istnieje"
            return render(request, 'museum_app/add_pracownik.html',
                          {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date,
                           'tag': "Edytuj"})
        else:
            return redirect('/table/pracownicy')

    return render(request, 'museum_app/add_pracownik.html',
                  {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date,
                   'tag': "Edytuj"})


def edit_harmonogram_zwiedzania(request, harmonogram_zwiedzania_id):
    harmonogram_zwiedzania = get_object_or_404(Harmonogram_zwiedzania, pk=harmonogram_zwiedzania_id)
    initial_values = {'godzina': harmonogram_zwiedzania.godzina_rozpoczecia,
                      'data': harmonogram_zwiedzania.data,
                      'pesel': harmonogram_zwiedzania.pracownik_pesel.pesel}
    if request.POST:
        form = HarmonogramZwiedzaniaForm(
            [(x.pesel, x.imie + " " + x.nazwisko + " (" + str(x.pesel) + ")") for x in Pracownik.objects.all()],
            request.POST)
    else:
        form = HarmonogramZwiedzaniaForm(
            [(x.pesel, x.imie + " " + x.nazwisko + " (" + str(x.pesel) + ")") for x in Pracownik.objects.all()],
            instance=initial_values)
    error_date = ""
    error = ""
    if form.is_valid():
        godzina = form.cleaned_data['godzina']
        data = form.cleaned_data['data']
        pesel = form.cleaned_data['pesel']

        if len(data.split("-")[0]) > 4:
            error_date = "Rok nie może być większy od 9999"
            return render(request, 'museum_app/add_harmonogram_zwiedzania.html',
                          {'form': form, 'error': error, 'error_date': error_date, 'tag': "Edytuj"})

        for x in Pracownik.objects.all():
            if str(x.pesel) == str(pesel):
                pracownik = x

        harmonogram_zwiedzania.pracownik_pesel = pracownik
        harmonogram_zwiedzania.data = data
        harmonogram_zwiedzania.godzina_rozpoczecia = godzina

        try:
            harmonogram_zwiedzania.save(force_update=True)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args[1]:
                error = "Taki harmonogram zwiedzania już istnieje"
            return render(request, 'museum_app/add_harmonogram_zwiedzania.html',
                          {'form': form, 'error': error, 'error_date': error_date, 'tag': "Edytuj"})
        else:
            return redirect('/table/harmonogram_zwiedzania')

    return render(request, 'museum_app/add_harmonogram_zwiedzania.html',
                  {'form': form, 'error': error, 'error_date': error_date, 'tag': "Edytuj"})


def edit_wydarzenie(request):
    form = WydarzenieForm(request.POST)
    return render(request, 'museum_app/add_wydarzenie.html', {'form': form})


def detailed_oddzial(request, oddzial_nazwa):
    form = TableWydarzeniaForm(request.POST)
    error = ""
    if request.method == 'POST' and form.is_valid():
        if 'delete' in request.POST:
            for item in form.cleaned_data['choices']:
                for x in Wydarzenie_oddzial.objects.all():
                    if str(x.wydarzenie_id_id) == str(item.id) and str(x.oddzial_nazwa.nazwa) == str(oddzial_nazwa):
                        try:
                            x.delete()
                        except Exception as e:
                            error = e.args[0]

    oddzial = get_object_or_404(Oddzial, pk=oddzial_nazwa)
    wydarzenie_oddzial = []
    for i in Wydarzenie_oddzial.objects.all():
        if i.oddzial_nazwa.nazwa == oddzial.nazwa:
            wydarzenie_oddzial.append(i)
    wydarzenia = []
    for wydarzenie in Wydarzenie.objects.all():
        for i in wydarzenie_oddzial:
            if wydarzenie.id == i.wydarzenie_id.id:
                wydarzenia.append(wydarzenie)
    initial_values = {'name': oddzial.nazwa, 'opening_hour': oddzial.godzina_otwarcia,
                      'closing_hour': oddzial.godzina_zamkniecia, 'address': oddzial.adres,
                      'number': oddzial.numer_telefonu}

    form = DetailedOddzialForm(initial=initial_values)
    return render(request, 'museum_app/detailed_oddzial.html',
                  {'form': form, 'wydarzenia': wydarzenia, 'error': error, 'oddzial': oddzial})


def detailed_dzial(request, dzial_id):
    # TODO fill obrazy and rzezby - add POST
    dzial = get_object_or_404(Dzial, pk=dzial_id)
    obrazy = []
    for x in Obraz.objects.all():
        try:
            if x.dzial_id.id == dzial.id:
                obrazy.append((x.nazwa, x.nazwa))
        except:
            continue

    rzezby = []
    for x in Rzezba.objects.all():
        try:
            if x.dzial_id.id == dzial.id:
                rzezby.append((x.nazwa, x.nazwa))
        except:
            continue

    if dzial.epoka == None:
        epoka = "Brak informacji"
    else:
        epoka = dzial.epoka
    initial_values = {
        "name": dzial.nazwa,
        "oddzial": dzial.oddzial_nazwa.nazwa,
        "floor": dzial.pietro,
        "epoch": epoka,
    }

    form = DetailedDzialForm(obrazy, rzezby, initial=initial_values)
    return render(request, 'museum_app/detailed_dzial.html', {'form': form})


def detailed_artysta(request, artysta_id):
    # TODO fill obrazy and rzezby - add POST somehow
    artysta = get_object_or_404(Artysta, pk=artysta_id)
    obrazy = []
    for x in Obraz.objects.all():
        try:
            if x.artysta_id.id == artysta_id:
                obrazy.append((x.nazwa, x.nazwa))
        except:
            continue

    rzezby = []
    for x in Rzezba.objects.all():
        try:
            if x.artysta_id.id == artysta_id:
                rzezby.append((x.nazwa, x.nazwa))
        except:
            continue

    initial_values = {
        "name": artysta.imie,
        "surname": artysta.nazwisko,
        "birth_date": artysta.data_urodzenia,
        "death_date": artysta.data_smierci,
    }
    form = DetailedArtystaForm(obrazy, rzezby, initial=initial_values)
    return render(request, 'museum_app/detailed_artysta.html', {'form': form})


def detailed_obraz(request, obraz_id):
    # for rzeźba pass -1 in width and height, for obraz pass -1 for weight and material
    obraz = get_object_or_404(Obraz, pk=obraz_id)
    try:
        artysta = (obraz.artysta_id.imie + " " + obraz.artysta_id.nazwisko)
    except AttributeError:
        artysta = "Anonimowy"

    initial_values = {
        "name": obraz.nazwa,
        "branch": obraz.dzial_id.oddzial_nazwa.nazwa,
        "department": obraz.dzial_id.nazwa,
        "artist": artysta,
        "width": obraz.szerokosc,
        "height": obraz.wysokosc,
        "weight": -1,
        "material": -1
    }
    form = DetailedDzieloForm(initial=initial_values)
    return render(request, 'museum_app/detailed_dzielo.html', {'form': form})


def detailed_rzezba(request, rzezba_id):
    rzezba = get_object_or_404(Rzezba, pk=rzezba_id)
    # for rzeźba pass -1 in width and height, for obraz pass -1 for weight and material
    try:
        artysta = (rzezba.artysta_id.imie + " " + rzezba.artysta_id.nazwisko)
    except AttributeError:
        artysta = "Anonimowy"

    initial_values = {
        "name": rzezba.nazwa,
        "branch": rzezba.dzial_id.oddzial_nazwa.nazwa,
        "department": rzezba.dzial_id.nazwa,
        "artist": artysta,
        "width": -1,
        "height": -1,
        "weight": rzezba.waga,
        "material": rzezba.material
    }
    form = DetailedDzieloForm(initial=initial_values)
    return render(request, 'museum_app/detailed_dzielo.html', {'form': form})
