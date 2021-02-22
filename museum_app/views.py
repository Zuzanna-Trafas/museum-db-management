from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import FieldDoesNotExist
from django.core.exceptions import ValidationError
from django.http import Http404
from django.db import connection
from plotly.offline import plot
from plotly.graph_objs import Bar
from museum_app.forms import OddzialForm, DzialForm, ObrazForm, RzezbaForm, ArtystaForm, BiletForm, RodzajBiletuForm, \
    PracownikForm, HarmonogramZwiedzaniaForm, WydarzenieForm, DetailedArtystaForm, DetailedDzialForm, \
    DetailedDzieloForm, DetailedOddzialForm, TableOddzialForm, TableDzialForm, TableArtystaForm, TableBiletyForm, \
    TableHarmonogramZwiedzaniaForm, TableDzieloForm, TablePracownikForm, TableRodzajeBiletowForm, TableWydarzeniaForm,\
    MainForm
from museum_app.models import Oddzial, Wydarzenie, Wydarzenie_oddzial, Rodzaj_biletu, Pracownik, Harmonogram_zwiedzania, \
    Bilet, Dzial, Artysta, Obraz, Rzezba
import sys


# TODO walidacja pól unique

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
    # TODO searching
    kolumny = {"oddzial": ["Nazwa", "Godzina otwarcia", "Godzina zamknięcia", "Adres", "Numer telefonu"],
               "wydarzenie": ["Nazwa", "Data rozpoczęcia", "Data zakończenia"],
               "dzial": ["Nazwa", "Nazwa oddziału", "Piętro", "Epoka"],
               "dzielo": ["Nazwa", "Artysta", "Dział"],
                "artysta" : ["Imię", "Nazwisko", "Data urodzenia", "Data śmierci"],
                "rodzaj_biletu" : ["Typ", "Oddział", "Czy z przewodnikiem", "Cena"],
                "bilet": ["Data zakupu", "Oddział", "Typ biletu", "Cena", "Czy z przewodnikiem"],
                "pracownik": ["Pesel", "Imię", "Nazwisko", "Płaca", "Etat", "Data zatrudnienia", "Numer telefonu"],
                "harmonogram_zwiedzania": ["Data", "Godzina rozpoczęcia", "Przewodnik", "Ilość kupionych biletów"]}
    wyniki = []
    #TODO jaki format wyników tho = for (obiektow) a w nim for (atrybutow)
    cursor = connection.cursor()
    cursor.execute("SET NAMES 'UTF8';")  # or utf8 or any other charset you want to handle

    cursor.execute("SET CHARACTER SET 'UTF8';")  # same as above

    cursor.execute("SET character_set_connection='UTF8';")  # same as above

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
    return render(request, 'museum_app/main.html', context={'form': form, 'plot_div': plot_div, 'kolumny': kolumny["pracownik"], 'wyniki': wyniki})


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
                          {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error})

        validator = number_validator(number)
        if validator == -1:
            error_number = "Niepoprawny numer telefonu."
            return render(request, 'museum_app/add_oddzial.html',
                          {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error})
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
                          {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error})

        else:
            return redirect('/table/oddzialy')

    return render(request, 'museum_app/add_oddzial.html',
                  {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error})


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
                          {'form': form, 'error': error})
        else:
            return redirect('/table/dzialy')
    return render(request, 'museum_app/add_dzial.html', {'form': form, 'error': error})


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

    return render(request, 'museum_app/add_obraz.html', {'form': form})


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

    return render(request, 'museum_app/add_rzezba.html', {'form': form})


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
                          {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death})
        if death_date != "":
            death_year = death_date.split("-")[0]
            if len(death_year) > 4:
                error_death = "Rok nie może być większy od 9999"
                return render(request, 'museum_app/add_artysta.html',
                              {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death})
            if death_date < birth_date:
                error = "Data urodzenia musi być wcześniejsza niż data śmierci!"
                return render(request, 'museum_app/add_artysta.html',
                              {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death})

        else:
            death_date = None
        Artysta.objects.create(imie=name, nazwisko=surname, data_urodzenia=birth_date, data_smierci=death_date)
        return redirect('/table/artysci')

    return render(request, 'museum_app/add_artysta.html',
                  {'form': form, 'error': error, 'error_birth': error_birth, 'error_death': error_death})


