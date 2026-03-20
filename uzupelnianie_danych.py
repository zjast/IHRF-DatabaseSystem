import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, text, ForeignKey
from sqlalchemy.orm import sessionmaker
import random
from sqlalchemy.orm import declarative_base,relationship
from faker import Faker
from urllib.parse import quote_plus
from datetime import date,timedelta
from typing import Any

Base = declarative_base()

faker=Faker("pl_PL")
faker2=Faker("de_DE")
faker3=Faker("fr_FR")
faker4=Faker("it_IT")
faker5=Faker("zh_CN")  
faker6=Faker("cs_CZ")
faker7=Faker("en_US")
faker8=Faker("hu_HU")
faker9=Faker("pt_BR")
faker10=Faker("en_AU")
#tyle odmian językowych ile krajów w tabeli państwa umożliwi generowanie losowych miast dla każdego kraju

class Panstwa(Base):
    __tablename__ = 'panstwa'
    id_panstwa = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    panstwo = sa.Column(sa.VARCHAR(40))
    miasta = relationship("Miasta", back_populates="panstwo")
    
class Miasta(Base):
    __tablename__ = "miasta"
    id_miasta = Column(Integer, primary_key=True, autoincrement=True)
    miasto = Column(String(50), nullable=False)
    id_panstwa = Column(Integer, ForeignKey("panstwa.id_panstwa"), nullable=False)
    kod_pocztowy = sa.Column(sa.VARCHAR(10))
    panstwo = relationship("Panstwa", back_populates="miasta")
    miasta2 = relationship("Zawody", back_populates="zawody")

class Sponsorzy(Base):
    __tablename__ = 'sponsorzy'
    id_sponsora = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    nazwa_firmy = sa.Column(sa.VARCHAR(40), nullable=False)
    oferta = sa.Column(sa.TEXT)
    nr_tel_reprezentanta = sa.Column(sa.INTEGER, nullable=False)
    data_podpisania_umowy = sa.Column(sa.DATE, default=sa.func.current_date())
    data_zakonczenia_umowy = sa.Column(sa.DATE, nullable=True)
    sponsor=relationship("Finansowanie", back_populates="finansowanie1")
    sponsor_sportowcy=relationship("Sportowcy_Sponsorzy", back_populates="sponsor2")

class Finansowanie(Base):
    __tablename__="finansowanie"
    id_transakcji = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True) 
    id_sponsora = sa.Column(sa.INTEGER, sa.ForeignKey("sponsorzy.id_sponsora", onupdate="CASCADE"))
    zrodlo=sa.Column(sa.VARCHAR(40))
    data_transakcji=sa.Column(sa.DATE)
    kwota=sa.Column(sa.INTEGER)
    id_pracownika=sa.Column(sa.INTEGER,sa.ForeignKey("pracownicy.id_pracownika", onupdate="CASCADE"))
    finansowanie1=relationship("Sponsorzy", back_populates="sponsor")
    finansowanie2=relationship("Pracownicy", back_populates="pracownik")

class Wlasciciele(Base):
    __tablename__="sportowcy_wlasciciele"
    id_wlasciciela = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    imie = sa.Column(sa.VARCHAR(40))
    nazwisko = sa.Column(sa.VARCHAR(40))
    sportowcy=relationship("Sportowcy", back_populates="wlasciciel")

class Sportowcy(Base):
    __tablename__ = 'sportowcy'
    id_uczestnika = sa.Column(sa.INTEGER, primary_key=True)
    id_wlasciciela = sa.Column(sa.INTEGER, sa.ForeignKey("sportowcy_wlasciciele.id_wlasciciela"))
    charakterystyka = sa.Column(sa.TEXT)
    data_urodzenia = sa.Column(sa.DATE)# default=sa.func.current_date())
    wartosc_wyposazenia=sa.Column(sa.INTEGER, default=0, comment="Cena sprzętu")
    aktywny = sa.Column(sa.BOOLEAN)
    wlasciciel=relationship("Wlasciciele", back_populates="sportowcy")
    sponsorzy_sportowcy=relationship("Sportowcy_Sponsorzy", back_populates="sportowiec")
    zawody_uczestnicy = relationship("Zawody_Uczestnicy", back_populates="sportowiec")
    wyniki_konkurencji = relationship("Konkurencje_Uczestnicy", back_populates="sportowiec")
    dyskwalifikacja = relationship("Zdyskwalifikowani", back_populates="sportowiec")


