# Purpur Tentakel
# Spielewiese 1
# Python 3.10

pi: float = 3.1416


class quader:
    def __init__(self, laenge: int, breite: int, hoehe: int) -> None:
        self.laenge: int = laenge
        self.breite: int = breite
        self.hoehe: int = hoehe

    def volumen(self):
        volumen = self.laenge * self.breite * self.hoehe
        return volumen

    def oberflaeche(self):
        oberflaeche = 2 * (self.laenge * self.breite + self.laenge * self.hoehe + self.breite * self.hoehe)
        return oberflaeche

    def max_seitenflaeche(self):
        seite1 = self.laenge * self.breite
        seite2 = self.laenge * self.hoehe
        seite3 = self.breite * self.hoehe
        return max(seite1, seite2, seite3)


class zylinder:
    def __init__(self, pi:float, radius:int, tiefe:int, menge:int)->None:
        self.pi:float = pi
        self.radius:int = radius
        self.tiefe:int = tiefe
        self.menge:int = menge

    def zylinder_vol(self)->float:
        zylinder_vol:float = self.pi * (self.radius ** 2) * self.tiefe * self.menge
        return zylinder_vol

    def zylinder_mantel(self):
        zylinder_mantel = self.pi * (self.radius ** 2) * self.tiefe * self.menge
        return zylinder_mantel

    def zylinder_kopf(self):
        zylinder_kopf = self.radius * self.radius * pi
        return zylinder_kopf


stahlplatte = quader(laenge=300, breite=100, hoehe=50)

platte1:zylinder = zylinder(pi=pi, radius=20, tiefe=50, menge=5)

print("die platte hat ein volumen von ", stahlplatte.volumen())
print(platte1.zylinder_vol())
print(platte1.zylinder_vol()/3)
print("die oberfläche beträgt ", stahlplatte.oberflaeche())
print("das volumen der lochplatte beträgt", stahlplatte.volumen() - platte1.zylinder_vol())
print("die oberfläche der lochblechs beträgt", stahlplatte.oberflaeche() + platte1.zylinder_mantel())
print("das volumen mit ein drittel loch beträgt", stahlplatte.volumen() - platte1.zylinder_vol()/3)
print("das volumen eines legosteins beträgt", stahlplatte.volumen() + platte1.zylinder_vol() + platte1.zylinder_kopf())
