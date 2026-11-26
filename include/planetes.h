#ifndef PLANETES_H
#define PLANETES_H


Planetes::Planetes(std::string name, int x, int y, int population, std::string nation, float fuelPrice) {
    Name_ = name;
    x_ = x;
    y_ = y;
    population_ = population;
    Nation_ = nation;
    FuelPrice_ = fuelPrice;
}

#endif