class Sportowcy_Sponsorzy(Base):
    __tablename__="sportowcy_sponsorzy"
    id_uczestnika = sa.Column(sa.INTEGER, sa.ForeignKey("sportowcy.id_uczestnika", onupdate="CASCADE"),nullable=False)
    id_sponsora = sa.Column(sa.INTEGER, sa.ForeignKey("sponsorzy.id_sponsora", onupdate="CASCADE"))
    kwota = sa.Column(sa.INTEGER)
    data_transakcji = sa.Column(sa.DATE,nullable=False)
    __table_args__ = (
        sa.PrimaryKeyConstraint('id_uczestnika', 'data_transakcji'),)
    sportowiec= relationship("Sportowcy", back_populates="sponsorzy_sportowcy")
    sponsor2= relationship("Sponsorzy", back_populates="sponsor_sportowcy")

class Zawody(Base):
    __tablename__="zawody"
    id_zawodow = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True) 
    data_zawodow = sa.Column(sa.DATE)
    id_miasta = sa.Column(sa.INTEGER, sa.ForeignKey("miasta.id_miasta"), nullable=False)
    liczba_widzow=sa.Column(sa.INTEGER, default=0)
    przychod=sa.Column(sa.INTEGER, default=0)
    koszt_organizacji=sa.Column(sa.INTEGER, default=0)
    zawody=relationship("Miasta", back_populates="miasta2")
    uczestnicy = relationship("Zawody_Uczestnicy", back_populates="zawody")
    konkurencje_zawodow = relationship("Konkurencje_Zawody", back_populates="zawody")

class Zawody_Uczestnicy(Base):
    __tablename__="zawody_uczestnicy"
    id_uczestnika = sa.Column(sa.Integer, sa.ForeignKey('sportowcy.id_uczestnika'), primary_key=True)
    id_zawodow = sa.Column(sa.Integer, sa.ForeignKey('zawody.id_zawodow'), primary_key=True)
    sportowiec = relationship("Sportowcy", back_populates="zawody_uczestnicy")
    zawody = relationship("Zawody", back_populates="uczestnicy")

class Kontrola_antydopingowa(Base):
    __tablename__ = 'kontrole_antydopingowe'
    id_kontroli = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    id_uczestnika = sa.Column(sa.Integer, sa.ForeignKey('sportowcy.id_uczestnika'))
    data_kontroli = sa.Column(sa.Date)
    wynik_kontroli = sa.Column(sa.VARCHAR(10))
    dyskwalifikacja = relationship("Zdyskwalifikowani", back_populates="kontrola")

class Zdyskwalifikowani(Base):
    __tablename__ = 'zdyskwalifikowani'
    id_uczestnika = sa.Column(sa.Integer, sa.ForeignKey('sportowcy.id_uczestnika'), primary_key=True)
    id_kontroli = sa.Column(sa.Integer, sa.ForeignKey('kontrole_antydopingowe.id_kontroli'), primary_key=True)
    substancja = sa.Column(sa.VARCHAR(40))
    sportowiec = relationship("Sportowcy", back_populates="dyskwalifikacja")
    kontrola = relationship("Kontrola_antydopingowa", back_populates="dyskwalifikacja")

class Kategorie(Base):
    __tablename__ = 'kategorie'
    id_kategorii = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    nazwa_kategorii = sa.Column(sa.VARCHAR(50), nullable=False)
    czy_wymaga_sprzetu = sa.Column(sa.Boolean, default=False, nullable=False)
    konkurencje = relationship("Konkurencje", back_populates="kategoria")

