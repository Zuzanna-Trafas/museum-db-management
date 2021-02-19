from django import forms
import sys
from museum_app.models import Oddzial, Wydarzenie, Wydarzenie_oddzial, Rodzaj_biletu, Pracownik, Harmonogram_zwiedzania, \
    Bilet, Dzial, Artysta, Obraz, Rzezba

OPTIONS = [("Pracownik", "Pracownik"),
           ("Stażysta", "Stażysta"),
           ("Kierownik", "Kierownik")]


class OddzialForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number'].required = False

    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100"}))

    opening_hour = forms.CharField(widget=forms.TextInput(attrs={"type": "time", "class": "form-control",
                                                                 "id": "opening-hour", "required": "true"}))

    closing_hour = forms.CharField(widget=forms.TextInput(attrs={"type": "time", "class": "form-control",
                                                                 "id": "closing-hour", "required": "true"}))

    address = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "address",
                                                            'maxlength': "100", 'required': 'true'}))

    number = forms.CharField(widget=forms.TextInput(attrs={'type': "text", "class": "form-control", "id": "number"}))


class DzialForm(forms.Form):
    def __init__(self, oddzial_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oddzial_select'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                  choices=oddzial_choices)
        self.fields['epoch'].required = False

    oddzial_select = forms.MultipleChoiceField()

    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100", 'required': 'true'}))

    floor = forms.CharField(widget=forms.TextInput(attrs={'type': "number", "class": "form-control", "id": "floor",
                                                          "min": "-100", "max": "100", 'required': 'true'}))

    epoch = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "epoch",
                                                          'maxlength': "100"}))


class ObrazForm(forms.Form):
    def __init__(self, oddzial_choices, dzial_choices, artysta_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oddzial_select'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                  choices=oddzial_choices)

        self.fields['dzial_select'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                choices=dzial_choices)

        self.fields['artysta_select'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                  choices=artysta_choices)

    oddzial_select = forms.MultipleChoiceField()
    dzial_select = forms.MultipleChoiceField()
    artysta_select = forms.MultipleChoiceField()

    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100"}))

    width = forms.CharField(widget=forms.TextInput(attrs={'type': "number", "class": "form-control", "id": "width",
                                                          "step": "0.01", "min": "0", "max": "1000000",
                                                          "required": "true"}))

    height = forms.CharField(widget=forms.TextInput(attrs={'type': "number", "class": "form-control", "id": "height",
                                                           "step": "0.01", "min": "0", "max": "1000000",
                                                           "required": "true"}))


class RzezbaForm(forms.Form):
    def __init__(self, oddzial_choices, dzial_choices, artysta_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oddzial_select'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                  choices=oddzial_choices)

        self.fields['dzial_select'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                choices=dzial_choices)

        self.fields['artysta_select'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                  choices=artysta_choices)

    oddzial_select = forms.MultipleChoiceField()
    dzial_select = forms.MultipleChoiceField()
    artysta_select = forms.MultipleChoiceField()

    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100"}))

    weight = forms.CharField(widget=forms.TextInput(attrs={'type': "number", "class": "form-control", "id": "weight",
                                                           "step": "0.01", "min": "0", "max": "1000000",
                                                           "required": "true"}))

    material = forms.CharField(widget=forms.TextInput(attrs={'type': "text", "class": "form-control", "id": "material",
                                                             "maxlength": "50", "required": "true"}))


class ArtystaForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "50", "required": "true"}))

    surname = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "surname",
                                                            'maxlength': "50", "required": "true"}))

    birth_date = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                               "id": "birth-date", "required": "true"}))

    death_date = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                               "id": "death-date"}))


class BiletForm(forms.Form):
    def __init__(self, type_choices, oddzial_choices, wycieczka_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                  choices=type_choices)

        self.fields['oddzial'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                choices=oddzial_choices)

        self.fields['wycieczka'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                  choices=wycieczka_choices)

        self.fields['przewodnik'] = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=[("tak", "tak"),("nie", "nie")])

    type = forms.MultipleChoiceField()
    oddzial = forms.MultipleChoiceField()
    wycieczka = forms.MultipleChoiceField()
    przewodnik = forms.ChoiceField()

    purchase_date = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                                  "id": "purchase-date", "required": "true"}))



class RodzajBiletuForm(forms.Form):
    def __init__(self, oddzial_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oddzial'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                  choices=oddzial_choices)
        self.fields['przewodnik'] = forms.ChoiceField(required=True, widget=forms.RadioSelect,
                                                      choices=[("tak", "tak"), ("nie", "nie")])

    oddzial = forms.MultipleChoiceField()
    przewodnik = forms.ChoiceField()
    type = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "type",
                                                         'maxlength': "100", "required": "true"}))

    price = forms.CharField(widget=forms.TextInput(attrs={'type': "number", 'class': "form-control", 'id': "price",
                                                          'min': "0", "max": "1000", "required": "true"}))


class PracownikForm(forms.Form):
    def __init__(self, oddzial_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oddzial'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                  choices=oddzial_choices)
    pesel = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "pesel",
                                                          "minlength": "11", 'maxlength': "11",
                                                          "required": "true"}))

    imie = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "50", "required": "true"}))

    nazwisko = forms.CharField(
        widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "surname",
                                      'maxlength': "50", "required": "true"}))

    etat = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                         choices=OPTIONS)

    placa = forms.CharField(widget=forms.TextInput(attrs={'type': "number", 'class': "form-control", 'id': "placa",
                                                         'min': "0", "max": "1000000", "required": "true"}))

    data_zatrudnienia = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                              "id": "data_zatrudnienia", "placeholder": "dd-mm-yyyy",
                                                              "required": "true"}))

    # TODO oddzial
    numer_telefonu = forms.CharField(widget=forms.TextInput(attrs={'type': "text", "class": "form-control", "id": "numer_telefonu", "required": "false"}))


