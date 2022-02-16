#include "library.h"
#include "BoardControl.h"
#include <memory>
#include "A_Algorithmus.h"
extern "C" int getaction(int array_state[121], int you_snake_head[2], int opp_snake_head[2], int you_snake_length, int opp_snake_length, int you_snake_health, int opp_snake_health, int you_snake_direction, int opp_snake_direction, int simulation_time){
    // return (int)cyc::board_control(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health);
    auto* env = new cyc::simulation_environment(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction);
    auto* root_node = new cyc::uct_node(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction, 0, 0);
    int i,max=0,j;
    int possible_actions[3];
    bool action_A_search[3] = {false, false, false};
    int action_a=0;
    bool flag = false;
    mcts(env,root_node,simulation_time);
    max =0;
    cyc::get_possible_actions(&possible_actions[0],you_snake_direction);
    // here is not A* search. A* search cost too much time.(Because sometimes there are much food) I simplified the algorithm
    cyc::action_A_algorithm(array_state,you_snake_head,action_A_search,you_snake_direction);
    double values_min[3];

    for(i=0;i<3;i++){ // min
        values_min[i] =121;
    }
    for(i=0;i<3;i++){ //min
        for(j=0;j<3;j++){ //min
            if(values_min[i] > root_node->child_values[i][j])  values_min[i] = root_node->child_values[i][j];
        }
    }

    for(i=0;i<3;i++){ //mean
        if(values_min[max]  < values_min[i])  max  = i;
    }

    if(!action_A_search[max]) {
        for(i=0;i<3;i++){
            if(action_A_search[i] && !flag) {
                action_a = i;
                flag = true;
            }
            if(action_A_search[i] && flag) {
                if(values_min[action_a] < values_min[i])action_a = i;
            }
        }
       // if(( you_snake_length < 5 || you_snake_health <20)  && values_min[action_a] > -20 && values_min[max] - values_min[action_a] < 25 && values_min[max] < 80 && action_A_search[action_a]) max = action_a;
        if(/*you_snake_length > opp_snake_length &&*/ you_snake_length - opp_snake_length <= 8 && (you_snake_length + opp_snake_length) >= 23 && (you_snake_length + opp_snake_length) < 33 && values_min[action_a] > 0 && values_min[max] - values_min[action_a] < 25 && values_min[max] < 80 &&action_A_search[action_a]) max = action_a;
        if(/*you_snake_length > opp_snake_length &&*/ you_snake_length > opp_snake_length && you_snake_length - opp_snake_length <= 8  && (you_snake_length + opp_snake_length) >= 13 && (you_snake_length + opp_snake_length) < 23 && values_min[action_a] > -30 && values_min[max] < 110 &&action_A_search[action_a]) max = action_a;
        if(/*you_snake_length > opp_snake_length &&*/ you_snake_length <= opp_snake_length && (you_snake_length + opp_snake_length) >= 13 && (you_snake_length + opp_snake_length) < 23 && values_min[action_a] > -60 && values_min[max] < 110 &&action_A_search[action_a]) max = action_a;
        if(/*you_snake_length > opp_snake_length &&*/you_snake_length > opp_snake_length &&  (you_snake_length + opp_snake_length) >= 8 && (you_snake_length + opp_snake_length)  < 13 && values_min[action_a] > -80 &&action_A_search[action_a]) max = action_a;
        if(/*you_snake_length > opp_snake_length &&*/((you_snake_length <=  opp_snake_length &&  (you_snake_length + opp_snake_length) >= 8 && (you_snake_length + opp_snake_length)  < 13) || you_snake_length <=5 )&& values_min[action_a] > -100 &&action_A_search[action_a]) max = action_a;
        if(/*you_snake_length > opp_snake_length &&*/(you_snake_length + opp_snake_length)  < 8 && values_min[action_a] > -100 &&action_A_search[action_a]) max = action_a;
        if(you_snake_health < 14 && values_min[action_a] > -60) max = action_a;
 }

    delete env;
    delete root_node;
    // return kkk;
    return (int)possible_actions[max];
}