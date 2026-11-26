#include <iostream>
#include <string>
#include "../include/planetes.h"


using namespace std;

Planetes::Planetes(string name, int x, int y, int population, string nation, float fuelPrice) {
    Name_ = name;
    x_ = x;
    y_ = y;
    population_ = population;
    Nation_ = nation;
    FuelPrice_ = fuelPrice;
}

