cmake_minimum_required(VERSION 3.21)
project (untitled2)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} "-static -static-libgcc -static-libstdc++")

add_library(untitled2  SHARED library.cpp simulator_environment.cpp simulator_environment.h uct_node.h BoardControl.cpp BoardControl.h mcts.cpp mcts.h)
