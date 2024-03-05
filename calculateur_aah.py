from personne import Personne
from date_mensuelle import DateMensuelle
from utils import plafond, plancher, abattement


class CalculateurAAH:
    """
    Objet implémentant le calcul de l’AAH
    L’objet permet de définir la situation, puis de calculer

    L’objet ne devrait pas être réutilisé avec une autre situation
    en modifiant directement les attributs

    Attributs:
        allocataire (Personne): allocataire sur lequel le calcul sera effectué
        conjoint (Personne, optionnel): conjoint·e de l’allocataire
        personnes_a_charge (collection): ensemble des personnes à charge
    """

    AAH_TAUX_PLEIN = 971.37
    SMIC_MENSUEL_BRUT = 1747.24
    TAUX_PREMIERE_TRANCHE = 0.2
    TAUX_SECONDE_TRANCHE = 0.6

    ABATTEMENT_ANNUEL_CONJOINT = 5000
    ABATTEMENT_ANNUEL_CONJOINT_PAR_ENFANT = 1400

    def __init__(self, allocataire: Personne):
        self.allocataire = allocataire
        self.conjoint = None
        self.personnes_a_charge = []

    def definir_conjoint(self, conjoint: Personne):
        """
        Définit le conjoint pour le calcul

        Paramètres:
            conjoint (Personne): conjoint·e de l’allocataire
        """
        self.conjoint = conjoint

    def ajouter_personne_a_charge(self, personne: Personne):
        """
        Ajoute une personne à charge au foyer

        Paramètres:
            personne (Personne): personne à charge à ajouter
        """
        self.personnes_a_charge.append(personne)

    def __calculer_plafond_ressources(self):
        plafond_ressources = self.AAH_TAUX_PLEIN
        if self.conjoint is not None:
            plafond_ressources += self.AAH_TAUX_PLEIN * 0.81
        for enfant in self.personnes_a_charge:
            plafond_ressources += 0.405 * self.AAH_TAUX_PLEIN
        return plafond_ressources

    def __calculer_ressources_allocataire(self, date: DateMensuelle):
        ressources_trimestres = 0
        for mois in range(1, 4):
            ressources_mois = self.allocataire.ressources.get(date - mois)
            if ressources_mois is not None:
                ressources_trimestres += ressources_mois.montant
        ressources_moyennes = ressources_trimestres / 3
        seuil = 0.3 * self.SMIC_MENSUEL_BRUT
        ressources_seuil1 = plafond(ressources_moyennes, seuil)
        ressources_seuil2 = plancher(ressources_moyennes - seuil, 0)
        ressources = ressources_seuil1 * self.TAUX_PREMIERE_TRANCHE + ressources_seuil2 * self.TAUX_SECONDE_TRANCHE
        return ressources

    def __calculer_ressources_conjoint(self, date: DateMensuelle):
        if self.conjoint is None:
            return 0
        nombre_personne_a_charge = len(self.personnes_a_charge)
        abattement_annuel = self.ABATTEMENT_ANNUEL_CONJOINT + nombre_personne_a_charge * self.ABATTEMENT_ANNUEL_CONJOINT_PAR_ENFANT
        abattement_trimestriel = abattement_annuel / 4
        ressources_trimestre = 0
        for mois in range(1, 4):
            ressources_mois = self.conjoint.ressources.get(date - mois)
            if ressources_mois is not None:
                ressources_trimestre += ressources_mois.montant
        ressources_trimestre = abattement(
            ressources_trimestre,
            abattement_trimestriel)
        ressources_moyennes = ressources_trimestre / 3
        return plancher(ressources_moyennes, 0)

    def calculer_AAH(self, date: DateMensuelle):
        """
        Calcule l’AAH pour le foyer définit pour une date donnée

        Paramètres:
            date (DateMensuelle): mois pour lequel calculer l’AAH
        """
        plafond_ressources = self.__calculer_plafond_ressources()
        ressources_allocataire = self.__calculer_ressources_allocataire(date)
        ressources_conjoint = self.__calculer_ressources_conjoint(date)
        ressources_foyer = ressources_allocataire + ressources_conjoint
        aah = plafond_ressources - ressources_foyer
        aah = plafond(aah, self.AAH_TAUX_PLEIN)
        aah = plancher(aah, 0)
        aah = round(aah, 2)
        return aah