class Konkurencje(Base):
    __tablename__ = 'konkurencje'
    id_konkurencji = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    nazwa_konkurencji = sa.Column(sa.VARCHAR(100))
    opis = sa.Column(sa.Text)
    id_kategorii = sa.Column(sa.Integer, sa.ForeignKey('kategorie.id_kategorii'))
    kategoria = relationship("Kategorie", back_populates="konkurencje")
    wyniki = relationship("Konkurencje_uczestnicy", back_populates="konkurencja")

class Konkurencje_Zawody(Base):
    __tablename__ = 'konkurencje_zawody'
    id_konkurencji = sa.Column(sa.Integer, sa.ForeignKey('konkurencje.id_konkurencji'), primary_key=True)
    id_zawodow = sa.Column(sa.Integer, sa.ForeignKey('zawody.id_zawodow'), primary_key=True)
    zwyciezca_konkurencji = sa.Column(sa.Integer, sa.ForeignKey('sportowcy.id_uczestnika'))
    zawody = relationship("Zawody", back_populates="konkurencje_zawodow")

class Konkurencje_Uczestnicy(Base):
    __tablename__ = 'konkurencje_uczestnicy'
    id_konkurencji = sa.Column(sa.Integer, sa.ForeignKey('konkurencje.id_konkurencji'), primary_key=True)
    id_uczestnika = sa.Column(sa.Integer, sa.ForeignKey('sportowcy.id_uczestnika'), primary_key=True)
    wynik_uczestnika = sa.Column(sa.Integer)
    konkurencja = relationship("Konkurencje", back_populates="wyniki")
    sportowiec = relationship("Sportowcy", back_populates="wyniki_konkurencji")

class Pracownicy(Base):
    __tablename__="pracownicy"
    id_pracownika = sa.Column(sa.INTEGER, primary_key = True, autoincrement = True) 
    imie = sa.Column(sa.VARCHAR(40))
    nazwisko = sa.Column(sa.VARCHAR(40))
    nr_telefonu = sa.Column(sa.String(30), nullable = True)
    ulica = sa.Column(sa.VARCHAR(30), nullable = False)
    nr_domu = sa.Column(sa.String(10), nullable = True)
    nr_mieszkania = sa.Column(sa.INTEGER, nullable = True)
    id_miasta = sa.Column(sa.INTEGER, sa.ForeignKey("miasta.id_miasta", onupdate="CASCADE"), nullable = False)
    data_zatrudnienia = sa.Column(sa.DATE, nullable = False)
    data_zwolnienia = sa.Column(sa.DATE, nullable = True)
    wynagrodzenie = sa.Column(sa.INTEGER, nullable = True)
    pracownik=relationship("Finansowanie", back_populates="finansowanie2")
    miasto = relationship("Miasta")



def generowanie_oferty():
    kwota=["100", "200", "300", "400", "500","600", "700", "800", "900", "1000"]
    bonusy=["dodatkowy sprzęt treningowy", "darmowe konsultacje z trenerem","darmowe wizyty u weterynarza", "udział w konferencjach sportowych","wyjazdy do SPA"]
    return f"Oferujemy wsparcie finansowe w wysokości {random.choice(kwota)}zł miesięcznie oraz dodatkowe bonusy, np. {random.choice(bonusy)}."


def generowanie_opisu():
    cechy = ["szybki", "zwinny", "silny", "wytrwały", "agresywny", "spokojny", "pomysłowy", "przebiegły","inteligenty"]
    umiejetnosci = ["skoki", "biegi", "spinacz", "prowadzenie pojazdu przez bieganie w kołowrotku", "skoki przez przeszkody"]
    preferencje = ["startuje w kategori naturalnej", "startuje w kategori formuła Ch"]
    description = f"Chomik jest {random.choice(cechy)}, {random.choice(cechy)}, specjalizuje się w kategori {random.choice(umiejetnosci)} oraz {random.choice(preferencje)}."
    return description


def odpowiednia_dlugosc():
    while True:
        name = faker.company()
        if len(name) <= 40:
            return name


def data_zawodow():
    if random.random() < 0.2:
        return faker.date_between(start_date="-1y", end_date="today")
    else:
        return faker.date_between(start_date="-5y", end_date="-1y")
    
    
