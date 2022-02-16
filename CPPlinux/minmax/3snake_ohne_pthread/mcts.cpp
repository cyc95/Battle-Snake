//
// Created by Yuancong Chen on 2021/12/15.
//
#include "uct_node.h"
#include "simulator_environment.h"
#include <sys/time.h>
#include "mcts.h"


int mcts(cyc::simulation_environment* env, cyc::uct_node* root_node, const int &simulation_time){
    int i = 0;
    struct timeval time_now{};
    gettimeofday(&time_now, nullptr);
    int alt_time;
    alt_time = (int)(time_now.tv_sec * 1000) + (int)(time_now.tv_usec / 1000);
    int new_time = alt_time;
    cyc::uct_node* current_node;
    while((new_time - alt_time) < simulation_time && ! root_node->checked && i< 20000 && (i<9 || simulation_time >= 1)){
        if(i%4 == 0) {
            gettimeofday(&time_now, nullptr);
            new_time = (int)(time_now.tv_sec * 1000) + (int)(time_now.tv_usec / 1000);
            if (new_time < alt_time) new_time = new_time + 60000;
        }
        current_node = root_node->select();
        i++;
        if(current_node == nullptr) continue;
        cyc::expand(env,current_node);
        current_node->backup();
    }
    return 0;
}