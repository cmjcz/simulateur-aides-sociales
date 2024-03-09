from calculateur_aah import CalculateurAAH
from personne import Personne
from ressource import Ressource
from date_mensuelle import DateMensuelle
from datetime import date
from foyer import Foyer

RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'


def check(resultat, resultat_attendu):
    if resultat == resultat_attendu:
        status = GREEN + "[PASS]" + RESET
    else:
        status = RED + "[FAIL]" + RESET
    print(f"{status} Attendu : {resultat_attendu}€ Résultat : {resultat}€")


def test_celib(
        nom_test: str,
        allocataire: Personne,
        revenu_mensuel: int,
        resultat_attendu,
        *enfants: Personne
        ):
    print(nom_test)
    foyer = Foyer(allocataire=allocataire)
    for enfant in enfants:
        foyer.ajouter_personne_a_charge(enfant)

    mois_teste = DateMensuelle(3, 2024)
    calculateur = CalculateurAAH(foyer)
    ressources_decembre = Ressource(revenu_mensuel, DateMensuelle(12, 2023))
    ressources_janvier = Ressource(revenu_mensuel, DateMensuelle(1, 2024))
    ressources_fevrier = Ressource(revenu_mensuel, DateMensuelle(2, 2024))
    allocataire.ajouter_ressource(ressources_decembre)
    allocataire.ajouter_ressource(ressources_janvier)
    allocataire.ajouter_ressource(ressources_fevrier)

    aah = calculateur.calculer_AAH(mois_teste)
    check(aah, resultat_attendu)


def test_couple(
        nom_test: str,
        allocataire: Personne,
        revenu_mensuel: int,
        partenaire: Personne,
        revenu_mensuel_partenaire: int,
        resultat_attendu,
        *enfants: Personne
        ):
    print(nom_test)
    mois_teste = DateMensuelle(3, 2024)
    foyer = Foyer(allocataire)
    foyer.definir_conjoint(conjoint=partenaire)
    for enfant in enfants:
        foyer.ajouter_personne_a_charge(enfant)

    calculateur = CalculateurAAH(foyer)
    ressources_decembre = Ressource(revenu_mensuel, DateMensuelle(12, 2023))
    ressources_janvier = Ressource(revenu_mensuel, DateMensuelle(1, 2024))
    ressources_fevrier = Ressource(revenu_mensuel, DateMensuelle(2, 2024))
    allocataire.ajouter_ressource(ressources_decembre)
    allocataire.ajouter_ressource(ressources_janvier)
    allocataire.ajouter_ressource(ressources_fevrier)

    ressources_decembre_partenaire = Ressource(revenu_mensuel_partenaire,
                                               DateMensuelle(12, 2023))
    ressources_janvie_partenaire = Ressource(revenu_mensuel_partenaire,
                                             DateMensuelle(1, 2024))
    ressources_fevrier_partenaire = Ressource(revenu_mensuel_partenaire,
                                              DateMensuelle(2, 2024))
    partenaire.ajouter_ressource(ressources_decembre_partenaire)
    partenaire.ajouter_ressource(ressources_janvie_partenaire)
    partenaire.ajouter_ressource(ressources_fevrier_partenaire)

    aah = calculateur.calculer_AAH(mois_teste)
    check(aah, resultat_attendu)


def main():
    naissance_cynthia = date(1999, 7, 23)
    cynthia = Personne("Cynthia", naissance_cynthia)
    test_celib("Test célib sans ressources", cynthia, 0, 971.37)
    test_celib("Test célib avec 500€ / mois", cynthia, 500, 871.37)
    test_celib("Test célib avec 1k€ / mois", cynthia, 1000, 581.04)
    test_celib("Test célib avec 1,5k€ / mois", cynthia, 1500, 281.04)

    naissance_juliette = date(1999, 7, 24)
    juliette = Personne("Juliette", naissance_juliette)
    test_couple("Test couple allocataire travaille 1,5k€ / mois",
                cynthia, 1500,
                juliette, 0,
                971.37)
    test_couple("Test couple, allocataire travaille 1,5k€ / mois, "
                "conjoint 750€ / mois",
                cynthia, 1500,
                juliette, 750,
                734.52)
    test_couple("Test couple conjoint travaille 1,5k€ /mois",
                cynthia, 0,
                juliette, 1500,
                674.85)

    naissance_enzo = date(2020, 12, 15)
    enzo = Personne("Enzo", naissance_enzo)
    test_celib("Test célib avec enfant",
               cynthia, 1500,
               674.44,
               enzo)
    test_couple("Test couple, conjoint 2k€/mois, avec enfant",
                cynthia, 0,
                juliette, 2000,
                684.92,
                enzo)


if __name__ == "__main__":
    main()
