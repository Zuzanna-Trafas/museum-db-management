from django.db import models


# TODO: on_delete
# TODO: missing verboses
# TODO: unique? unique_for_data? Who knows, not me
# TODO: length validators

class Oddzial(models.Model):
    nazwa = models.CharField(max_length=100, primary_key=True)
    godzina_otwarcia = models.TimeField()
    godzina_zamkniecia = models.TimeField(verbose_name="godzina zamknięcia")
    adres = models.CharField(max_length=100)
    numer_telefonu = models.CharField(max_length=20)


class Wydarzenie(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=100)
    data_rozpoczecia = models.DateField(verbose_name="data rozpoczęcia")
    data_zakonczenia = models.DateField(verbose_name="data zakończenia")

    class Meta:
        unique_together = (("nazwa", "data_rozpoczecia"),)


class Wydarzenie_oddzial(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    oddzial_nazwa = models.ForeignKey(Oddzial, on_delete=models.PROTECT)
    wydarzenie_id = models.ForeignKey(Wydarzenie, on_delete=models.CASCADE,
                                      related_name='wydarzenie_oddzial_wydarzenie_id')

    class Meta:
        unique_together = (("oddzial_nazwa", "wydarzenie_id"),)


class Rodzaj_biletu(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    typ = models.CharField(max_length=100)
    czy_z_przewodnikiem = models.BooleanField()
    cena = models.FloatField()
    oddzial_nazwa = models.ForeignKey(Oddzial, on_delete=models.PROTECT)

    class Meta:
        unique_together = (("typ", "czy_z_przewodnikiem", "oddzial_nazwa"),)


class Pracownik(models.Model):
    pesel = models.PositiveIntegerField(primary_key=True)
    imie = models.CharField(max_length=50, verbose_name="imię")
    nazwisko = models.CharField(max_length=50)
    placa = models.PositiveIntegerField(verbose_name="płaca")
    etat = models.CharField(max_length=50)
    data_zatrudnienia = models.DateField()
    numer_telefonu = models.CharField(max_length=20)
    oddzial_nazwa = models.ForeignKey(Oddzial, on_delete=models.PROTECT)


class Harmonogram_zwiedzania(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    godzina_rozpoczecia = models.TimeField()
    data = models.DateField()
    pracownik_pesel = models.ForeignKey(Pracownik, on_delete=models.PROTECT)

    class Meta:
        unique_together = (("godzina_rozpoczecia", "data", "pracownik_pesel"),)


class Bilet(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    data_zakupu = models.DateField()
    rodzaj_biletu_id = models.ForeignKey(Rodzaj_biletu, related_name='bilet_rodzaj_biletu_id',
                                         on_delete=models.PROTECT)
    harmonogram_zwiedzania_id = models.ForeignKey(Harmonogram_zwiedzania, on_delete=models.PROTECT)


class Dzial(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=100)
    pietro = models.PositiveIntegerField(verbose_name="piętro")
    epoka = models.CharField(max_length=100)
    oddzial_nazwa = models.ForeignKey(Oddzial, on_delete=models.PROTECT)

    class Meta:
        unique_together = (("nazwa", "oddzial_nazwa"),)


class Artysta(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    imie = models.CharField(max_length=50, verbose_name="imię")
    nazwisko = models.CharField(max_length=50)
    data_urodzenia = models.DateField()
    data_smierci = models.DateField(verbose_name="data śmierci")


class Obraz(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=100)
    szerokosc = models.FloatField(verbose_name="szerokość")
    wysokosc = models.FloatField(verbose_name="wysokość")
    artysta_id = models.ForeignKey(Artysta, on_delete=models.PROTECT)
    dzial_id = models.ForeignKey(Dzial, on_delete=models.PROTECT, related_name='obraz_dzial_id')


class Rzezba(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=100)
    waga = models.FloatField()
    material = models.CharField(max_length=50, verbose_name="materiał")
    artysta_id = models.ForeignKey(Artysta, on_delete=models.PROTECT)
    dzial_id = models.ForeignKey(Dzial, on_delete=models.PROTECT, related_name='rzezba_dzial_id')
