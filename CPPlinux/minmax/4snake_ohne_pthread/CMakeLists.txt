cmake_minimum_required(VERSION 3.21)
project(snake_4)

set(CMAKE_CXX_STANDARD 14)

add_library(snake_4 SHARED library.cpp simulator_environment.cpp simulator_environment.h uct_node.h BoardControl.cpp BoardControl.h mcts.cpp mcts.h uct_node.cpp A_Algorithmus.h A_Algorithmus.cpp)
