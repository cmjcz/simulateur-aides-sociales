def plafond(nombre, plafond):
    """
    Paramètres:
        nombre: nombre à plafonner
        plafond: plafond à appliquer

    Return:
        le nombre si il est inférieur au plafond
        le plafond si le nombre est plus grand
    """
    if nombre > plafond:
        return plafond
    return nombre


def plancher(nombre, plancher):
    """
    Paramètres:
        nombre: nombre à plancher
        plafond: plancher à appliquer

    Return:
        le nombre si il est supérieur au plancher
        le plancher si le nombre est plus petit
    """
    if nombre < plancher:
        return plancher
    return nombre


def abattement(nombre, abattement):
    """
    Soustrait l’abattement au nombre
    Permet purement d’avoir une version plus
    légale de la soustraction afin de faciliter
    la compréhension de l’algorithme
    """
    return nombre - abattement
