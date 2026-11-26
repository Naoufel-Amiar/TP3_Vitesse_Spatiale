#include <iostream>
#include <vector>
#include <exception>

#include "chargement.h"
#include "vaisseaux.h"
#include "planetes.h"

int main()
{
    try
    {
        // ==================== VAISSEAUX ====================

        std::cout << "===== CHARGEMENT DES VAISSEAUX ====="
                  << std::endl;

        std::vector<Vaisseau> vaisseaux =
            Chargement::chargerVaisseaux("../data/VAISSEAUX.txt");

        std::cout << "Nombre de vaisseaux charges : "
                  << vaisseaux.size() << std::endl;

        for (const Vaisseau& vaisseau : vaisseaux)
        {
            vaisseau.afficher();
            std::cout << "--------------------" << std::endl;
        }

        // ==================== PLANETES ====================

        std::cout << "\n===== CHARGEMENT DES PLANETES ====="
                  << std::endl;

        std::vector<Planetes> planetes =
            Chargement::chargerPlanetes("../data/PLANETES.txt");

        std::cout << "Nombre de planetes chargees : "
                  << planetes.size() << std::endl;

        // ==================== RESULTAT ====================

        std::cout << "\nChargement termine avec succes."
                  << std::endl;
    }
    catch (const std::exception& erreur)
    {
        std::cerr << "ERREUR : " << erreur.what() << std::endl;
        return 1;
    }

    return 0;
}