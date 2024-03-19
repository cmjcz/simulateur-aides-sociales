class DateMensuelleInterval:
    """
    Cet objet permet de créer des intervals de DateMensuelle
    afin de simplifier les calcul
    """
    def __init__(self, date_debut=None, date_fin=None):
        self.date_debut = date_debut
        self.date_fin = date_fin

    def __contains__(self, key):
        if self.date_debut is None and self.date_fin is None:
            return True
        elif self.date_debut is None:
            return key <= self.date_fin
        elif self.date_fin is None:
            return self.date_debut <= key
        return self.date_debut <= key <= self.date_fin
