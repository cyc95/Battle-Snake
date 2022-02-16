//
// Created by Yuancong Chen on 2021/12/18.
//

#include "uct_node.h"
#include <cmath>

#define PI 3.1415926


void cyc::calculated_action_rate(const double *child_values, double *action_rate){
    double sum;
    if(*child_values > 120.8){
        *action_rate = 1;
        *(action_rate+1) = 0;
        *(action_rate+2) = 0;
    }else {
        if(*(child_values + 1) > 120.8) {
            *action_rate = 0;
            *(action_rate + 1) = 1;
            *(action_rate + 2) = 0;
        }else {
            if(*(child_values + 2) > 120.8) {
                *action_rate = 0;
                *(action_rate + 1) = 0;
                *(action_rate + 2) = 1;
            }else{
                *action_rate =  tan((*child_values+121)/484*PI);
                *(action_rate + 1) = tan((*(child_values+1)+121)/484*PI);
                *(action_rate + 2) = tan((*(child_values+2)+121)/484*PI);
                sum = *action_rate + *(action_rate + 1) +  *(action_rate + 2);
                *action_rate = *action_rate / sum;
                *(action_rate + 1) = *(action_rate + 1) / sum;
                *(action_rate + 2) = *(action_rate + 2) / sum;
            }
        }
    }
}

void cyc::expand(simulation_environment* env, cyc::uct_node *current_node){
    if(!current_node->expanded){
        float result[3] = {0,0,0};
        int i,j,t,d;
        int opp_action[2], opp_action_num[2];
        int you_possible_action[3], opp_possible_action[3],opp_possible_action2[3];
        get_possible_actions(&you_possible_action[0], current_node->you_snake_direction);
        get_possible_actions(&opp_possible_action[0], current_node->opp_snake_direction[0]);
        get_possible_actions(&opp_possible_action2[0], current_node->opp_snake_direction[1]);
        for(i=0;i<3;i++){
            for(j=0;j<3;j++){
                for(t=0;t<3;t++) {
                        opp_action[0] = opp_possible_action[j];
                        opp_action[1] = opp_possible_action2[t];
                        opp_action_num[0] = j;
                        opp_action_num[1] = t;
                        env->set_state(&current_node->state[0][0], current_node->you_snake_head,
                                       current_node->opp_snake_head, current_node->you_snake_length,
                                       current_node->opp_snake_length, current_node->you_snake_health,
                                       current_node->opp_snake_health, current_node->you_snake_direction,
                                       current_node->opp_snake_direction);
                        if (env->step(you_possible_action[i], opp_possible_action[j],opp_possible_action2[t])) {
                            // game over
                            cyc::board_control(result, &env->state[0][0], env->you_snake_head,
                                          env->opp_snake_head, env->you_snake_length,
                                          env->opp_snake_length,
                                          env->you_snake_health,
                                          env->opp_snake_health);
                            current_node->child_values[i][j][t][0] = *result;
                            current_node->child_values[i][j][t][1] = *(result+1);
                            current_node->child_values[i][j][t][2] = *(result+2);
                            current_node->child_valid[i][j][t] = false;
                            current_node->child_visits[i][j][t] = 1;
                        } else {
                            // game not over
                            cyc::board_control(result, &env->state[0][0], env->you_snake_head,
                                               env->opp_snake_head, env->you_snake_length,
                                               env->opp_snake_length,
                                               env->you_snake_health,
                                               env->opp_snake_health);
                            current_node->child_values[i][j][t][0] = *result;
                            current_node->child_values[i][j][t][1] = *(result+1);
                            current_node->child_values[i][j][t][2] = *(result+2);
                            current_node->child_visits[i][j][t] = 1;
                            auto *p = new uct_node(&env->state[0][0], env->you_snake_head, env->opp_snake_head,
                                                   env->you_snake_length, env->opp_snake_length, env->you_snake_health,
                                                   env->opp_snake_health, you_possible_action[i],
                                                   opp_action, i, opp_action_num);
                            current_node->children[i][j][t] = p;
                            p->parent = current_node;
                        }
                }
            }
        }
    }
    current_node->expanded = true;
}
