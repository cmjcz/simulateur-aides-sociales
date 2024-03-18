from foyer import Foyer
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

    def __init__(self, foyer: Foyer):
        self.foyer = foyer

    def __calculer_plafond_ressources(self):
        plafond_ressources = self.AAH_TAUX_PLEIN
        if self.foyer.contient_conjoint():
            plafond_ressources += self.AAH_TAUX_PLEIN * 0.81
        plafond_ressources += 0.405 * self.AAH_TAUX_PLEIN * self.foyer.nombre_personnes_a_charge()
        return plafond_ressources

    def __calculer_ressources_allocataire(self, periode_reference):
        ressources_trimestres = 0
        for mois in periode_reference:
            ressources_mois = self.foyer.ressource_allocataire(mois)
            ressources_trimestres += ressources_mois
        ressources_moyennes = ressources_trimestres / len(periode_reference)
        seuil = 0.3 * self.SMIC_MENSUEL_BRUT
        ressources_seuil1 = plafond(ressources_moyennes, seuil)
        ressources_seuil2 = plancher(ressources_moyennes - seuil, 0)
        ressources = ressources_seuil1 * self.TAUX_PREMIERE_TRANCHE + ressources_seuil2 * self.TAUX_SECONDE_TRANCHE
        return ressources

    def __calculer_ressources_conjoint(self, periode_reference):
        if not self.foyer.contient_conjoint():
            return 0
        nombre_personne_a_charge = self.foyer.nombre_personnes_a_charge()
        abattement_annuel = self.ABATTEMENT_ANNUEL_CONJOINT + nombre_personne_a_charge * self.ABATTEMENT_ANNUEL_CONJOINT_PAR_ENFANT
        abattement_trimestriel = abattement_annuel / 4
        ressources_trimestre = 0
        for mois in periode_reference:
            ressources_mois = self.foyer.ressource_conjoint(mois)
            ressources_trimestre += ressources_mois
        ressources_trimestre = abattement(
            ressources_trimestre,
            abattement_trimestriel)
        ressources_moyennes = ressources_trimestre / len(periode_reference)
        return plancher(ressources_moyennes, 0)

    def calculer_AAH(self, periode_reference):
        """
        Calcule l’AAH pour une periode de reference donnée

        Paramètres:
            periode_preference (Set de DateMensuelle): mois utilisé pour calculer l’AAH
        """
        plafond_ressources = self.__calculer_plafond_ressources()
        ressources_allocataire = self.__calculer_ressources_allocataire(periode_reference)
        ressources_conjoint = self.__calculer_ressources_conjoint(periode_reference)
        ressources_foyer = ressources_allocataire + ressources_conjoint
        aah = plafond_ressources - ressources_foyer
        aah = plafond(aah, self.AAH_TAUX_PLEIN)
        aah = plancher(aah, 0)
        aah = round(aah, 2)
        return aah
