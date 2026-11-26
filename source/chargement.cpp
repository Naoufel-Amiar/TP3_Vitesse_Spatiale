#include "chargement.h"

#include <fstream>
#include <stdexcept>

// ==================== VAISSEAUX ====================

std::vector<Vaisseau> Chargement::chargerVaisseaux(
    const std::string& fichier)
{
    std::vector<Vaisseau> vaisseaux;

    std::ifstream flux(fichier);

    if (!flux.is_open())
    {
        throw std::runtime_error(
            "Impossible d'ouvrir le fichier : " + fichier
        );
    }

    std::string modele;
    double capacite;

    while (flux >> modele >> capacite)
    {
        vaisseaux.emplace_back(modele, capacite);
    }

    return vaisseaux;
}

// ==================== PLANETES ====================

std::vector<Planete> Chargement::chargerPlanetes(
    const std::string& fichier)
{
    std::vector<Planete> planetes;

    std::ifstream flux(fichier);

    if (!flux.is_open())
    {
        throw std::runtime_error(
            "Impossible d'ouvrir le fichier : " + fichier
        );
    }

    std::string nom;
    double x;
    double y;
    long long population;
    std::string nation;
    double prixCarburant;

    while (flux >> nom >> x >> y >> population
                >> nation >> prixCarburant)
    {
        planetes.emplace_back(
            nom,
            x,
            y,
            population,
            nation,
            prixCarburant
        );
    }

    return planetes;
}