class HarmonogramZwiedzaniaForm(forms.Form):
    def __init__(self, pracownik_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pesel'] = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                                                  choices=pracownik_choices)
    godzina = forms.CharField(widget=forms.TextInput(attrs={"type": "time", "class": "form-control",
                                                               "id": "godzina", "required": "true"}))

    data = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                         "id": "data", "required": "true"}))




class WydarzenieForm(forms.Form):
    nazwa = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "nazwa",
                                                         'maxlength': "100", "required": "true"}))

    data_rozpoczecia = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                               "id": "data_rozpoczecia", "required": "true"}))

    data_zakonczenia = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                             "id": "data_zakonczenia", "required": "true"}))


class DetailedArtystaForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "50"}))

    surname = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "surname",
                                                            'maxlength': "50"}))

    birth_date = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                               "id": "birth-date"}))

    death_date = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                               "id": "death-date"}))
    # TODO painitngs
    # TODO sculptures


class DetailedDzialForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100"}))

    oddzial = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "branch",
                                                            'maxlength': "100"}))

    floor = forms.CharField(widget=forms.TextInput(attrs={'type': "number", "class": "form-control", "id": "floor",
                                                          "min": "-100", "max": "100"}))

    epoch = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "epoch",
                                                          'maxlength': "100"}))

    paintings = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple, choices=[])
    # TODO painitngs
    # TODO sculptures


class DetailedDzieloForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100"}))

    branch = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "branch",
                                                           'maxlength': "100"}))

    department = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control",
                                                               'id': "department", 'maxlength': "100"}))

    artist = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "artist",
                                                           'maxlength': "100"}))

    width = forms.CharField(widget=forms.TextInput(attrs={'type': "number", "class": "form-control", "id": "width",
                                                          "step": "0.01"}))

    height = forms.CharField(widget=forms.TextInput(attrs={'type': "number", "class": "form-control", "id": "height",
                                                           "step": "0.01"}))

    weight = forms.CharField(widget=forms.TextInput(attrs={'type': "number", "class": "form-control", "id": "weight",
                                                           "step": "0.01", "required": "true"}))

    material = forms.CharField(widget=forms.TextInput(attrs={'type': "text", "class": "form-control", "id": "material",
                                                             "maxlength": "50"}))


class DetailedOddzialForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100", 'required': 'true'}))

    opening_hour = forms.CharField(widget=forms.TextInput(attrs={"type": "time", "class": "form-control",
                                                                 "id": "opening-hour", "required": "true"}))

    closing_hour = forms.CharField(widget=forms.TextInput(attrs={"type": "time", "class": "form-control",
                                                                 "id": "closing-hour", "required": "true"}))

    address = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "address",
                                                            'maxlength': "100", 'required': 'true'}))

    number = forms.CharField(widget=forms.TextInput(attrs={'type': "text", "class": "form-control", "id": "number"}))


class TableArtystaForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Artysta.objects.all(),  # not optional, use .all() if unsure
        widget=forms.CheckboxSelectMultiple,
    )


class TableDzialForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Dzial.objects.all(),  # not optional, use .all() if unsure
        widget=forms.CheckboxSelectMultiple,
    )


class TableOddzialForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Oddzial.objects.all(),  # not optional, use .all() if unsure
        widget=forms.CheckboxSelectMultiple,
    )


class TableDzieloForm(forms.Form):
    choices_obrazy = forms.ModelMultipleChoiceField(
        queryset=Obraz.objects.all(),  # not optional, use .all() if unsure
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    choices_rzezby = forms.ModelMultipleChoiceField(
        queryset=Rzezba.objects.all(),  # not optional, use .all() if unsure
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class TablePracownikForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Pracownik.objects.all(),  # not optional, use .all() if unsure
        widget=forms.CheckboxSelectMultiple,
    )


class TableHarmonogramZwiedzaniaForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Harmonogram_zwiedzania.objects.all(),  # not optional, use .all() if unsure
        widget=forms.CheckboxSelectMultiple,
    )


class TableBiletyForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Bilet.objects.all(),  # not optional, use .all() if unsure
        widget=forms.CheckboxSelectMultiple,
    )


class TableRodzajeBiletowForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Rodzaj_biletu.objects.all(),  # not optional, use .all() if unsure
        widget=forms.CheckboxSelectMultiple,
    )


class TableWydarzeniaForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Wydarzenie.objects.all(),  # not optional, use .all() if unsure
        widget=forms.CheckboxSelectMultiple,
    )


class EditOddzialForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_type = post_type
        self.fields['number'].required = False

    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100"}))

    opening_hour = forms.CharField(widget=forms.TextInput(attrs={"type": "time", "class": "form-control",
                                                                 "id": "opening-hour", "required": "true"}))

    closing_hour = forms.CharField(widget=forms.TextInput(attrs={"type": "time", "class": "form-control",
                                                                 "id": "closing-hour", "required": "true"}))

    address = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "address",
                                                            'maxlength': "100", 'required': 'true'}))

    number = forms.CharField(widget=forms.TextInput(attrs={'type': "text", "class": "form-control", "id": "number"}))
