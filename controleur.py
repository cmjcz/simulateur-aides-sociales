from calculateur_aah.calculateur_aah import CalculateurAAH
from model.personne import Personne
from date_mensuelle.date_mensuelle import DateMensuelle
from model.ressource import Ressource
from model.foyer import Foyer
from calculateur_aah.calculateur_trimestre_reference_aah import CalculateurTrimestreReferenceAAH


class Controleur:
    def __init__(self, vue):
        self.vue = vue

    def demarrer_vue(self):
        self.vue.message_bienvenue()

    def __recuperer_personne(self, nom):
        """
        Méthode générique pour générer des Personne
        Les autres méthodes ne font que l’encapsuler
        """
        date_naissance = self.vue.demander_date_naissance(nom)
        personne = Personne(nom, date_naissance)
        for mois in self.definir_periode_reference_simulee():
            montant = self.vue.demander_ressource(nom, mois)
            ressource = Ressource(montant, mois)
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

    def definir_periode_reference_simulee(self):
        """
        Cette méthode sert à retourner une période de référence
        utilisée temporairement pour les tests du programme
        en attendant d’avoir une vue adaptée pour la calculer
        automatiquement
        On part du principe que l’AAH a été obtenue à partir de Décembre 2023
        et qu’on simule le mois de Mars 2024
        """
        calculateur = CalculateurTrimestreReferenceAAH(DateMensuelle(12, 2023))
        return calculateur.calculer_trimestre_reference(DateMensuelle(3, 2024))

    def calculer_aah(self,
                     periode_reference,
                     foyer: Foyer):
        """
        Exécute le calcul de l’AAH avec le calculateur, et retourne le résultat

        Paramètres:
            periode_reference: ensemble des mois sur lequel se baser pour calculer l’AAH
            foyer (Foyer): foyer pour lequel calculer l’AAH
        """
        calculateur = CalculateurAAH(foyer)
        aah = calculateur.calculer_AAH(periode_reference)
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

        periode_reference = self.definir_periode_reference_simulee()
        montant_aah = self.calculer_aah(periode_reference, foyer)
        self.afficher_resultat_aah(montant_aah)
