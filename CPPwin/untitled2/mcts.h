//
// Created by Yuancong Chen on 2021/12/15.
//

#ifndef UNTITLED2_MCTS_H
#define UNTITLED2_MCTS_H
#include "uct_node.h"
#include "simulator_environment.h"
#include <windows.h>

int mcts(cyc::simulation_environment* env, cyc::uct_node* p, const int &simulation_time);

#endif //UNTITLED2_MCTS_H
