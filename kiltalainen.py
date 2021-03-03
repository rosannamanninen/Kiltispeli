
class Kiltalainen():

    def __init__(self, name, type, kiltis):

        self.rp = 7  # kun rp laskee nollaan  kiltalainen kuolee
        self.is_alive = True
        self.name = name
        self.type = type  # joko tupsu tai fuksi 0 = fuksi, 1 = tupsu
        self.huone = kiltis

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_rp(self):
        return self.rp

    def heal(self, amount):
        if self.is_alive:
            self.rp += amount

    def damage(self, amount):
        self.rp -= amount
        if self.rp <= 0:
            self.rippaa()

    def rippaa(self):
        if self.rp <= 0:
            self.huone.tilaviestim(
                "Kiltalaisen {:s} rippauspisteet laskivat\nliian alas ja hän meni pilalle :(".format(
                    self.name))
        else:
            self.huone.tilaviestim("{:s} valitettavasti rippasi :o".format(self.get_name()))
        self.is_alive = False
        self.huone.remove_kiltalainen(self)

