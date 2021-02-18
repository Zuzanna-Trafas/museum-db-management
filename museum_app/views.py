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
    TableHarmonogramZwiedzaniaForm, TableDzieloForm, TablePracownikForm, TableRodzajeBiletowForm, TableWydarzeniaForm
from museum_app.models import Oddzial, Wydarzenie, Wydarzenie_oddzial, Rodzaj_biletu, Pracownik, Harmonogram_zwiedzania, \
    Bilet, Dzial, Artysta, Obraz, Rzezba
import sys


def get_profit(cursor, typ, czy_z_przewodnikiem, oddzial):
    cursor.execute("SELECT policz_dochod(%s, %s, %s)", [typ, czy_z_przewodnikiem, oddzial])
    return cursor.fetchone()[0]


def main(request):
    # TODO searching
    cursor = connection.cursor()
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
    return render(request, 'museum_app/main.html', context={'plot_div': plot_div})


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


# TODO handle adding for all tables (also wydarzenia)
# TODO redirect to table view after submit


def add_oddzial(request):
    form = OddzialForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        opening_hour = form.cleaned_data['opening_hour']
        closing_hour = form.cleaned_data['closing_hour']
        address = form.cleaned_data['address']
        number = form.cleaned_data['number']

        #if opening_hour > closing_hour:
        #    self.add"Godzina otwarcia musi być przed godziną zamknięcia!")

        #else:
        Oddzial.objects.create(nazwa=name, godzina_otwarcia=opening_hour, godzina_zamkniecia=closing_hour, adres=address, numer_telefonu=number)
        return redirect('/table/oddzialy')
    return render(request, 'museum_app/add_oddzial.html', {'form': form})


def add_dzial(request):
    form = DzialForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        floor = form.cleaned_data['floor']
        epoch = form.cleaned_data['epoch']
        oddzial_select = form.cleaned_data['oddzial_select'][0]
        for x in Oddzial.objects.all():
            print(x.nazwa, file=sys.stderr)
            print(oddzial_select, file=sys.stderr)
            if str(x.nazwa) == str(oddzial_select):
                print("WHYYYYYY", file=sys.stderr)
                oddzial = x
        Dzial.objects.create(nazwa=name, pietro=floor, epoka=epoch,
                             oddzial_nazwa=oddzial)
        return redirect('/table/dzialy')
    return render(request, 'museum_app/add_dzial.html', {'form': form})


def add_obraz(request):
    # TODO dynamically fill Działy depending on Oddziały or merge both to one select field
    form = ObrazForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()], [(x.nazwa, x.nazwa) for x in Dzial.objects.all()], [(x.imie+" "+x.nazwisko, x.imie+" "+x.nazwisko) for x in Artysta.objects.all()], request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        width = form.cleaned_data['width']
        height = form.cleaned_data['height']
        oddzial_select = form.cleaned_data['oddzial_select'][0]
        dzial_select = form.cleaned_data['dzial_select'][0]
        artysta_select = form.cleaned_data['artysta_select'][0]

        dzial_id = -1
        for x in Dzial.objects.all():

            if x.nazwa == dzial_select and x.oddzial_nazwa.nazwa == oddzial_select:
                dzial_id = x

        artysta_id = -1
        for x in Artysta.objects.all():
            if x.imie == artysta_select.split(" ")[0] and x.nazwisko == artysta_select.split(" ")[1]:
                artysta_id = x

        Obraz.objects.create(nazwa=name, szerokosc=width, wysokosc=height, dzial_id=dzial_id, artysta_id = artysta_id)
        return redirect('/table/dziela')

    return render(request, 'museum_app/add_obraz.html', {'form': form})


def add_rzezba(request):
    # TODO dynamically fill Działy depending on Oddziały or merge both to one select field
    form = RzezbaForm([(x.nazwa, x.nazwa) for x in Oddzial.objects.all()],
                     [(x.nazwa, x.nazwa) for x in Dzial.objects.all()],
                     [(x.imie + " " + x.nazwisko, x.imie + " " + x.nazwisko) for x in Artysta.objects.all()],
                     request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        weight = form.cleaned_data['weight']
        material = form.cleaned_data['material']
        oddzial_select = form.cleaned_data['oddzial_select'][0]
        dzial_select = form.cleaned_data['dzial_select'][0]
        artysta_select = form.cleaned_data['artysta_select'][0]

        dzial_id = -1
        for x in Dzial.objects.all():
            print(x.nazwa, file=sys.stderr)
            print(dzial_select, file=sys.stderr)
            print(x.oddzial_nazwa.nazwa, file=sys.stderr)
            print(oddzial_select, file=sys.stderr)
            if x.nazwa == dzial_select and x.oddzial_nazwa.nazwa == oddzial_select:
                dzial_id = x

        artysta_id = -1
        for x in Artysta.objects.all():
            if x.imie == artysta_select.split(" ")[0] and x.nazwisko == artysta_select.split(" ")[1]:
                artysta_id = x

        Rzezba.objects.create(nazwa=name, waga=weight, material=material, dzial_id=dzial_id, artysta_id=artysta_id)
        return redirect('/table/dziela')

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


def add_wydarzenie(request):
    form = WydarzenieForm(request.POST)
    return render(request, 'museum_app/add_wydarzenie.html', {'form': form})


# TODO handle editing for all tables (also wydarzenia) - fill values with initial, like for detailed
# TODO disable primary keys after filling them for editing
# TODO figure out how to fill date and time fields
# TODO redirect to table view after submit

def edit_oddzial(request, oddzial_nazwa):
    oddzial = get_object_or_404(Oddzial, pk=oddzial_nazwa)
    initial_values = {'name': oddzial.nazwa,
                      'opening_hour': oddzial.godzina_otwarcia,
                      'closing_hour': oddzial.godzina_zamkniecia,
                      'address': oddzial.adres,
                      'number': oddzial.numer_telefonu}

    form = OddzialForm(initial=initial_values)
    if form.is_valid():
        name = form.cleaned_data['name']
        print(name, file=sys.stderr)
        return redirect('/')

    return render(request, 'museum_app/add_oddzial.html', {'form': form})


def edit_dzial(request):
    form = DzialForm([(1, 1), (2, 2)], request.POST)
    return render(request, 'museum_app/add_dzial.html', {'form': form})


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


# TODO fill initial values with values from model

def detailed_oddzial(request, oddzial_nazwa):
    form = TableWydarzeniaForm(request.POST)
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
    return render(request, 'museum_app/detailed_oddzial.html', {'form': form, 'wydarzenia': wydarzenia, 'error': error})


def detailed_dzial(request, dzial_id):
    dzial = get_object_or_404(Dzial, pk=dzial_id)
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
    form = DetailedDzialForm(initial=initial_values)
    return render(request, 'museum_app/detailed_dzial.html', {'form': form})


def detailed_artysta(request, artysta_id):
    artysta = get_object_or_404(Artysta, pk=artysta_id)

    initial_values = {
        "name": artysta.imie,
        "surname": artysta.nazwisko,
        "birth_date": artysta.data_urodzenia,
        "death_date": artysta.data_smierci,

    }
    form = DetailedArtystaForm(initial=initial_values)
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