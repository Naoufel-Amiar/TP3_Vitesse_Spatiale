#ifndef PLANETES_H
#define PLANETES_H

#include <string>

class Planetes
{
private:

    std::string Name_;
    double x_;
    double y_;
    long long population_;
    std::string Nation_;
    double FuelPrice_;

public:

    // Constructeur
    Planetes(
        std::string name,
        double x,
        double y,
        long long population,
        std::string nation,
        double fuelPrice
    );
};

#endif