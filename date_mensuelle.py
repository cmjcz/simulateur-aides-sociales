class DateMensuelle:
    """
    Objet immutable
    Représente une date sur un format mois/année uniquement
    Permet de faire facilement des opérations sur la date

    Cet objet est issus d’un besoin d’utiliser des dates
    d’un point de vue aide sociale, c’est à dire uniquement
    une question de mois / année

    Contrairement à un couple de nombre entiers, il permet
    de stocker explicitement ces 2 valeurs et de réaliser
    des opérations d’ajout et de soustraction de mois
    
    Rajouter 1 mois incrémentera l’année automatiquement
    si on est en Décembre, et retirer 1 mois décrémentera
    automatiquement l’année si on est en Janvier

    Attributs:
        mois: nombre entier de 1 à 12 représentant le mois
        année: nombre entier représentant l’année
    """

    def __init__(self, mois: int, annee: int) -> None:
        self._annee = annee
        self._mois = mois

    @property
    def annee(self):
        return self._annee

    @property
    def mois(self):
        return self._mois

    def __add__(self, nombre_mois):
        mois = self.mois
        annee = self.annee
        for i in range(nombre_mois):
            if mois < 12:
                mois += 1
            else:
                annee += 1
                mois = 1
        return DateMensuelle(mois, annee)

    def __sub__(self, nombre_mois):
        mois = self.mois
        annee = self.annee
        for i in range(nombre_mois):
            if mois > 1:
                mois -= 1
            else:
                annee -= 1
                mois = 12
        return DateMensuelle(mois, annee)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DateMensuelle):
            return False
        return self._mois == other._mois and self._annee == other._annee

    def __hash__(self) -> int:
        return hash((self._annee, self._mois))

    def __str__(self):
        return f"{self._mois}/{self._annee}"


if __name__ == "__main__":
    d1 = DateMensuelle(1, 2023)
    d2 = DateMensuelle(12, 2023)
    d3 = DateMensuelle(1, 2023)
    d4 = DateMensuelle(1, 2025)
    d5 = DateMensuelle(2, 2023)

    print("Tests ajout")
    for nombre_mois in range(1, 14):
        print(f"{d1} + {nombre_mois} mois = {d1 + nombre_mois}")
    for nombre_mois in range(1, 14):
        print(f"{d2} + {nombre_mois} mois = {d2 + nombre_mois}")

    print("Tests soustraction")
    for nombre_mois in range(1, 14):
        print(f"{d1} - {nombre_mois} mois = {d1 - nombre_mois}")
    for nombre_mois in range(1, 14):
        print(f"{d2} - {nombre_mois} mois = {d2 - nombre_mois}")
    for nombre_mois in range(1, 14):
        print(f"{d5} - {nombre_mois} mois = {d5 - nombre_mois}")

    print("Test égalité")
    print(f"{d1} = {d3} ? {d1 == d3}")
    print(f"{d1} != {d4} ? {d1 != d4}")
    print(f"{d1} != {d5} ? {d1 != d5}")
