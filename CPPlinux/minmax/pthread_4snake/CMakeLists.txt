cmake_minimum_required(VERSION 3.21)
project(pthread_4snake)

set(CMAKE_CXX_STANDARD 14)

add_library(snake4_ohne_pthread SHARED library.cpp simulator_environment.cpp simulator_environment.h uct_node.h BoardControl.cpp BoardControl.h mcts.cpp mcts.h uct_node.cpp)