def add_bilet(request):
    error = ""
    error_oddzial = ""
    error_data = ""
    typ = []
    for x in Rodzaj_biletu.objects.all():
        if (str(x.typ) + " ; " + str(x.oddzial_nazwa.nazwa), str(x.typ) + ", " + str(x.oddzial_nazwa.nazwa)) not in typ:
            typ.append(
                (str(x.typ) + " ; " + str(x.oddzial_nazwa.nazwa), str(x.typ) + ", " + str(x.oddzial_nazwa.nazwa)))

    form = BiletForm(typ, [
        (x.id, str(x.pracownik_pesel.oddzial_nazwa.nazwa) + ", " + str(x.data) + " " + str(x.godzina_rozpoczecia) +
         ", " + str(x.pracownik_pesel.imie) + " " + str(x.pracownik_pesel.nazwisko)) for x in
        Harmonogram_zwiedzania.objects.all()],
                     request.POST)
    if form.is_valid():
        purchase_date = form.cleaned_data['purchase_date']
        przewodnik = form.cleaned_data['przewodnik']
        type = form.cleaned_data['type'].split(" ; ")
        wycieczka = form.cleaned_data['wycieczka']

        if len(purchase_date.split("-")[0]) > 4:
            error_data = "Rok nie może być większy niż 9999"
            return render(request, 'museum_app/add_bilet.html',
                          {'form': form, 'error': error, 'error_oddzial': error_oddzial, 'error_data': error_data})

        rodzaj_biletu_id = None
        for x in Rodzaj_biletu.objects.all():
            if x.typ == type[0] and ((przewodnik == "tak" and x.czy_z_przewodnikiem == True) or (
                    przewodnik == "nie" and x.czy_z_przewodnikiem == False)) and x.oddzial_nazwa.nazwa == type[1]:
                rodzaj_biletu_id = x

        if rodzaj_biletu_id == None:
            error = "Dla tego typu biletu nie można wybrać wycieczki"
            return render(request, 'museum_app/add_bilet.html',
                          {'form': form, 'error': error, 'error_oddzial': error_oddzial, 'error_data': error_data})

        harmonogram = None
        for x in Harmonogram_zwiedzania.objects.all():
            if str(x.id) == str(wycieczka):
                harmonogram = x

        if harmonogram is not None:
            if harmonogram.pracownik_pesel.oddzial_nazwa.nazwa != type[0]:
                error_oddzial = "Ta wycieczka odbywa się na innym oddziale!"
                return render(request, 'museum_app/add_bilet.html',
                              {'form': form, 'error': error, 'error_oddzial': error_oddzial, 'error_data': error_data})

        Bilet.objects.create(data_zakupu=purchase_date, rodzaj_biletu_id=rodzaj_biletu_id,
                             harmonogram_zwiedzania_id=harmonogram)

        return redirect('/table/bilety')

    return render(request, 'museum_app/add_bilet.html',
                  {'form': form, 'error': error, 'error_oddzial': error_oddzial, 'error_data': error_data})


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
            return render(request, 'museum_app/add_rodzaj_biletu.html', {'form': form, 'error': error})

        return redirect('/table/rodzaje_biletow')

    return render(request, 'museum_app/add_rodzaj_biletu.html', {'form': form, 'error': error})


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
                          {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date})

        for x in Oddzial.objects.all():
            if str(x.nazwa) == str(oddzial):
                oddzial = x

        validator = number_validator(numer_telefonu)
        if validator == -1:
            error_number = "Niepoprawny numer telefonu."
            return render(request, 'museum_app/add_pracownik.html',
                          {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date})
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
                          {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date})
        else:
            return redirect('/table/pracownicy')

    return render(request, 'museum_app/add_pracownik.html',
                  {'form': form, 'error_number': error_number, 'error': error, 'error_date': error_date})


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
                          {'form': form, 'error': error, 'error_date': error_date})

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
                          {'form': form, 'error': error, 'error_date': error_date})
        else:
            return redirect('/table/harmonogram_zwiedzania')

    return render(request, 'museum_app/add_harmonogram_zwiedzania.html',
                  {'form': form, 'error': error, 'error_date': error_date})


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
                           'error_data_zakonczenia': error_data_zakonczenia, 'error_dates': error_dates})

        if len(data_zakonczenia.split("-")[0]) > 4:
            error_data_zakonczenia = "Rok nie może być większy od 9999"
            return render(request, 'museum_app/add_wydarzenie.html',
                          {'form': form, 'error': error, 'error_data_rozpoczecia': error_data_rozpoczecia,
                           'error_data_zakonczenia': error_data_zakonczenia, 'error_dates': error_dates})

        if data_rozpoczecia > data_zakonczenia:
            error_dates = "Data rozpoczęcia musi być przed datą zakończenia!"
            return render(request, 'museum_app/add_wydarzenie.html',
                          {'form': form, 'error': error, 'error_data_rozpoczecia': error_data_rozpoczecia,
                           'error_data_zakonczenia': error_data_zakonczenia, 'error_dates': error_dates})

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
                           'error_data_zakonczenia': error_data_zakonczenia, 'error_dates': error_dates})

        for oddzial in oddzialy:
            Wydarzenie_oddzial.objects.create(oddzial_nazwa=oddzial, wydarzenie_id=wydarzenie)

        return redirect('/detailed/' + str(oddzial_nazwa) + '/oddzial')

    return render(request, 'museum_app/add_wydarzenie.html',
                  {'form': form, 'error': error, 'error_data_rozpoczecia': error_data_rozpoczecia,
                   'error_data_zakonczenia': error_data_zakonczenia, 'error_dates': error_dates})


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

        validator = number_validator(number)
        if validator == -1:
            error_number = "Niepoprawny numer telefonu."
        else:
            number = validator

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
                          {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error})

        else:
            return redirect('/table/oddzialy')
    return render(request, 'museum_app/add_oddzial.html',
                  {'form': form, 'error_time': error_time, 'error_number': error_number, 'error': error})


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
        dzial.oddzial_nazwa = x

        try:
            dzial.save(force_update=True)
        except Exception as e:
            error = e.args
            if "Duplicate" in e.args[1]:
                error = "Dział o tej nazwie już istnieje na wybranym oddziale."
            return render(request, 'museum_app/add_dzial.html',
                          {'form': form, 'error': error})
        else:
            return redirect('/table/dzialy')
    return render(request, 'museum_app/add_dzial.html', {'form': form, 'error': error})


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


def detailed_oddzial(request, oddzial_nazwa):
    form = TableWydarzeniaForm(request.POST)
    error = ""
    if request.method == 'POST' and form.is_valid():
        if 'delete' in request.POST:
            for item in form.cleaned_data['choices']:
                try:
                    item.delete()
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
