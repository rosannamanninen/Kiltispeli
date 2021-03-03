import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QMainWindow, QLabel , QPushButton, QMessageBox, QApplication)


class Window(QMainWindow):

    def __init__(self, tila):
        QMainWindow.__init__(self)
        self.title = "Kiltispeli"
        self.top = 100
        self.left = 100
        self.width = 1000
        self.height = 600
        self.tila = tila
        self.tila.determine_gui(self)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.InitUI()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(10)

        self.message = "Viestikenttä, tähän tulee kaikki info"
        self.muuttujamessage = "Kiltiksen muuttujat:\n" \
                               "Lämpötila: \n" \
                               "Kahvi:\n" \
                               "Cosmot:\n" \
                               "Ikkuna\n" \
                               "\n" \
                               "Hirviö:\n" \
                               "Hp: "


        self.show()

    def InitUI(self):

        self.tausta = QLabel(self)
        self.tausta.setPixmap(QtGui.QPixmap('Kiltis3.jpg'))
        self.tausta.setGeometry(0, 0, self.width, self.height)

        self.label = QLabel(self)
        self.label.setText("Kiltispeli!")
        self.label.move(150, 40)
        self.label.adjustSize()

        self.viesti = QLabel(self)
        self.viesti.setText("Viestikenttä, tähän tulee kaikki info")
        self.viesti.move(720,40)
        self.viesti.adjustSize()

        self.muuttujat = QLabel(self)
        self.muuttujat.setText("Kiltiksen muuttujat:\n"
                               "Lämpötila: \n"
                               "Kahvi: \n"
                               "Snapsit: \n"
                               "Ikkuna: \n"
                               "\n"
                               "Hirviö:\n"
                               "Hp: ")
        self.muuttujat.move(150,370)
        self.muuttujat.adjustSize()

        self.kierrokset = QLabel(self)
        self.kierrokset.setText("Kierrokset: 0")
        self.kierrokset.move(150, 500)
        self.kierrokset.adjustSize()

        self.kiltalaiset = QLabel(self)
        self.kiltalaiset.setText("")
        self.kiltalaiset.move(520, 350)
        self.kiltalaiset.adjustSize()

        self.InitButtons()

    def update_all(self):
        self.viesti.setText(self.tila.get_tilaviesti())
        self.viesti.adjustSize()

        self.muuttujat.setText(self.tila.muuttujaviesti())
        self.muuttujat.adjustSize()

        self.kiltalaiset.setText("Kiltiksellä:\n\n" + self.tila.kiltalaisinfo())
        self.kiltalaiset.adjustSize()

        self.kierrokset.setText("Kierrokset: {:d}".format(self.tila.get_kierrokset()))
        self.kierrokset.adjustSize()

        self.update_ikkunanappi()

    def closeEvent(self, event):
        varmistus = QMessageBox.question(self, "Ikkunan sulkeminen", "Oletko ihan varma?",
                                         QMessageBox.Yes | QMessageBox.No)
        if varmistus == QMessageBox.Yes:
            event.accept()
        if varmistus == QMessageBox.No:
            event.ignore()

    def peli(self):
        self.label.setText("Erään synkän ja masentavan periodin aikana\n"
                           "kiltikselle oli asuttautunut hirviö, laiska\n"
                           "ja pahantuulinen. Esimerkillään se kuitenkin\n"
                           "tartutti asenteensa kiltalaisiin ja houkutteli\n"
                           "fuksit pahoille teille.\n\n"
                           "Sinun tehtäväsi on pelastaa kiltis ja sen\n"
                           "käyttäjät tältä iljettävältä oliolta, joka\n"
                           "kuluttaa kaiken hapen ja juo kahvitkin!")
        self.label.adjustSize()

    def tilaviesti(self, message):
        if self.jatkan():
            self.message = message
        else:
            self.tilaviesti(message)

    def InitButtons(self):
        self.ulos = QPushButton("Lore", self)
        self.ulos.clicked.connect(self.peli)
        self.ulos.setToolTip("Miten tähän tilanteeseen päädyttiin :o")

        self.info = QPushButton("Ohje", self)
        self.info.move(0, 40)
        self.info.clicked.connect(self.ohje)
        self.info.setToolTip("Lue ohjeita!")

        self.poistu = QPushButton("Poistu", self)
        self.poistu.move(0, 120)
        self.poistu.clicked.connect(self.sulje)
        self.poistu.setToolTip("Sulje sovellus!")

        self.snapsi = QPushButton("Lukekaa Snapsia", self)
        self.snapsi.move(520, 40)
        self.snapsi.clicked.connect(self.tila.lue_snapsi)
        self.snapsi.setToolTip("Lukekaa snapsia kiltalaisten kanssa,\n"
                               "+1 rp/ kiltalainen -1 snapsi")

        self.kahvi = QPushButton("Juokaa kahvia", self)
        self.kahvi.move(520, 80)
        self.kahvi.clicked.connect(self.tila.keita_kahvia)
        self.kahvi.setToolTip("Keitä kahvia, nostattaa satunnaisen kiltalaisen rp:ta +2,\n"
                              "hirviö pitää kuitenkin myös kahvista! -1 kahvi")

        self.mindfull = QPushButton("Mindfullnes", self)
        self.mindfull.move(520, 120)
        self.mindfull.clicked.connect(self.tila.mindfullnes)
        self.mindfull.setToolTip("Harrastakaa mindfullnesia, tämä vahingoittaa hirviötä.\n"
                                 "Varo kuitenkin, saatat suututtaa sen! :o")

        self.uusipeli = QPushButton("Uusi peli", self)
        self.uusipeli.move(0, 80)
        self.uusipeli.clicked.connect(self.tila.uusipeli)
        self.uusipeli.setToolTip("Aloita uusi peli, vanha keskeytyy!")

        self.ikkunanappi = QPushButton("Avaa ikkuna", self)
        self.ikkunanappi.move(520, 160)
        self.ikkunanappi.clicked.connect(self.tila.ikkuna_muutos)

        self.houkuttelu = QPushButton("Houkuttele", self)
        self.houkuttelu.move(520, 200)
        self.houkuttelu.clicked.connect(self.tila.houkuttele)
        self.houkuttelu.setToolTip("Houkuttele muita tulemaan kiltikselle ja auttamaan\n"
                                   "hirviön voittamisessa!")

        self.kauppaan = QPushButton("Käy kaupassa", self)
        self.kauppaan.move(520, 240)
        self.kauppaan.clicked.connect(self.tila.kauppa)
        self.kauppaan.setToolTip("Lähetä yksi kiltalainen käymään kaupassa!(-2rp)\n"
                                 "Kaupasta hän voi tuoda kahvia ja snapsin!")

    def update_ikkunanappi(self):
        if self.tila.get_ikkuna():
            self.ikkunanappi.setText("Sulje ikkuna")
            self.ikkunanappi.setToolTip("Sulje ikkuna, jos se on liian kauan auki\n"
                                        "kiltalaisille sekä hirviölle tulee kylmä!")
        else:
            self.ikkunanappi.setText("Avaa ikkuna")
            self.ikkunanappi.setToolTip("Avaa ikkuna, jos se on liian kauan kiinni\n"
                                        "kiltalaisille tulee kuuma!")


    def aloitapeli(self):
        if not self.tila.onko_paalla():
            self.tilaviesti("peli alkaa!")
            self.tila.intro()
        else:
            self.tilaviesti("Olet jo käynnistänyt pelin,\neikä se ole päättynyt")

    def ohje(self):
        self.label.setText("Pelin tavoite on voittaa hirviö. Sinun tulee myös\n"
                           "pitää kiltalaiset hengissä, muuten et voi voittaa!\n\n"
                           "Voit käyttää erilaisia metodeja,jotka joko nostavat\n"
                           "kiltalaistesi hyvinvointia, vahingoittavat hirviötä\n"
                           "tai keräävät resusrsseja muihin toimintoihin. Muista\n"
                           "myös huolehtia, että ympäristö kiltiksellä on sopiva!\n"
                           "Lämpötila nousee joka kierroksella!\n\n"
                           "Jokaisen toimintosi jälkeen hirviö tekee vuorostaan\n"
                           "jotakin automaattisesti! Tiedot jokaisesta kierroksesta\n"
                           "tulevat näkyviin toimintonappien viereen.\n\n"
                           "Häviät pelin jos kaikki kiltalaisesi menevät pilalle,\n"
                           "eli heidän rp:nsä laskevat nollaan. Hirviö taas häviää,\n"
                           "jos saat pelattua sen hp:n nollaan!\n\n"
                           "Kiltalaisia on tupsuja ja fukseja, joista tupsut kestävät\n"
                           "enemmän vahinkoa.")
        self.label.adjustSize()

    def sulje(self):
        sys.exit()