def aktywny_status(data_uro):
    wiek = date.today().year - data_uro.year
    return wiek <  3


def data_zakonczenia_umowy(data_podpisania):
    if random.random() < 0.3:
        return faker.date_between(start_date=data_podpisania, end_date="today")
    else:
        return None
    

def kwota_sponsoringu(x):
    liczba = ""
    for znak in x:
        if znak.isdigit():
            liczba+=znak
    return int(liczba)


def okres_aktywnosci(data_uro):
    start=data_uro
    koniec=data_uro+timedelta(days=3*365)
    return start, koniec

def daty_sponsoringu(sportowiec,n):
    poczatek,koniec = okres_aktywnosci(sportowiec.data_urodzenia)
    daty = set()
    while len(daty) < n:
        nowa_data = faker.date_between(start_date=poczatek, end_date=koniec)
        daty.add(nowa_data)
    return list(daty)


def usuwanie(session, usun: bool, klasa: Any, nazwa: str):
    """usuwanie danych z tabeli"""
    
    if not usun: 
        return
    
    session.execute(text("SET FOREIGN_KEY_CHECKS= 0"))
    session.query(klasa).delete()
    session.execute(text(f"ALTER TABLE {nazwa} AUTO_INCREMENT = 1"))
    session.execute(text("SET FOREIGN_KEY_CHECKS= 1"))


def stworz_panstwa_miasta(session, kraje, miasta, kody_pocztowe, usun: bool = False):
    usuwanie(session, usun, Panstwa, "panstwa")
    usuwanie(session, usun, Miasta, "miasta")
    dane_panstwa = [Panstwa(panstwo=kraj) for kraj in kraje]

    panstwa_wszystkie = session.query(Panstwa).all()
   
    dane_miasta = []
    for kraj in panstwa_wszystkie:
        for miasto in random.sample(miasta[kraj.panstwo], random.randint(1, 10)):
            dane_miasta.append(
                Miasta(
                    miasto=miasto,
                    kod_pocztowy=random.choice(kody_pocztowe[kraj.panstwo]),
                    id_panstwa=kraj.id_panstwa
            )
        )
            
    if session.query(Panstwa).first() is None:
        session.add_all(dane_panstwa)
        session.commit()
    else:
         print("Dane już istnieją w tabeli.")
    
    if session.query(Miasta).first() is None:
        session.add_all(dane_miasta)
        session.commit()
    else:
         print("Dane już istnieją w tabeli.")  


def stworz_wlascicieli(session, usun: bool = False):
    
    usuwanie(session, usun, Wlasciciele, "sportowcy_wlasciciele")

    dane_wlasciciele = []
    for _ in range(100):
        dane_wlasciciele.append(Wlasciciele(
            imie=faker.first_name(),
            nazwisko=faker.last_name()  
        ))
        
    if usun or session.query(Wlasciciele).first() is None:
        session.add_all(dane_wlasciciele)
        session.commit()
    else:
         print("Dane już istnieją w tabeli.")  
    
    
def stworz_sponsorow(session, usun: bool = False):

    usuwanie(session, usun, Sponsorzy, "sponsorzy")

    dane_sponsorzy = []
    for _ in range(35):
        podpisanie_umowy=faker.date_between(start_date="-5y",end_date="today")
        dane_sponsorzy.append(  
            Sponsorzy(
                nazwa_firmy=odpowiednia_dlugosc(),
                oferta=generowanie_oferty(),
                data_podpisania_umowy=podpisanie_umowy,
                data_zakonczenia_umowy=data_zakonczenia_umowy(podpisanie_umowy),
                nr_tel_reprezentanta=faker.random_number(digits=9, fix_len=True)
            ))

    if usun or session.query(Sponsorzy).first() is None:
        session.add_all(dane_sponsorzy)
        session.commit()
    else:
         print("Dane już istnieją w tabeli.")


