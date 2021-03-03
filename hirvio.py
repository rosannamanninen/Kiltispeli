

class Hirvio():

    def __init__(self,name):

        self.hp = 10
        self.is_alive = True
        self.name = name
        self.type = 2

    def alive(self):
        return self.is_alive

    def get_hp(self):
        return self.hp

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def heal(self, amount):
        if self.is_alive:
            self.hp += amount

    def damage(self, amount):
        if self.is_alive:
            self.hp -= amount
            if self.hp <= 0:
                self.rippaa()

    def rippaa(self):
        print("hirviö on kuollut")
        self.is_alive = False