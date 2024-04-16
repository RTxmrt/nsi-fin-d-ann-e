from random import randint

def attaquer(dico_nom_pv, joueur, adversaire):
    coup = randint(10, 20) #// (2 if adversaire.defense else 1)
    print(joueure)
    print(adversaire)
    dico_nom_pv[adversaire] -= coup
    print(f"{joueur} attaque {adversaire} et lui inflige {coup} points de dégâts.")

def defendre(nom):
    defense = True
    print(f"{nom} se met en position de défense.")
    
def main():
    print("Bienvenue dans le jeu de combat textuel !")
    dico_nom_pv = {}
    joueur1 = input("Entrez le nom du joueur 1 ")
    joueur2 = input("Entrez le nom du joueur 2 ")
    dico_nom_pv[joueur1] = 100
    dico_nom_pv[joueur2] = 100
    print(dico_nom_pv)
    
    while dico_nom_pv[joueur1] > 0 and dico_nom_pv[joueur2] > 0:
        for joueur in  dico_nom_pv:
            adversaire = 
            rep_joueur = input("Voulez vous attaquer ou vous défendre (a, d): ")
            if rep_joueur == 'a':
                attaquer(dico_nom_pv, joueur, adversaire)
            else:
                defendre()
            
main()