def stworz_sportowcow(session, usun: bool = False):
    
    usuwanie(session, usun, Sportowcy, "sportowcy")
    wlasciciele_db=session.query(Wlasciciele).all()
    dane_sportowcy = []
    for _ in range(100):
        data_uro = faker.date_between(start_date="-5y", end_date="today")
        aktywny_status1=aktywny_status(data_uro)
        dane_sportowcy.append( Sportowcy(
            id_wlasciciela=random.choice(wlasciciele_db).id_wlasciciela,
            charakterystyka=generowanie_opisu(),
            data_urodzenia=data_uro,
            wartosc_wyposazenia=random.randint(500,5000),
            aktywny=aktywny_status1
        ))
    
    if usun or session.query(Sportowcy).first() is None:
        session.add_all(dane_sportowcy)
        session.commit()
    else:
         print("Dane już istnieją w tabeli.")


def stworz_zawody(session, miasta, usun: bool = False):
    
    usuwanie(session, usun, Zawody, "zawody")

    dane_zawody = [
        Zawody(
            data_zawodow=data_zawodow(),
            id_miasta=random.choice(miasta).id_miasta,
            liczba_widzow=random.randint(1000,10000),
            przychod=random.randint(5000,50000),
            koszt_organizacji=random.randint(2000,10000),
            )for _ in range(100)]
    random.shuffle(dane_zawody)
    
    if usun or session.query(Zawody).first() is None:
        session.add_all(dane_zawody)
        session.commit()
    else:
         print("Dane już istnieją w tabeli.")

    
def stworz_sportowcow_sponsorow(session, sportowcy, sponsorzy, usun: bool = False):
    usuwanie(session, usun, Sportowcy_Sponsorzy, "sportowcy_sponsorzy")

    dane_sponsorzy_sportowcy = []
    for uczestnik in sportowcy:
        wybrany_sponsor = random.choice(sponsorzy)
        n=random.randint(1,10)
        daty = daty_sponsoringu(uczestnik, n)
        for data in daty:
            kwota = kwota_sponsoringu(wybrany_sponsor.oferta)
            dane_sponsorzy_sportowcy.append(
                Sportowcy_Sponsorzy(
                    id_uczestnika=uczestnik.id_uczestnika,
                    id_sponsora=wybrany_sponsor.id_sponsora,
                    kwota=kwota,
                    data_transakcji=data
                )
            )

    if usun or session.query(Sportowcy_Sponsorzy).first() is None:
        session.add_all(dane_sponsorzy_sportowcy)
        session.commit()
    else:
         print("Dane już istnieją w tabeli.")


def stworz_pracownikow(session, usun: bool = False):
    
    usuwanie(session, usun, Pracownicy, "pracownicy")
    
    liczba_pracownikow = random.randint(3,100)
    liczba_zwolnionych = int(liczba_pracownikow * 0.3)
    indeks_zwolnionego = random.sample(range(liczba_pracownikow), liczba_zwolnionych)
    miasta_db = session.query(Miasta).all()
    dane_pracownicy = []

    for i in range(liczba_pracownikow):
        
        if i in indeks_zwolnionego:
            data_zwolnienia = faker.date_between(start_date = "-5y")
            data_zatrudnienia = faker.date_between(start_date = "-5y", end_date = data_zwolnienia)
            wynagrodzenie = None
        else: 
            data_zwolnienia = None
            data_zatrudnienia = faker.date_between(start_date = "-5y")
            wynagrodzenie = random.randint(4800,10000)

        nr_domu = faker.building_number().split('/')[0]
        # pracownik mieszka w domu
        if random.random() < 0.3:
            nr_mieszkania = None
        #pracownik mieszka w mieszkaniu
        else:
            nr_mieszkania = random.randint(1,80)   
        
        pracownik = Pracownicy(
            imie = faker.first_name(),
            nazwisko = faker.last_name(),
            nr_telefonu = faker.phone_number(),
            ulica = faker.street_name(),
            nr_domu = nr_domu,
            nr_mieszkania = nr_mieszkania,
            miasto = random.choice(miasta_db),
            data_zatrudnienia =  data_zatrudnienia,
            data_zwolnienia = data_zwolnienia,
            wynagrodzenie = wynagrodzenie
        )
        dane_pracownicy.append(pracownik)

    if session.query(Pracownicy).first() is None:
        session.add_all(dane_pracownicy)
        session.commit()
    else:
         print("Dane już istnieją w tabeli.")
         
         
