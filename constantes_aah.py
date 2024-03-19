from date_mensuelle import DateMensuelle
from date_mensuelle_interval import DateMensuelleInterval

class ConstantesAAH:
    """
    Cet objet a pour objectif de centraliser la gestion des constantes
    pour le calcul de l’AAH

    En effet, les constantes utilisées pour le calcul dépendent du mois
    sur lequel le calcul est effectué.
    """
    def __init__(self, date) -> None:
        self.date = date

        self._aah_taux_plein = {
            DateMensuelleInterval(DateMensuelle(4, 2020), DateMensuelle(3, 2021)): 902.70,
            DateMensuelleInterval(DateMensuelle(4, 2021), DateMensuelle(3, 2022)): 903.60,
            DateMensuelleInterval(DateMensuelle(4, 2022), DateMensuelle(6, 2022)): 919.86,
            DateMensuelleInterval(DateMensuelle(7, 2022), DateMensuelle(3, 2023)): 956.65,
            DateMensuelleInterval(DateMensuelle(4, 2023), DateMensuelle(3, 2024)): 971.37,
            DateMensuelleInterval(DateMensuelle(4, 2024), DateMensuelle(3, 2025)): 1016.05
        }

        self._smic_horaire_brut = {
            DateMensuelleInterval(DateMensuelle(1, 2021), DateMensuelle(7, 2021)): 10.25,
            DateMensuelleInterval(DateMensuelle(8, 2021), DateMensuelle(12, 2021)): 10.48,
            DateMensuelleInterval(DateMensuelle(1, 2022), DateMensuelle(4, 2022)): 10.57,
            DateMensuelleInterval(DateMensuelle(5, 2022), DateMensuelle(7, 2022)): 10.85,
            DateMensuelleInterval(DateMensuelle(8, 2022), DateMensuelle(12, 2022)): 11.07,
            DateMensuelleInterval(DateMensuelle(8, 2022), DateMensuelle(12, 2022)): 11.07,
            DateMensuelleInterval(DateMensuelle(1, 2023), DateMensuelle(4, 2023)): 11.27,
            DateMensuelleInterval(DateMensuelle(5, 2023), DateMensuelle(12, 2023)): 11.52,
            DateMensuelleInterval(DateMensuelle(1, 2024), DateMensuelle(12, 2024)): 11.65
        }

        self._taux_premier_tranche = {
            DateMensuelleInterval(DateMensuelle(11, 2010)): 0.2
        }

        self._taux_seconde_tranche = {
            DateMensuelleInterval(DateMensuelle(11, 2010)): 0.6
        }

        self._abattement_annuel_conjoint = {
            DateMensuelleInterval(DateMensuelle(1, 2022), DateMensuelle(10, 2023)): 5000
        }

        self._abattement_annuel_conjoint_par_enfant = {
            DateMensuelleInterval(DateMensuelle(1, 2022), DateMensuelle(10, 2023)): 1400
        }

    def __recherche_generique(self, dict):
        for interval, montant in dict.items():
            if self.date in interval:
                return montant
        return None  # Todo : raise IntervalNonImplémenté

    @property
    def AAH_TAUX_PLEIN(self):
        return self.__recherche_generique(self._aah_taux_plein)

    @property
    def SMIC_HORAIRE_BRUT(self):
        return self.__recherche_generique(self._smic_horaire_brut)

    @property
    def TAUX_PREMIERE_TRANCHE(self):
        return self.__recherche_generique(self._taux_premier_tranche)

    @property
    def TAUX_SECONDE_TRANCHE(self):
        return self.__recherche_generique(self._taux_seconde_tranche)

    @property
    def ABATTEMENT_ANNUEL_CONJOINT(self):
        return self.__recherche_generique(self._abattement_annuel_conjoint)

    @property
    def ABATTEMENT_ANNUEL_CONJOINT_PAR_ENFANT(self):
        return self.__recherche_generique(self._abattement_annuel_conjoint_par_enfant)
