#include <iostream>
#include <string>
#include <vector>
#include "planetes.h"


#ifndef GRAPH_H
#define GRAPH_H


class Graph {
private:
    std::vector<Planetes> PlanetesList_; // Liste des planètes
    std::vector<std::vector<int>> Matrix_; // Matrice d'adjacence
    int n;

public:    
    Graph(std::vector<Planetes> planeteListFull);
    void AfficherMatAdj();


};


#endif