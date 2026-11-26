#include <iostream>
#include "vaisseaux.h"

int main()
{
    Vaisseau vaisseau("Asp-Explorer", 850.0);

    vaisseau.afficher();

    std::cout << std::boolalpha;

    std::cout << "Distance 500 : "
              << vaisseau.peutParcourir(500) << std::endl;

    std::cout << "Distance 850 : "
              << vaisseau.peutParcourir(850) << std::endl;

    std::cout << "Distance 900 : "
              << vaisseau.peutParcourir(900) << std::endl;

    return 0;
}