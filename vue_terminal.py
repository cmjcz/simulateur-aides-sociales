class VueTerminal:
    def __init__(self) -> None:
        pass

    def message_bienvenue(self):
        print("Bienvenue dans le simulateur d’aides sociales\n"
              "Actuellement il ne permet que de tester le "
              "calcul de l’AAH")
        
    def __yes_no_input(self):
        reponse = input()
        match reponse:
            case "y":
                return True
            case "n":
                return False

    def demander_nom_allocataire(self):
        print("Veuillez entrer le nom de l’allocataire")
        nom = input()
        return nom

    def demander_si_conjoint(self):
        print("Avez vous un ou une conjoint·e ? (y/n)")
        return self.__yes_no_input()

    def demander_nom_conjoint(self):
        print("Veuillez entrer le nom du conjoint")
        nom = input()
        return nom

    def demande_si_personne_a_charge(self):
        print("Avez vous une personne a charge ? (y/n)")
        return self.__yes_no_input()

    def demander_nom_personne_a_charge(self):
        print("Veuillez entrer le nom de la personne")
        nom = input()
        return nom

    def demander_date_naissance(self, nom):
        return "01/01/1970"

    def demander_ressource(self, nom, date):
        print(f"Combien {nom} a gagné en {date} ?")
        try:
            montant = int(input())
        except ValueError:
            montant = None
        return montant

    def afficher_resultat_calcul(self, nom_aide, resultat):
        print(f"Montant de {nom_aide} : {resultat}€")
