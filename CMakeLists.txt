cmake_minimum_required(VERSION 3.10)

project(TP3_Vitesse_Spatiale LANGUAGES CXX)

# Configuration du standard C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Fichiers sources
add_executable(TP3_Vitesse_Spatiale
    main.cpp
    source/vaisseaux.cpp
    source/planetes.cpp
    source/chargement.cpp
    source/graph.cpp
)

# Dossier des fichiers d'en-tete
target_include_directories(TP3_Vitesse_Spatiale PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Options de compilation
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(
        TP3_Vitesse_Spatiale PRIVATE
        -Wall -Wextra -Wpedantic
    )
endif()