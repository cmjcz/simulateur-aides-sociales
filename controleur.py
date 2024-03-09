from calculateur_aah import CalculateurAAH
from personne import Personne
from datetime import date
from date_mensuelle import DateMensuelle
from ressource import Ressource
from foyer import Foyer


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

    def recuperer_conjoint(self, foyer: Foyer):
        """"
        Communique avec la vue pour générer une Personne
        correspondant au conjoint
        Le conjoint est ajouté au foyer passé en paramètre
        """
        a_conjoint = self.vue.demander_si_conjoint()
        if a_conjoint:
            nom = self.vue.demander_nom_conjoint()
            conjoint = self.__recuperer_personne(nom)
            foyer.definir_conjoint(conjoint)

    def recuperer_personnes_a_charge(self, foyer: Foyer):
        """
        Communique avec la vue pour générer une collection de personnes à charge
        Retourne la collection
        Les personnes a charge sont ajoutées au foyer passé en paramètre
        """
        self.afficher_foyer(foyer)
        a_personne_a_charge = self.vue.demande_si_personne_a_charge()
        while a_personne_a_charge:
            nom = self.vue.demander_nom_personne_a_charge()
            personne = self.__recuperer_personne(nom)
            foyer.ajouter_personne_a_charge(personne)
            self.afficher_foyer(foyer)
            a_personne_a_charge = self.vue.demande_si_personne_a_charge()

    def definir_mois_simule(self):
        return self.__aujourdhui()

    def calculer_aah(self,
                     date: DateMensuelle,
                     foyer: Foyer):
        """
        Exécute le calcul de l’AAH avec le calculateur, et retourne le résultat

        Paramètres:
            date (DateMensuelle): mois sur lequel calculer l’AAH
            allocataire (Personne): Allocataire pour lequel calculer l’aide
            conjoint (Personne): Conjoint de l’allocataire si
                                    le calcul est conjugalisé
            personnes_a_charge: collection de Personne à charge
        """
        calculateur = CalculateurAAH(foyer)
        aah = calculateur.calculer_AAH(date)
        return aah

    def afficher_resultat_aah(self, montant_aah):
        self.vue.afficher_resultat_calcul("aah", montant_aah)

    def afficher_foyer(self, foyer):
        self.vue.afficher_foyer(foyer)

    def run(self):
        self.demarrer_vue()
        allocataire = self.recuperer_allocataire()
        foyer = Foyer(allocataire)
        self.recuperer_conjoint(foyer)
        self.recuperer_personnes_a_charge(foyer)

        mois = self.definir_mois_simule()
        montant_aah = self.calculer_aah(mois, foyer)
        self.afficher_resultat_aah(montant_aah)