def stworz_finansowanie(session, sponsorzy, pracownicy, usun: bool = False):
    
    usuwanie(session, usun, Finansowanie, "finansowanie")

    dane_finansowanie=[ Finansowanie(
        id_sponsora=random.choice(sponsorzy).id_sponsora,
        zrodlo=odpowiednia_dlugosc(),
        data_transakcji=faker.date_between(start_date="-5y"),
        kwota=random.choice([1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]),
        id_pracownika = random.choice(pracownicy).id_pracownika
    ) for _ in range(100)]
    
    if session.query(Finansowanie).first() is None:
        session.add_all(dane_finansowanie)
        session.commit()
    else:
         print("Dane już istnieją w tabeli.")


def stworz_uczestnikow_zawodow(session, zawody, sportowcy, usun: bool = False):
    
    usuwanie(session, usun, Zawody_Uczestnicy, "zawody_uczestnicy")

    dane_uczestnicy=[]

    for konkurs in zawody:
        ilosc_startujacych = random.randint(10,30)
        kandydaci = random.sample(sportowcy, min(ilosc_startujacych, len(sportowcy)))

        for kandydat in kandydaci:
            data_urodzenia, koniec_kariery = okres_aktywnosci(kandydat.data_urodzenia)
            poczatek_startow = data_urodzenia + timedelta(days=90)
            if poczatek_startow <= konkurs.data_zawodow <= koniec_kariery:
                dane_uczestnicy.append(Zawody_Uczestnicy(
                    id_uczestnika = kandydat.id_uczestnika,
                    id_zawodow = konkurs.id_zawodow
                    )
                )
    
    if session.query(Zawody_Uczestnicy).first() is None:
        session.add_all(dane_uczestnicy)
        session.commit()
    else:
         print("Dane już istnieją w tabeli.")


def stworz_kategorie(session, usun: bool = False):

    usuwanie(session, usun, Kategorie, "kategorie")

    lista_kategorii = [
        {"nazwa": "Naturalna", "sprzet": False},
        {"nazwa": "Formuła Ch", "sprzet": True}
    ]

    dane_kategorie = [
            Kategorie(
                nazwa_kategorii = kategoria["nazwa"],
                czy_wymaga_sprzetu = kategoria["sprzet"])
                for kategoria in lista_kategorii
    ]

    if session.query(Kategorie).first() is None:
        session.add_all(dane_kategorie)
        session.commit()
    else:
        print("Dane juz istnieją w tabeli")

def stworz_konkurencje(session, kategorie, usun: bool = False):

    usuwanie(session, usun, Konkurencje, "konkurencje")

    kategoria_nat = session.query(Kategorie).filter_by(nazwa_kategorii = "Naturalna").first()
    kategoria_ch = session.query(Kategorie).filter_by(nazwa_kategorii = "Formuła Ch").first()
    id_nat = kategoria_nat.id_kategorii
    id_ch = kategoria_ch.id_kategorii

    dane_konkurencje = [
        # Naturalne
        Konkurencje(nazwa_konkurencji = "Maraton", opis = "Wyścig długodystansowy w kuli na dystansie 42,195 metra.", id_kategorii=id_nat),
        Konkurencje(nazwa_konkurencji = "Sprint", opis = "Szybki bieg w kołowrotku na 20 obrotów.", id_kategorii=id_nat),
        Konkurencje(nazwa_konkurencji = "Labirynt", opis = "Znalezienie wyjścia z nieznanego labiryntu na czas.", id_kategorii=id_nat),
        Konkurencje(nazwa_konkurencji = "Bieg z przeszkodami", opis = "Wyścig na trasie długości 5 metrów z przeszkodami.", id_kategorii=id_nat),
        Konkurencje(nazwa_konkurencji = "Skok w dal", opis = "Konkurs na najdłuższy skok do papierowej ściółki.", id_kategorii=id_nat),      
        Konkurencje(nazwa_konkurencji = "Bieg z obciążeniem", opis = "Sprint na 3 metry z policzkami pełnymi karmy.", id_kategorii=id_nat),
        Konkurencje(nazwa_konkurencji = "Limbo", opis = "Przechodzenie pod coraz niżej zawieszoną poprzeczką.", id_kategorii=id_nat),
        # Formuła Ch
        Konkurencje(nazwa_konkurencji = "Wyścig - Formuła Ch", opis = "Wyścig o dystansie 15 okrążeń w autkach napędzanych kołowrotkiem", id_kategorii=id_ch),
        Konkurencje(nazwa_konkurencji = "Wyścig wytrzymałościowy - Formuła Ch", opis = "Jazda w autku na czas - kto wytrzyma najdłużej.", id_kategorii=id_ch),
        Konkurencje(nazwa_konkurencji="Drag Race - Formuła Ch", opis="Wyścig par na przyspieszenie w autkach.", id_kategorii=id_ch)
    ]

    if session.query(Konkurencje).first() is None:
        session.add_all(dane_konkurencje)
        session.commit()
    else:
        print("Dane juz istnieją w tabeli")


