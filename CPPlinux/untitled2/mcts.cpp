//
// Created by Yuancong Chen on 2021/12/15.
//
#include "uct_node.h"
#include "simulator_environment.h"

#include "mcts.h"


int mcts(cyc::simulation_environment* env, cyc::uct_node* root_node, const int &simulation_time){
    int i = 0, sum=0;
    //SYSTEMTIME s_time;
    //GetLocalTime(&s_time);
    //int alt_time;
    //alt_time = (int) s_time.wSecond * 1000 + (int) s_time.wMilliseconds;
    //int new_time = alt_time;
    cyc::uct_node* current_node;
    while(/*(new_time - alt_time) < simulation_time && ! root_node->checked*/i<2000 && (i<9 || simulation_time >= 1)){
        /*
        if(i%100 == 0) {
            GetLocalTime(&s_time);
            new_time = (int) s_time.wSecond * 1000 + (int) s_time.wMilliseconds;
            if (new_time < alt_time) new_time = new_time + 60000;
        }*/
        current_node = root_node->select();
        i++;
        if(current_node == nullptr) continue;
        current_node->expand(env);
        current_node->backup();
    }

    sum=root_node->sum_child_visits();

    return sum;
}
