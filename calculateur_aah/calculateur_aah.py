from .constantes_aah import ConstantesAAH
from model.foyer import Foyer
from utils import plafond, plancher, abattement


class CalculateurAAH:
    """
    Objet implémentant le calcul de l’AAH
    L’objet permet de définir la situation, puis de calculer

    L’objet ne devrait pas être réutilisé avec une autre situation
    en modifiant directement les attributs

    Ce calculateur n’implémente que le calcul conjugalisé valable à partir de
    Janvier 2022, prenant fin pour la majorité des allocataires en
    Octobre 2023

    Attributs:
        foyer (Foyer): foyer sur lequel effectuer le calcul
    """

    def __init__(self, foyer: Foyer):
        self.foyer = foyer

    def __calculer_plafond_ressources(self):
        AAH_TAUX_PLEIN = self.CONSTANTES.AAH_TAUX_PLEIN
        plafond_ressources = AAH_TAUX_PLEIN
        if self.foyer.contient_conjoint():
            plafond_ressources += AAH_TAUX_PLEIN * 0.81
        plafond_ressources += 0.405 * AAH_TAUX_PLEIN * self.foyer.nombre_personnes_a_charge()
        return plafond_ressources

    def __calculer_ressources_allocataire(self, periode_reference):
        SMIC_MENSUEL_BRUT = self.CONSTANTES.SMIC_HORAIRE_BRUT * 151.67
        TAUX_PREMIERE_TRANCHE = self.CONSTANTES.TAUX_PREMIERE_TRANCHE
        TAUX_SECONDE_TRANCHE = self.CONSTANTES.TAUX_SECONDE_TRANCHE

        ressources_trimestres = 0
        for mois in periode_reference:
            ressources_mois = self.foyer.ressource_allocataire(mois)
            ressources_trimestres += ressources_mois
        ressources_moyennes = ressources_trimestres / len(periode_reference)
        seuil = 0.3 * SMIC_MENSUEL_BRUT
        ressources_seuil1 = plafond(ressources_moyennes, seuil)
        ressources_seuil2 = plancher(ressources_moyennes - seuil, 0)
        ressources = ressources_seuil1 * TAUX_PREMIERE_TRANCHE + ressources_seuil2 * TAUX_SECONDE_TRANCHE
        return ressources

    def __calculer_ressources_conjoint(self, periode_reference):
        ABATTEMENT_ANNUEL_CONJOINT = self.CONSTANTES.ABATTEMENT_ANNUEL_CONJOINT
        ABATTEMENT_ANNUEL_CONJOINT_PAR_ENFANT = self.CONSTANTES.ABATTEMENT_ANNUEL_CONJOINT_PAR_ENFANT
        if not self.foyer.contient_conjoint():
            return 0
        nombre_personne_a_charge = self.foyer.nombre_personnes_a_charge()
        abattement_annuel = ABATTEMENT_ANNUEL_CONJOINT + nombre_personne_a_charge * ABATTEMENT_ANNUEL_CONJOINT_PAR_ENFANT
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
            periode_preference (Liste de DateMensuelle): mois utilisés pour calculer l’AAH
        """
        self.CONSTANTES = ConstantesAAH(periode_reference[-1])
        plafond_ressources = self.__calculer_plafond_ressources()
        ressources_allocataire = self.__calculer_ressources_allocataire(periode_reference)
        ressources_conjoint = self.__calculer_ressources_conjoint(periode_reference)
        ressources_foyer = ressources_allocataire + ressources_conjoint
        aah = plafond_ressources - ressources_foyer
        aah = plafond(aah, self.CONSTANTES.AAH_TAUX_PLEIN)
        aah = plancher(aah, 0)
        aah = round(aah, 2)
        return aah
