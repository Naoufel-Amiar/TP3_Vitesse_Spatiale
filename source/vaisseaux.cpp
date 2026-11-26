#include "vaisseaux.h"
#include <iostream>

// Constructeur par defaut
Vaisseau::Vaisseau()
    : modele(""), capacite(0.0)
{
}

// Constructeur parametre
Vaisseau::Vaisseau(const std::string& modele, double capacite)
    : modele(modele), capacite(capacite)
{
}

// ==================== GETTERS ====================

std::string Vaisseau::getModele() const
{
    return modele;
}

double Vaisseau::getCapacite() const
{
    return capacite;
}

// ==================== SETTERS ====================

void Vaisseau::setModele(const std::string& modele)
{
    this->modele = modele;
}

void Vaisseau::setCapacite(double capacite)
{
    this->capacite = capacite;
}

// ==================== METHODES ====================

// Verifie si le vaisseau peut parcourir une distance
bool Vaisseau::peutParcourir(double distance) const
{
    return distance >= 0.0 && distance <= capacite;
}

// Affiche les informations du vaisseau
void Vaisseau::afficher() const
{
    std::cout << "Modele : " << modele << std::endl;
    std::cout << "Capacite : " << capacite << std::endl;
}