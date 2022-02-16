#include "library.h"
#include "BoardControl.h"
#include "A_Algorithmus.h"
extern "C" int getaction(int array_state[121], int you_snake_head[2], int opp_snake_head[6], int you_snake_length, int opp_snake_length[3], int you_snake_health, int opp_snake_health[3], int you_snake_direction, int opp_snake_direction[3], int simulation_time){
    // return (int)cyc::board_control(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health);
    int nulllll[3] = {0,0,0};
    auto* env = new cyc::simulation_environment(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction);
    auto* root_node = new cyc::uct_node(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction, 0, nulllll);
    int i,max=0,j;
    int possible_actions[3] ;
    bool action_A_search[3] = {false, false, false};
    int  t,d;
    int action_a=0;
    double values_min[3][3], test[3]={121,121,121};
    bool flag = false;
    mcts(env,root_node,simulation_time);
    max =0;
    cyc::get_possible_actions(&possible_actions[0],you_snake_direction);
    cyc::action_A_algorithm(array_state,you_snake_head,action_A_search,you_snake_direction);

    int values_max_num2[3][3], values_max_num3[3][3][3];
    int values_max_num[3]={0,0,0};
    for(i=0;i<3;i++){ // min
        for(j=0;j<3;j++) { // min
            values_max_num2[i][j] = 0;
            for(t=0;t<3;t++){
                values_max_num3[i][j][t] = 0;
            }
        }
    }
    //cyc::calculated_action_rate(values_mean, values_rate);
    // rate for opp
    for(i=0;i<3;i++){ //min
        for(j=0;j<3;j++){ //min
            for(t=0;t<3;t++) {
                for (d = 0; d < 3; d++) {
                    if (root_node->child_values[i][j][t][values_max_num3[i][j][t]][3] < root_node->child_values[i][j][t][d][3]) values_max_num3[i][j][t] = d;
                }
            }
        }
    }
    for(i=0;i<3;i++){ //min
        for(j=0;j<3;j++){ //min
            for(t=0;t<3;t++) {
                if (root_node->child_values[i][j][values_max_num2[i][j]][values_max_num3[i][j][values_max_num2[i][j]]][2] < root_node->child_values[i][j][t][values_max_num3[i][j][t]][2]) values_max_num2[i][j] = t;
            }
        }
    }
    for(i=0;i<3;i++){ // min
        for(j=0;j<3;j++) { // min
            if (root_node->child_values[i][values_max_num[i]][values_max_num2[i][values_max_num[i]]][values_max_num3[i][values_max_num[i]][values_max_num2[i][values_max_num[i]]]][1] < root_node->child_values[i][j][values_max_num2[i][j]][values_max_num3[i][j][values_max_num2[i][j]]][1]) values_max_num[i] = j;
            //   this->child_values[i][j]                [values_max_num2[i][j                ]][values_max_num3[i][j]                [values_max_num2[i][j                ]]][1]
        }
    }

    for(i=0;i<3;i++){ //max
        test[i] = root_node->child_values[i][values_max_num[i]][values_max_num2[i][values_max_num[i]]][values_max_num3[i][values_max_num[i]][values_max_num2[i][values_max_num[i]]]][0];
    }
    for(i=0;i<3;i++){ //max
        if(test[max]  < test[i])  max  = i;
    }

    if(!action_A_search[max]) {
        for(i=0;i<3;i++){
            if(action_A_search[i] && !flag) {
                action_a = i;
                flag = true;
            }
            if(action_A_search[i] && flag) {
                if(test[action_a] < test[i])action_a = i;
            }
        }
        int max_opp_length=0;
        for(i=0;i<3;i++){
            if(max_opp_length<*(opp_snake_length+i)) max_opp_length =*(opp_snake_length+i);
        }
        if(you_snake_length < 5   && test[action_a] > 5 && action_A_search[action_a]) max = action_a;
        if(you_snake_health > 80 && you_snake_length >= 5  && you_snake_length < max_opp_length + 4  && test[action_a] > 20  && test[max] < 60 && action_A_search[action_a]) max = action_a;
        if(you_snake_health <= 80 && test[action_a] > 20 && test[max] < 60 && action_A_search[action_a]) max = action_a;
        if(you_snake_health <= 60 && test[action_a] > 12 && action_A_search[action_a]) max = action_a;
        if(you_snake_health <= 30 && test[action_a] > 8  && action_A_search[action_a]) max = action_a;
        if(you_snake_health <= 10 && test[action_a] > 5  && action_A_search[action_a]) max = action_a;
    }
    delete env;
    delete root_node;
    // return kkk;
    return (int)possible_actions[max];
}