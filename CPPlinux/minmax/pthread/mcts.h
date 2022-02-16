//
// Created by Yuancong Chen on 2021/12/15.
//

#ifndef UNTITLED2_MCTS_H
#define UNTITLED2_MCTS_H
#include "uct_node.h"
#include "simulator_environment.h"

int mcts(cyc::simulation_environment* env, cyc::uct_node* p, const int &simulation_time);
namespace cyc {
    void *expand_thread1(void *arg);
    void *expand_thread2(void *arg);
    void *expand_thread3(void *arg);
    void *expand_thread4(void *arg);
    void *expand_thread5(void *arg);
    void *expand_thread6(void *arg);
    void *expand_thread7(void *arg);
    void *expand_thread8(void *arg);
    void *expand_thread9(void *arg);
}
#endif //UNTITLED2_MCTS_H
