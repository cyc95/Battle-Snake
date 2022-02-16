#ifndef UNTITLED2_LIBRARY_H
#define UNTITLED2_LIBRARY_H
#include "simulator_environment.h"
#include "uct_node.h"
#include "mcts.h"

extern "C" int getaction(int array_state[121], int you_snake_head[2], int opp_snake_head[2], int you_snake_length, int opp_snake_length, int you_snake_health, int opp_snake_health, int you_snake_direction, int opp_snake_direction, int simulation_time);

#endif //UNTITLED2_LIBRARY_H
