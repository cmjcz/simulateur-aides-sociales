from date_mensuelle_iterator import date_mensuelle_range
from date_mensuelle import DateMensuelle


class CalculateurTrimestreReferenceAAH:
    """
    Objet permettant de retourner le trimestre de référence
    sur lequel se baser pour calculer l’AAH en fonction
    de la date de début de l’AAH
    """
    def __init__(self, date_debut_aah: DateMensuelle) -> None:
        self.date_debut_aah = date_debut_aah

    def calculer_trimestre_reference(self, mois: DateMensuelle):
        """
        Retourne le trimestre de référence qui doit être utilisé
        pour calculer l’AAH sur un mois donné
        Il est retourné sous forme de Liste
        """
        for debut_trimestre in date_mensuelle_range(self.date_debut_aah, None, 3):
            if mois < debut_trimestre:
                return [
                    debut_trimestre-6,
                    debut_trimestre-5,
                    debut_trimestre-4
                    ]


if __name__ == "__main__":
    janvier = DateMensuelle(1, 2023)
    juin = DateMensuelle(6, 2023)
    juillet = DateMensuelle(7, 2023)
    aout = DateMensuelle(8, 2023)

    calculateur = CalculateurTrimestreReferenceAAH(date_debut_aah=janvier)
    trimestre = calculateur.calculer_trimestre_reference(mois=juin)

    print("Période référence AAH de Juin")
    for mois in trimestre:
        print(mois)
    
    trimestre = calculateur.calculer_trimestre_reference(mois=juillet)

    print("Période référence AAH de Juillet")
    for mois in trimestre:
        print(mois)
    
    trimestre = calculateur.calculer_trimestre_reference(mois=aout)

    print("Période référence AAH d’Aout")
    for mois in trimestre:
        print(mois)