def stworz_kontrole_antydopingowe(session, sportowcy, usun: bool = False):

    usuwanie(session, usun, Kontrola_antydopingowa, "kontrole_antydopingowe")

    dane_kontrole = []

    for _ in range(100):
            uczestnik = random.choice(sportowcy)
            data_urodzenia, koniec_kariery = okres_aktywnosci(uczestnik.data_urodzenia)
            
            start_date_kontrola = data_urodzenia + timedelta(days=90)

            if start_date_kontrola > date.today():
                continue
                
            end_date_kontrola = min(date.today(), koniec_kariery)

            if start_date_kontrola <= end_date_kontrola:
                wynik = random.choices(["pozytywny", "negatywny"], weights=[20, 80])[0]
                dane_kontrole.append(Kontrola_antydopingowa(
                    id_uczestnika = uczestnik.id_uczestnika,
                    data_kontroli = faker.date_between(start_date=start_date_kontrola, end_date=end_date_kontrola),
                    wynik_kontroli = wynik
                ))

    if session.query(Kontrola_antydopingowa).first() is None:
        session.add_all(dane_kontrole)
        session.commit()
    else:
        print("Dane juz istnieją w tabeli")


def stworz_dyskwalifikacje(session, sportowcy, usun: bool = False):

    usuwanie(session, usun, Zdyskwalifikowani, "zdyskwalifikowani")

    pozytywne_kontrole = session.query(Kontrola_antydopingowa).filter_by(wynik_kontroli='pozytywny').all()
    substancje = ["Kofeina", "Cukier", "Inne słodziki", "Sterydy", "Ingerencja właściciela"]

    dane_dyskwalifikacje = []

    for kontrola in pozytywne_kontrole:

        dane_dyskwalifikacje.append(Zdyskwalifikowani(
            id_uczestnika = kontrola.id_uczestnika,
            id_kontroli = kontrola.id_kontroli,
            substancja = random.choice(substancje)
            )
        )
    if session.query(Zdyskwalifikowani).first() is None:
        session.add_all(dane_dyskwalifikacje)
        session.commit()
    else:
        print("Dane juz istnieją w tabeli")


def stworz_uczestnikow_konkurencji(session, konkurencje, sportowcy, usun: bool = False):

    usuwanie(session, usun, Konkurencje_Uczestnicy, "konkurencje_uczestnicy")

    dane_wyniki = []

    if konkurencje and sportowcy:
        for sportowiec in sportowcy:
            liczba_startow = random.randint(1, 3)
            wybrane_konkurencje = random.sample(konkurencje, min(liczba_startow, len(konkurencje)))
            for konkurencja in wybrane_konkurencje:
                wynik = random.randint(50, 500)
                uz = Konkurencje_Uczestnicy(
                    id_konkurencji = konkurencja.id_konkurencji,
                    id_uczestnika = sportowiec.id_uczestnika,
                    wynik_uczestnika = wynik
                )
                dane_wyniki.append(uz)

    if session.query(Konkurencje_Uczestnicy).first() is None:
        session.add_all(dane_wyniki)
        session.commit()
    else:
        print("Dane juz istnieją w tabeli")


