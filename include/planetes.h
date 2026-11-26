#ifndef PLANETES_H
#define PLANETES_H


class Planetes {

private:

    std::string Name_;
    int x_;
    int y_;
    int population_;
    std::string Nation_;
    float FuelPrice_;


public:
    Planetes(std::string name, int x, int y, int population, std::string nation, float fuelPrice);

    
};

#endif