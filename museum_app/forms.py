from django import forms
from museum_app.models import Oddzial, Wydarzenie, Wydarzenie_oddzial, Rodzaj_biletu, Pracownik, Harmonogram_zwiedzania, \
    Bilet, Dzial, Artysta, Obraz, Rzezba

OPTIONS = [("Pracownik", "Pracownik"),
           ("Stażysta", "Stażysta"),
           ("Kierownik", "Kierownik")]


class OddzialForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100", 'required': 'true'}))

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
    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100"}))

    # TODO oddzial
    # TODO dzial
    # TODO artysta

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
    purchase_date = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                                  "id": "purchase-date", "required": "true"}))

    birth_date = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                               "id": "birth-date", "required": "true"}))

    # TODO type
    # TODO oddzial
    # TODO guide
    # TODO tour


class RodzajBiletuForm(forms.Form):
    type = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "type",
                                                         'maxlength': "100", "required": "true"}))

    price = forms.CharField(widget=forms.TextInput(attrs={'type': "number", 'class': "form-control", 'id': "price",
                                                          'min': "0", "max": "1000", "required": "true"}))

    # TODO oddzal
    # TODO guide


class PracownikForm(forms.Form):
    pesel = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "pesel",
                                                          "minlength": "11", 'maxlength': "11",
                                                          "required": "true"}))

    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "50", "required": "true"}))

    surname = forms.CharField(
        widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "surname",
                                      'maxlength': "50", "required": "true"}))

    position = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                         choices=OPTIONS)

    wage = forms.CharField(widget=forms.TextInput(attrs={'type': "number", 'class': "form-control", 'id': "wage",
                                                         'min': "0", "max": "1000000", "required": "true"}))

    join_date = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                              "id": "join-date", "placeholder": "dd-mm-yyyy",
                                                              "required": "true"}))

    # TODO oddzial
    number = forms.CharField(widget=forms.TextInput(attrs={'type': "text", "class": "form-control", "id": "number"}))


class HarmonogramZwiedzaniaForm(forms.Form):
    start_hour = forms.CharField(widget=forms.TextInput(attrs={"type": "time", "class": "form-control",
                                                               "id": "start-hour", "required": "true"}))

    date = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                         "id": "date", "required": "true"}))

    # TODO pesel


class WydarzenieForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100", "required": "true"}))

    start_date = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                               "id": "start-date", "required": "true"}))

    end_date = forms.CharField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",
                                                             "id": "end-date", "required": "true"}))


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
