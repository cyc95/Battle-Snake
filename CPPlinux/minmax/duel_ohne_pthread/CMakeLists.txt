cmake_minimum_required(VERSION 3.21)
project(untitled)

set(CMAKE_CXX_STANDARD 14)

add_library(untitled SHARED library.cpp simulator_environment.cpp simulator_environment.h uct_node.h BoardControl.cpp BoardControl.h mcts.cpp mcts.h uct_node.cpp A_Algorithmus.cpp A_Algorithmus.h)