def stworz_konkurencje_zawody(session, zawody_lista, konkurencje_lista, usun: bool = False):

    usuwanie(session, usun, Konkurencje_Zawody, "konkurencje_zawody")

    dane_konkurencje_zawody = []

    for zawody in zawody_lista:
        sample_size = min(random.randint(3, 7), len(konkurencje_lista))
        konkurencje = random.sample(konkurencje_lista, sample_size)

        uczestnicy = session.query(Zawody_Uczestnicy).filter_by(id_zawodow = zawody.id_zawodow).all()
        uczestnicy_id = [u.id_uczestnika for u in uczestnicy]
        
        if uczestnicy_id:
            for kon in konkurencje:
                zwyciezca = random.choice(uczestnicy_id)
                k = Konkurencje_Zawody(
                    id_konkurencji = kon.id_konkurencji,
                    id_zawodow = zawody.id_zawodow,
                    zwyciezca_konkurencji = zwyciezca
                )
                dane_konkurencje_zawody.append(k)

    if session.query(Konkurencje_Zawody).first() is None:
        session.add_all(dane_konkurencje_zawody)
        session.commit()
    else:
        print("Dane juz istnieją w tabeli")
    

def main():
    
    host=host
    user=user
    database=database
    port=port
    password = quote_plus(password)
    engine = sa.create_engine(
        f"mariadb+pymysql://{user}:{password}@{host}:{port}/{database}",
        connect_args={"charset": "utf8mb4"},future=True
    )

    Base.metadata.create_all(engine)

    kraje = ["Polska", "Niemcy", "Francja", "Włochy", "Chiny", "Czechy", "USA", "Węgry", "Brazylia", "Australia"]

    miasta={ "Polska": [faker.city() for _ in range(10)],
         "Niemcy": [faker2.city() for _ in range(10)],
         "Francja": [faker3.city() for _ in range(10)],
         "Włochy": [faker4.city() for _ in range(10)],
         "Chiny": [faker5.city() for _ in range(10)],  
         "Czechy": [faker6.city() for _ in range(10)],
         "USA": [faker7.city() for _ in range(10)],
         "Węgry": [faker8.city() for _ in range(10)],
         "Brazylia": [faker9.city() for _ in range(10)],
         "Australia": [faker10.city() for _ in range(10)]}
    kody_pocztowe = {"Polska":[faker.postcode() for _ in range(100)],
                     "Niemcy":[faker2.postcode() for _ in range(100)],
                     "Francja":[faker3.postcode() for _ in range(100)],
                     "Włochy":[faker4.postcode() for _ in range(100)],
                     "Chiny":[faker5.postcode() for _ in range(100)],  
                     "Czechy":[faker6.postcode() for _ in range(100)],
                     "USA":[faker7.postcode() for _ in range(100)],
                     "Węgry":[faker8.postcode() for _ in range(100)],
                     "Brazylia":[faker9.postcode() for _ in range(100)],
                     "Australia":[faker10.postcode() for _ in range(100)]}
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    stworz_panstwa_miasta(session, kraje, miasta, kody_pocztowe)
    usun = True
    
    
    miasta_db = session.query(Miasta).all()
    
    stworz_wlascicieli(session, usun)
    
    stworz_sportowcow(session, usun)
    
    stworz_sponsorow(session, usun)
    sponsorzy_db = session.query(Sponsorzy).all()
    sportowcy_db=session.query(Sportowcy).all()
    stworz_pracownikow(session, usun)
    pracownicy_db = session.query(Pracownicy).all()
    stworz_sportowcow_sponsorow(session, sportowcy_db, sponsorzy_db, usun)
    stworz_zawody(session, miasta_db, usun)
    
    stworz_finansowanie(session, sponsorzy_db, pracownicy_db, usun)
    
    
    
if __name__ == "__main__":
    main()