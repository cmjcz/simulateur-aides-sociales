from controleur import Controleur
from vue_terminal import VueTerminal


def main():
    vue = VueTerminal()
    controleur = Controleur(vue)
    controleur.run()


if __name__ == "__main__":
    main()
