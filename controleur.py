from calculateur_aah import CalculateurAAH
from personne import Personne
from datetime import date
from date_mensuelle import DateMensuelle
from ressource import Ressource


class Controleur:
    def __init__(self, vue):
        self.vue = vue

    def __aujourdhui(self):
        """
        Retourne le mois en cours
        Sous un objet DateMensuelle
        """
        today = date.today()
        mois = today.month
        annee = today.year
        return DateMensuelle(mois, annee)

    def demarrer_vue(self):
        self.vue.message_bienvenue()

    def __recuperer_personne(self, nom):
        """
        Méthode générique pour générer des Personne
        Les autres méthodes ne font que l’encapsuler
        """
        date_naissance = self.vue.demander_date_naissance(nom)
        personne = Personne(nom, date_naissance)
        aujourdhui = self.__aujourdhui()
        for mois in range(1, 4):
            montant = self.vue.demander_ressource(nom, aujourdhui - mois)
            ressource = Ressource(montant, aujourdhui - mois)
            personne.ajouter_ressource(ressource)
        return personne

    def recuperer_allocataire(self):
        """"
        Communique avec la vue pour générer une Personne
        correspondant à l’allocataire
        """
        nom = self.vue.demander_nom_allocataire()
        return self.__recuperer_personne(nom)

    def recuperer_conjoint(self):
        """"
        Communique avec la vue pour générer une Personne
        correspondant au conjoint
        """
        a_conjoint = self.vue.demander_si_conjoint()
        if a_conjoint:
            nom = self.vue.demander_nom_conjoint()
            return self.__recuperer_personne(nom)
        return None

    def recuperer_personnes_a_charge(self):
        """
        Communique avec la vue pour générer une collection de personnes à charge
        Retourne la collection
        """
        a_personne_a_charge = self.vue.demande_si_personne_a_charge()
        personnes_a_charge = []
        while a_personne_a_charge:
            nom = self.vue.demander_nom_personne_a_charge()
            personne = self.__recuperer_personne(nom)
            personnes_a_charge.append(personne)
            a_personne_a_charge = self.vue.demande_si_personne_a_charge()
        return personnes_a_charge

    def definir_mois_simule(self):
        return self.__aujourdhui()

    def calculer_aah(self,
                     date: DateMensuelle,
                     allocataire: Personne,
                     conjoint: Personne,
                     *personnes_a_charge):
        """
        Exécute le calcul de l’AAH avec le calculateur, et retourne le résultat

        Paramètres:
            date (DateMensuelle): mois sur lequel calculer l’AAH
            allocataire (Personne): Allocataire pour lequel calculer l’aide
            conjoint (Personne): Conjoint de l’allocataire si
                                    le calcul est conjugalisé
            personnes_a_charge: collection de Personne à charge
        """
        calculateur = CalculateurAAH(allocataire)
        if conjoint is not None:
            calculateur.definir_conjoint(conjoint)
        for personne in personnes_a_charge:
            calculateur.ajouter_personne_a_charge(personne)
        aah = calculateur.calculer_AAH(date)
        return aah

    def afficher_resultat_aah(self, montant_aah):
        self.vue.afficher_resultat_calcul("aah", montant_aah)

    def run(self):
        self.demarrer_vue()
        allocataire = self.recuperer_allocataire()
        conjoint = self.recuperer_conjoint()
        personnes_a_charge = self.recuperer_personnes_a_charge()
        mois = self.definir_mois_simule()
        montant_aah = self.calculer_aah(mois,
                                        allocataire,
                                        conjoint,
                                        personnes_a_charge)
        self.afficher_resultat_aah(montant_aah)
