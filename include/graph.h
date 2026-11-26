#include <iostream>
#include <string>
#include <vector>
#include "planetes.h"


#ifndef GRAPH_H
#define GRAPH_H


class Graph {
private:
    std::vector<Planetes> PlanetesList; // Liste des planètes
    std::vector<std::vector<int>> Matrix; // Matrice d'adjacence

    void GetPlaneteListe(std::vector<Planetes>&);
public:    
};


#endif