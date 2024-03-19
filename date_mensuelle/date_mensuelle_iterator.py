class DateMensuelleIterator:
    """
    Cet intérateur permet de générer des objets DateMensuelle
    À la manière de la fonction range()
    La date de fin est optionnelle, si jamais elle n’est pas renseignée
    l’itérateur génèrera à l’infini des dates
    """
    def __init__(self, date_debut, date_fin=None, pas=1) -> None:
        self.debut = date_debut
        self.fin = date_fin
        self.pas = pas

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.fin is not None:
            if self.debut + self.index >= self.fin:
                raise StopIteration
        date = self.debut + self.index
        self.index += self.pas
        return date


def date_mensuelle_range(debut, fin=None, pas=1):
    iterator = DateMensuelleIterator(debut, fin, pas)
    return iterator
