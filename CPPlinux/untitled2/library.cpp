#include "library.h"
#include "BoardControl.h"

extern "C" int getaction(int array_state[121], int you_snake_head[2], int opp_snake_head[2], int you_snake_length, int opp_snake_length, int you_snake_health, int opp_snake_health, int you_snake_direction, int opp_snake_direction, int simulation_time){
   // return (int)cyc::board_control(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health);
    auto* env = new cyc::simulation_environment(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction);
    auto* root_node = new cyc::uct_node(array_state, you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction, 0, 0);
    int i,max=0;
    int possible_actions[3];
    int new_position[3][2];
    float values[3];


    mcts(env,root_node,simulation_time);
    max =0;
    cyc::get_possible_actions(&possible_actions[0],you_snake_direction);

    for(i=0;i<3;i++){ //mean
        //cyc::get_new_position(&new_position[i][0], possible_actions[i]);
        values[i] = (root_node->child_values[i][0]+root_node->child_values[i][1]+root_node->child_values[i][2])/3;
        /*
        if(new_position[i][0]>0 && new_position[i][0]<10 && new_position[i][1]>0 && new_position[i][1]<10){
            if(array_state[new_position[i][0]*11+new_position[i][0]] == 500) values[i] += (300 / (float )you_snake_health);
            if(new_position[i][0] - 1 >0 && new_position[i][0] - 1<10 && new_position[i][1]>0 && new_position[i][1]<10){
                if(array_state[new_position[i][0]*11-11+new_position[i][0]] == 500) values[i] += (100 / (float)you_snake_health);
            }
            if(new_position[i][0] + 1 >0 && new_position[i][0] + 1<10 && new_position[i][1]>0 && new_position[i][1]<10){
                if(array_state[new_position[i][0]*11+11+new_position[i][0]] == 500) values[i] += (100 / (float)you_snake_health);
            }
            if(new_position[i][0] >0 && new_position[i][0]<10 && new_position[i][1] - 1 >0 && new_position[i][1] - 1 <10){
                if(array_state[new_position[i][0]*11-1+new_position[i][0]] == 500) values[i] += (100 / (float)you_snake_health);
            }
            if(new_position[i][0] >0 && new_position[i][0]<10 && new_position[i][1] + 1 >0 && new_position[i][1] + 1 <10){
                if(array_state[new_position[i][0]*11+1+new_position[i][0]] == 500) values[i] += (100 / (float)you_snake_health);
            }
        }
         */
    }

    for(i=0;i<3;i++){ //mean
        if(values[i] > values[max]) max=i;
    }
    delete env;
    delete root_node;
    return (int)possible_actions[max];
}

