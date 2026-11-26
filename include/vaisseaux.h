#ifndef VAISSEAU_H
#define VAISSEAU_H

#include <string>

class Vaisseau
{
private:

    // Attributs
    std::string modele;
    double capacite;

public:

    // Constructeurs
    Vaisseau();
    Vaisseau(const std::string& modele, double capacite);

    // Destructeur
    ~Vaisseau() = default;

    // Getters
    std::string getModele() const;
    double getCapacite() const;

    // Setters
    void setModele(const std::string& modele);
    void setCapacite(double capacite);

    // Methodes fonctionnelles
    bool peutParcourir(double distance) const;
    void afficher() const;
};

#endif