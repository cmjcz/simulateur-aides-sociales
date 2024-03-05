from datetime import date
from ressource import Ressource


class Personne:
    """
    Classe qui représente une personne

    Attributs:
        nom (str): le nom de la personne
        date_naissance (datetime.date): date de naissance de la personne
        ressources (dictionnaire): ensemble des ressources de la personne
    """
    def __init__(self, nom: str, date_naissance: date):
        self.nom = nom
        self.date_naissance = date_naissance
        self.ressources = {}

    def ajouter_ressource(self, ressource: Ressource):
        """
        Ajoute une ressource à la personne

        Paramètres:
            ressource: objet Ressource à ajouter à la personne
        """
        self.ressources[ressource.date] = ressource

    def __str__(self):
        return f"{self.nom} né·e le {self.date_naissance}"
