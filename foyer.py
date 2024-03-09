from date_mensuelle import DateMensuelle

class Foyer:
    """
    Objet permettant de stocker toutes les informations
    relatives à un foyer (composition, ressources)
    """
    def __init__(self, allocataire) -> None:
        self._allocataire = allocataire
        self.conjoint = None
        self.personnes_a_charge = []

    @property
    def allocataire(self):
        return self._allocataire

    def definir_conjoint(self, conjoint):
        """
        Définit le conjoint pour le calcul
        Paramètres:
            conjoint (Personne): conjoint·e de l’allocataire
        """
        self.conjoint = conjoint

    def ajouter_personne_a_charge(self, personne):
        """
        Ajoute une personne à charge au foyer

        Paramètres:
            personne (Personne): personne à charge à ajouter
        """
        self.personnes_a_charge.append(personne)

    def ressource_conjoint(self, mois: DateMensuelle):
        """
        Retourne le montant des ressources du conjoint
        pour un mois donné
        Si aucune ressource n’est renseignée, la méthode
        retourne 0
        """
        if not self.contient_conjoint():
            return 0
        ressource = self.conjoint.ressources.get(mois)
        if ressource is not None:
            return ressource.montant
        return 0

    def ressource_allocataire(self, mois: DateMensuelle):
        """
        Retourne le montant des ressources de l’allocataire
        pour un mois donné
        Si aucune ressource n’est renseignée, la méthode
        retourne 0
        """
        ressource = self.allocataire.ressources.get(mois)
        if ressource is not None:
            return ressource.montant
        return 0

    def nombre_personnes_a_charge(self):
        """
        Retourne le nombre de personnes à charge du foyer
        """
        return len(self.personnes_a_charge)

    def contient_conjoint(self):
        """
        Teste si le foyer contient un conjoint
        Retourne vrai si il y a un conjoint
        Faux sinon
        """
        return self.conjoint is not None

    def __str__(self) -> str:
        string = f"Foyer : [Allocataire: {self.allocataire}"
        if self.conjoint is not None:
            string += f", Conjoint·e : {self.conjoint}"
        for enfant in self.personnes_a_charge:
            string += f", {enfant}"
        string += "]"
        return string
