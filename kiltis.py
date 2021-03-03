import hirvio
import kiltalainen


def muutaluku(number):  # laskee numeron tekijöiden määrän (1-5, suuruusalueella, jossa liikutaan)
    tekijat = []
    ehdokas = 2
    while number > 1:
        if number % ehdokas == 0:
            number = number / ehdokas
            tekijat.append(ehdokas)
        else:
            ehdokas += 1
    return len(tekijat)


class Kiltis():  # Luokka, joka hallinnoi peliympäristöä

    def __init__(self):

        self.kiltalaiset = []  # lista kiltiksellä olevista henkilöistä
        self.hirvio = hirvio.Hirvio("namnam")
        self.ikkuna = False  # false = kiinni, true = auki
        self.lampotila = 17
        self.tila = None
        self.pelipaalla = False
        self.kahvi = 0
        self.snapsi = 1
        self.kierrokset = 0

        self.tilaviesti = "Tervetuloa! Aloita uusi peli!"

        self.luo_aloituskitalaiset()
        print(self.kiltalaiset)
        self.lisanimet = ["Klaus", "Jenny-Rosa", "Lukas", "Anna", "Elias", "Susanna","Santtu", "Milla", "Olivia","Maija", "Ian"
                          "Samu", "Susan", "Reetta", "Mikaela", "Silmu", "Laura", "Salli"]

        self.viestit = []

    '''Pelin toimintoja'''

    def luo_aloituskitalaiset(self):

        self.add_kiltalainen(kiltalainen.Kiltalainen("Heidi", 1, self))
        self.add_kiltalainen(kiltalainen.Kiltalainen("Linnea", 0, self))
        self.add_kiltalainen(kiltalainen.Kiltalainen("Emilia", 0, self))

    def uusipeli(self):
        self.ikkuna = False
        self.lampotila = 17
        self.pelipaalla = True
        self.kahvi = 0
        self.snapsi = 1
        self.kierrokset = 0
        self.hirvio = hirvio.Hirvio("Solumolu")
        self.kiltalaiset.clear()
        self.luo_aloituskitalaiset()
        self.tilaviestim("Olet aloittanut uuden pelin!")

    '''Pelaajan toiminnot'''

    def lue_snapsi(self):
        if self.pelitarkistus():
            # print("self.tila.lue_snapsi()")
            if self.snapsi >= 1:
                self.tilaviestim("Luitte snapsin, kiltalaisesi saivat\n"
                                 "lisää rp:ta(+1)")
                self.snapsi -= 1
                for a in self.kiltalaiset:
                    a.heal(1)
                self.vuoroloppu()
            else:
                self.tilaviestim("Kiltikseltä ei löydy snapseja, ette pääse\n"
                                 "lukemaan päätähuimaavia testausraportteja tai\n"
                                 "tarkkaakin tarkempia horoskooppeja :(\n"
                                 "Kokeile jotakin muuta!")

    def keita_kahvia(self):
        if self.pelitarkistus():
            # print("self.tila.keita_kahvia()")
            numero = len(self.kiltalaiset) + self.lampotila + self.hirvio.get_hp()
            if self.kahvi > 0:
                if numero % 2 == 0:
                    if len(self.kiltalaiset) >2:
                        tyyppi = self.kiltalaiset[2]
                    elif len(self.kiltalaiset) >1:
                        tyyppi = self.kiltalaiset[1]
                    else:
                        tyyppi = self.kiltalaiset[0]
                    self.tilaviestim("Keitit kahvia, mutta hirviö joi niin paljon,\n"
                                     "että vain {:s}lle riitti!(+2rp)\n"
                                     "Myös hirviö voimistui tästä +3hp".format(tyyppi.get_name()))
                    tyyppi.heal(2)
                    self.hirvio.heal(1)
                    self.kahvi -= 1
                    self.vuoroloppu()
                else:
                    for a in self.kiltalaiset:
                        a.heal(2)
                    self.tilaviestim("Kahvia riitti kaikille! Jokainen +2rp!")
                self.vuoroloppu()
            else:
                self.tilaviestim("Kahvi on loppu, kokeile jotakin muuta!!")

    def mindfullnes(self):
        if self.pelitarkistus():
            # print("self.tila.mindfullnes()")
            if self.lampotila % 2 == 0:
                self.tilaviestim("Mindfullness operaationne onnistui hyvin, ja\n"
                                 "hirviö menetti 2hp:ta")
                self.hirvio.damage(2)
            else:
                vahinko = self.kiltalaiset[len(self.kiltalaiset)-1]
                self.tilaviestim("Mindfullness puri hirviöön hieman huonosti ja se\n"
                                 "menetti vain 1hp ja suuttuessaan vahingoitti\n"
                                 "kiltalaistasi {:s}(-2rp)".format(vahinko.get_name()))
                vahinko.damage(2)
                self.hirvio.damage(1)

            self.vuoroloppu()

    def ikkuna_muutos(self):
        if self.pelitarkistus():
            # print("self.tila.ikkuna_muutos()")
            if self.ikkuna:
                self.ikkuna = False
                vahinko = self.enitenrp()
                self.tilaviestim("Suljit ikkunan, {:s} kuitenkin väsähti tästä\n"
                                 "urakasta (-1rp)".format(vahinko.get_name()))
                vahinko.damage(1)
            else:
                self.ikkuna = True
                vahinko = self.enitenrp()
                self.tilaviestim(
                    "Avasit ikkunan,{:s} kuitenkin väsähti tästä\n"
                    "urakasta (-1rp)".format(vahinko.get_name()))
                vahinko.damage(1)
            self.vuoroloppu()

    def houkuttele(self): #houkuttelee lisää kiltalaisia!
        if self.pelitarkistus():
            # print("self.tila.houkuttele()")
            if len(self.kiltalaiset) <= 12:
                if self.hirvio.get_hp() % 3 == 0:
                    nimi = self.lisanimet[0]
                    self.lisanimet.remove(nimi)
                    if self.lampotila % 2 == 0:
                        tyyppi = 0
                    else:
                        tyyppi = 1
                    kil = kiltalainen.Kiltalainen(nimi, tyyppi, self)
                    self.add_kiltalainen(kil)
                    self.tilaviestim("Kiltikselle saapui uusi kiltalainen {:s}. Jee!".format(kil.get_name()))
                else:
                    self.tilaviestim("Valitettavasti kiltikselle ei saapunut ketään :(")
                self.vuoroloppu()
            else:
                self.tilaviestim("Kiltikselle ei mahdu enenpää ihmisiä!")

    def kauppa(self):
        if self.pelitarkistus():
            # print("self.tila.kauppa()")
            luku1 = self.hirvio.get_hp() // 3 #kahvi
            self.kahvi += luku1
            kahvin = "{:d} kahvia".format(luku1)

            if luku1 == 1:
                kahvin = "yhden kahvin"

            luku2 = self.hirvio.get_hp() % 2 #snapsi
            self.snapsi += luku2

            uhri = self.enitenrp()

            if luku1 > 0 and luku2 > 0:
                self.tilaviestim("{:s}(-2rp) kävi kaupassa, ja toi mukanaan\n"
                                 "{:s} ja yhden S'napsin".format(uhri.get_name(), kahvin))
            elif luku1 > 0:
                self.tilaviestim("{:s}(-2rp) kävi kaupassa, ja toi mukanaan\n"
                                 "{:s}.".format(uhri.get_name(), kahvin))
            elif luku1 == 0 and luku2 == 1:
                self.tilaviestim("{:s}(-2rp) kävi kaupassa, ja toi mukanaan\n"
                                 "yhden S'napsin".format(uhri.get_name()))
            else:
                self.tilaviestim("{:s}(-2rp) kävi kaupassa, muttei tuonut\n"
                                 "sieltä mitään!".format(uhri.get_name()))
            uhri.damage(2)
            self.vuoroloppu()

    def vuoroloppu(self):
        if self.hirvio.alive():
            self.hirvioturn()
            if len(self.kiltalaiset) > 0:
                self.muuttujienvaikutukset()
                self.kiltismuuttujat()
                if len(self.kiltalaiset) >0 and self.hirvio.alive():
                    self.tilaviestim("Sinun vuorosi")
                else:
                    if len(self.kiltalaiset)>0:
                        self.tilaviestim("Voitit pelin!!")
                        self.peli_pois()
                    else:
                        self.tilaviestim("Olosuhteet pilasivat loput kiltalaisesi, hävisit :(")
                        self.peli_pois()
            else:
                self.tilaviestim("Hirviö pilasi kiltalaisesi, hävisit :(")
                self.peli_pois()
        else:
            self.tilaviestim("Voitit pelin, hirviö ei ole enää elossa")
            self.peli_pois()

    '''Hirviön vuoro'''

    def hirvioturn(self):
        numero = muutaluku(len(self.kiltalaiset) + self.lampotila + self.hirvio.get_hp())

        if numero == 1:  # smash
            vahinko = self.maaraansuhteutettu()
            info = ""
            for w in vahinko:
                info += "" + w.get_name() + " -2rp "
            self.tilaviestim("Hirviö houkuttelee muutaman kiltalaisen\n"
                             "pelaamaan smashia\n"
                             "{:s}".format(info))
            for a in vahinko:
                a.damage(2)

        elif numero == 2:  # mariamonde
            self.tilaviestim("Hirviö soittaa Maria Mondea,\n"
                             "Fuksit -2 rp, Tupsut -1 rp.\n"
                             "Hirviö voimaantuu tästä 3hp:n verran!")
            for w in self.kiltalaiset:
                if w.get_type() == 0:
                    w.damage(1)
                else:
                    w.damage(1)
            self.hirvio.heal(3)

        elif numero == 3:  # epäonnistuu
            self.tilaviestim("Hirviö ei onnistunut tekemään mitään")

        elif numero == 4:  # pelottele kursseilla
            self.tilaviestim("Hirviö pelotteli kiltalaistasi kurseilla, {:s}\n"
                             "menetti 2 rp:ta.".format(self.kiltalaiset[0].get_name()))
            self.kiltalaiset[len(self.kiltalaiset)-1].damage(2)

        elif numero == 5:  # kaappaa
            kaapattu = self.kiltalaiset[0]
            self.tilaviestim("Hirviö kaappasi yhden kiltalaisesi,\n"
                             "{:s} menetetty.".format(kaapattu.get_name()))
            kaapattu.rippaa()


    '''Matikkaa'''

    def maaraansuhteutettu(self):
        if len(self.kiltalaiset) > 6:
            number = len(self.kiltalaiset) // 2
            vahinko = [self.kiltalaiset[1], self.kiltalaiset[number], self.kiltalaiset[number * 2 - 2]]
        elif len(self.kiltalaiset) > 3:
            vahinko = [self.kiltalaiset[0], self.kiltalaiset[3]]
        else:
            if self.hirvio.get_hp() % 2 == 0:
                vahinko = [self.kiltalaiset[0]]
            else:
                vahinko = [self.kiltalaiset[len(self.kiltalaiset) - 1]]
        return vahinko

    def enitenrp(self):
        korkein = self.kiltalaiset[0]
        for k in self.kiltalaiset:
            if k.get_rp() >= korkein.get_rp():
                korkein = k
        return k


    '''Pelin kontrollointi'''

    def peli_pois(self):
        self.pelipaalla = False
        self.kierrokset = 0

    def pelitarkistus(self):
        if self.pelipaalla:
            self.kierrokset += 1
            return True
        else:
            self.tilaviestim("Peli ei ole päällä! Aloita uusi painamalla\n"
                             "Uusi peli -nappia!")
            return False

    '''Kiltiksen muuttujat'''

    def kiltismuuttujat(self):
        if self.ikkuna:
            self.lampotila -= 1
        elif len(self.kiltalaiset) > 2:  # jos kiltiksellä on enemmän kuin 2 henkeä lämpötila nousee asteella
            self.lampotila += 1

    def muuttujienvaikutukset(self):
        if self.lampotila >= 25:
            self.tilaviestim("Kiltiksellä on liian kuuma! Kaikki -1rp.")
            for w in self.kiltalaiset:
                w.damage(1)

        elif self.lampotila < 16:
            self.tilaviestim("Kiltiksellä on liian kylmä! Kaikki -1rp\n"
                             "ja hirviö -1rp!")
            for w in self.kiltalaiset:
                w.damage(1)
            self.hirvio.damage(1)

    '''Lisäys ja poistaminen'''

    def add_kiltalainen(self, kiltalainen):
        self.kiltalaiset.append(kiltalainen)

    def remove_kiltalainen(self, kiltalainen):
        self.kiltalaiset.remove(kiltalainen)

    '''Viestintä'''

    def tilaviestim(self, viesti):
        if len(self.viestit) < 5:
            self.viestit.append(viesti)
        else:
            self.viestit.remove(self.viestit[0])
            self.viestit.append(viesti)
        teksti = ""
        for a in self.viestit:
            teksti = "{:s}{:s}\n\n".format(teksti,a)
        self.tilaviesti = teksti


    def muuttujaviesti(self):
        if not self.pelipaalla:
            return "Kiltiksen muuttujat:\n" \
                   "Lämpötila: \n" \
                   "Kahvi:\n" \
                   "Snapsit:\n" \
                   "Ikkuna:\n" \
                   "\n" \
                   "Hirviö:\n" \
                   "Hp:"

        else:
            if self.ikkuna:
                ikkuna = "Auki"
            else:
                ikkuna = "Kiinni"
            lt = "(Sopiva)"
            if self.lampotila >= 25:
                lt = "(Kuumaaaa)"
            elif self.lampotila < 16:
                lt = "(Kylmääää)"
            viesti = "Kiltiksen muuttujat: \n\n" \
                    "Lämpötila: {:d} {:s}\n" \
                    "Kahvi: {:d}\n" \
                    "Snapsit: {:d}\n" \
                    "Ikkuna: {:s}\n" \
                    "\n" \
                    "Hirviö:\n" \
                    "Hp: {:d} {:s}".format(self.lampotila, lt, self.kahvi, self.snapsi, ikkuna, self.hirvio.get_hp(),
                                           "* "*self.hirvio.get_hp())
            return viesti

    def kiltalaisinfo(self):
        info = ""
        if self.pelipaalla:
            for hkl in self.kiltalaiset:
                if hkl.get_type() == 0:
                    tyyppi = "fuksi"
                else:
                    tyyppi = "Tupsu"
                info += "Nimi: {:s}  Tyyppi: {:s}  Rp: {:d} {:s}\n".format(hkl.get_name(), tyyppi, hkl.get_rp(),
                                                                           "* "*hkl.get_rp())

        return info

    '''Get-funktiot'''

    def get_tila(self):
        return self.tila

    def get_kiltalaiset(self):
        return self.kiltalaiset

    def get_ikkuna(self):
        return self.ikkuna

    def get_tilaviesti(self):
        return self.tilaviesti

    def get_kierrokset(self):
        return self.kierrokset

    def onko_paalla(self):
        return self.pelipaalla

    def determine_gui(self, tila):
        self.tila = tila

