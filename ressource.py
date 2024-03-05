class Ressource:
    """
    Représente un couple ressource / date de la ressource

    Attributs:
        montant: montant de la ressource
        date: date de la ressource
    """

    def __init__(self, montant, date) -> None:
        self.montant = montant
        self.date = date

    def __str__(self) -> str:
        return f"Ressource à date du {self.date} : {self.montant}€"
