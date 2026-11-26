#ifndef CHARGEMENT_H
#define CHARGEMENT_H

#include <string>
#include <vector>

#include "vaisseaux.h"
#include "planetes.h"

class Chargement
{
public:

    // Chargement des vaisseaux
    static std::vector<Vaisseau> chargerVaisseaux(
        const std::string& fichier
    );

    // Chargement des planetes
    static std::vector<Planetes> chargerPlanetes(
        const std::string& fichier
    );
};

#endif