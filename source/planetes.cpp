#include <iostream>
#include <string>
#include "planetes.h"


using namespace std;

class Planetes {

private:

    string Name_;
    int x_;
    int y_;
    int population_;
    string Nation_;
    float FuelPrice_;


public:
    planetes(std::string name, int x, int y, int population, std::string nation, float fuelPrice);
    

};