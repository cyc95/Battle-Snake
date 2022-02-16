#include "library.h"
#include "BoardControl.h"
#include <memory>
extern "C" int getaction(int array_state[121], int you_snake_head[2], int opp_snake_head[2], int you_snake_length, int opp_snake_length, int you_snake_health, int opp_snake_health, int you_snake_direction, int opp_snake_direction, int simulation_time){
   // return (int)cyc::board_control(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health);
    auto* env = new cyc::simulation_environment(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction);
    auto* root_node = new cyc::uct_node(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction, 0, 0);
    int i,max=0,j;
    int possible_actions[3];
    mcts(env,root_node,simulation_time);
    max =0;
    cyc::get_possible_actions(&possible_actions[0],you_snake_direction);
    double values_mean[3], values_rate[3],values_min[3], values_max;

    // rate for you
    if (0) {
        for (i = 0; i < 3; i++) { //mean
            values_rate[i] = (double) 1 / 3;
        }
        //cyc::calculated_action_rate(values_mean, values_rate);
        // rate for opp
        for (i = 0; i < 3; i++) { //mean
            values_mean[i] =
                    -root_node->child_values[0][i] * values_rate[0] - root_node->child_values[1][i] * values_rate[1] -
                    root_node->child_values[2][i] * values_rate[2];
        }
        cyc::calculated_action_rate(values_mean, values_rate);
        for (i = 0; i < 3; i++) { //mean
            values_mean[i] =
                    root_node->child_values[i][0] * values_rate[0] + root_node->child_values[i][1] * values_rate[1] +
                    root_node->child_values[i][2] * values_rate[2];
        }
        for(i=0;i<3;i++){ //mean
            if(values_mean[i] > values_mean[max]) max=i;
        }
    }
    if(1){
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
    }

    delete env;
    delete root_node;
    return (int)possible_actions[max];
}

