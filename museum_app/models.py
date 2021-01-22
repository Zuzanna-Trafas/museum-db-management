from django.db import models
#TODO: on_delete
#TODO: missing verboses
#TODO: unique? unique_for_data? Who knows, not me
#TODO: length validators
#TODO: primary keys fix

class Oddzial(models.Model):
        nazwa = models.CharField(max_length=100, primary_key=True)
        godzina_otwarcia = models.TimeField()
        godzina_zamkniecia = models.TimeField(verbose_name="godzina zamknięcia")
        adres = models.CharField(max_length=100)
        numer_telefonu = models.PositiveIntegerField()

class Wydarzenie(models.Model):
    nazwa = models.CharField(max_length=100, primary_key=True)
    data_rozpoczecia = models.DateField(verbose_name="data rozpoczęcia")
    data_zakonczenia = models.DateField(verbose_name="data zakończenia")

class Wydarzenie_oddzial(models.Model):
    oddzial_nazwa = models.OneToOneField(Oddzial, on_delete=models.CASCADE, primary_key=True) 
    wydarzenie_nazwa = models.OneToOneField(Wydarzenie, on_delete=models.CASCADE, related_name='wydarzenie_oddzial_wydarzenie_nazwa')
    wydarzenie_data_rozpoczecia = models.OneToOneField(Wydarzenie, on_delete=models.CASCADE, related_name='wydarzenie_oddzial_wydarzenie_data_rozpoczecia')

class Rodzaj_biletu(models.Model):
    typ = models.CharField(max_length=100, primary_key=True)
    czy_z_przewodnikiem = models.BooleanField()
    cena = models.FloatField()
    oddzial_nazwa = models.OneToOneField(Oddzial, on_delete=models.CASCADE)

class Pracownik(models.Model):
    pesel = models.PositiveIntegerField(primary_key=True)
    imie = models.CharField(max_length=50, verbose_name="imię")
    nazwisko = models.CharField(max_length=50)
    placa = models.PositiveIntegerField(verbose_name="płaca")
    etat = models.CharField(max_length=50)
    data_zatrudnienia = models.DateField()
    numer_telefonu = models.PositiveIntegerField()
    oddzial_nazwa = models.ForeignKey(Oddzial, on_delete=models.CASCADE)

class Harmonogram_zwiedzania(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    godzina_rozpoczecia = models.TimeField(unique=True)
    data = models.DateField(unique=True)
    pracownik_pesel = models.OneToOneField(Pracownik, on_delete=models.CASCADE)

class Bilet(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    data_zakupu = models.DateField()
    rodzaj_biletu_typ = models.ForeignKey(Rodzaj_biletu, related_name='bilet_rodzaj_biletu_typ', on_delete=models.CASCADE)
    rodzaj_biletu_oddzial_nazwa = models.ForeignKey(Rodzaj_biletu, related_name='bilet_rodzaj_biletu_oddzial_nazwa', on_delete=models.CASCADE)
    rodzaj_biletu_czy_z_przewodnikiem = models.ForeignKey(Rodzaj_biletu, related_name='bilet_rodzaj_biletu_czy_z_przewodnikiem', on_delete=models.CASCADE)
    harmonogram_zwiedzania_id = models.ForeignKey(Harmonogram_zwiedzania, on_delete=models.CASCADE)

class Dzial(models.Model):
    nazwa = models.CharField(max_length=100, primary_key=True)
    pietro = models.PositiveIntegerField(verbose_name="piętro")
    epoka = models.CharField(max_length=100)
    oddzial_nazwa = models.OneToOneField(Oddzial, on_delete=models.CASCADE)

class Artysta(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    imie = models.CharField(max_length=50, verbose_name="imię")
    nazwisko = models.CharField(max_length=50)
    data_urodzenia = models.DateField()
    data_śmierci = models.DateField(verbose_name="data śmierci")

class Obraz(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=100)
    szerokosc = models.FloatField(verbose_name="szerokość")
    wysokosc = models.FloatField(verbose_name="wysokość")
    artysta_id = models.ForeignKey(Artysta, on_delete=models.CASCADE)
    dzial_nazwa = models.ForeignKey(Dzial, on_delete=models.CASCADE, related_name='obraz_dzial_nazwa')
    dzial_oddzial_nazwa = models.ForeignKey(Dzial, on_delete=models.CASCADE, related_name='obraz_dzial_oddzial_nazwa')
    
class Rzezba(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=100)
    waga = models.FloatField()
    material = models.CharField(max_length=50, verbose_name="materiał")
    artysta_id = models.ForeignKey(Artysta, on_delete=models.CASCADE)
    dzial_nazwa = models.ForeignKey(Dzial, on_delete=models.CASCADE, related_name='rzezba_dzial_nazwa')
    dzial_oddzial_nazwa = models.ForeignKey(Dzial, on_delete=models.CASCADE, related_name='rzezba_dzial_oddzial_nazwa')
    


