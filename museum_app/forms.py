from django import forms

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
    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100", 'required': 'true'}))
    # TODO oddzial
    oddzial_select = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple,
                                               choices=OPTIONS)

    floor = forms.CharField(widget=forms.TextInput(attrs={'type': "number", "class": "form-control", "id": "floor",
                                                          "min": "-100", "max": "100"}))

    epoch = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "epoch",
                                                          'maxlength': "100"}))


class ObrazForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "name",
                                                         'maxlength': "100"}))

    # TODO oddzial
    # TODO dzial
    # TODO artysta

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
