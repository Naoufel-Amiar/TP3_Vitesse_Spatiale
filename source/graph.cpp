#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include "../include/graph.h"


using namespace std;


Graph::Graph(std::vector<Planetes> planeteListFull) {
    PlanetesList_ = planeteListFull;
    n = PlanetesList_.size();
    Matrix_.assign(n, std::vector<int>(n, -1));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            Matrix_.at(i).at(j) = sqrt(pow(PlanetesList_.at(i).GetX() - PlanetesList_.at(j).GetX(), 2) + pow(PlanetesList_.at(i).GetY() - PlanetesList_.at(j).GetY(), 2));
        }
    }
}

void Graph::AfficherMatAdj(){
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            std::cout << Matrix_.at(i).at(j) << " ";
        }
        std::cout << std::endl;
    }
}

