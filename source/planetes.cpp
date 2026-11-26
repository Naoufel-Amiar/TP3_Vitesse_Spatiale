#include "planetes.h"

Planetes::Planetes(
    std::string name,
    double x,
    double y,
    long long population,
    std::string nation,
    double fuelPrice
)
{
    Name_ = name;
    x_ = x;
    y_ = y;
    population_ = population;
    Nation_ = nation;
    FuelPrice_ = fuelPrice;
}