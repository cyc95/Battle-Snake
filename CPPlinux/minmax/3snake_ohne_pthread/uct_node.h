//
// Created by Yuancong Chen on 2021/12/14.
//

#ifndef UNTITLED2_UCT_NODE_H
#define UNTITLED2_UCT_NODE_H
#include "simulator_environment.h"
#include "BoardControl.h"
#include <cmath>
#define you 1
#define opp 2
// 0: UP y+1
// 1: LEFT x-1
// 2: RIGHT x+1
// 3: DOWN y-1
namespace cyc {
    void calculated_action_rate(const double *child_values, double *action_rate);



    class uct_node {
    public:      //There are no private variables. The variables are directly used for speed //health -> 0 = death
        int state[11][11]{}, you_snake_head[2]{}, opp_snake_head[4]{}, you_snake_length, opp_snake_length[2]{}, you_snake_health,
                opp_snake_health[2]{}, you_snake_direction, opp_snake_direction[2]{}, you_snake_direction_num,
                opp_snake_direction_num[2]{}, child_visits[3][3][3]{};
        float  child_values[3][3][3][3]{};
        uct_node* parent = nullptr;
        uct_node* children[3][3][3]{};
        bool child_valid[3][3][3]{}; //child_valid = false -> all node checked
        bool expanded, checked=false;

        uct_node(const int* input_state, const int* input_you_snake_head, const int* input_opp_snake_head, const int &input_you_snake_length, const int* input_opp_snake_length, const int &input_you_snake_health, const int* input_opp_snake_health, const int &input_you_snake_direction, const int* input_opp_snake_direction, const int &input_you_snake_direction_num, const int *input_opp_snake_direction_num) {
            int i, j, t, d;
            for (i = 0; i < 11; i++) {
                for (j = 0; j < 11; j++) {
                    state[i][j] = *(input_state + i * 11 + j);
                }
            }
            you_snake_head[0] = *input_you_snake_head;
            you_snake_head[1] = *(input_you_snake_head + 1);
            opp_snake_head[0] = *input_opp_snake_head;
            opp_snake_head[1] = *(input_opp_snake_head + 1);
            opp_snake_head[2] = *(input_opp_snake_head + 2);
            opp_snake_head[3] = *(input_opp_snake_head + 3);
            you_snake_length = input_you_snake_length;
            opp_snake_length[0] = *input_opp_snake_length;
            opp_snake_length[1] = *(input_opp_snake_length + 1);
            you_snake_health = input_you_snake_health;
            opp_snake_health[0] = *input_opp_snake_health;
            opp_snake_health[1] = *(input_opp_snake_health + 1);
            you_snake_direction = input_you_snake_direction;
            opp_snake_direction[0] = *input_opp_snake_direction;
            opp_snake_direction[1] = *(input_opp_snake_direction + 1);
            you_snake_direction_num = input_you_snake_direction_num;
            opp_snake_direction_num[0] = *input_opp_snake_direction_num;
            opp_snake_direction_num[1] = *(input_opp_snake_direction_num + 1);
            for (i = 0; i < 3; i++) {
                for (j = 0; j < 3; j++) {
                    for (t = 0; t < 3; t++) {
                            children[i][j][t] = nullptr;
                            child_values[i][j][t][0] =  0;  //control_field_snake1
                            child_values[i][j][t][1] =  0;  //control_field_snake2
                            child_values[i][j][t][2] =  0;  //control_field_snake3
                            child_visits[i][j][t] = 0;
                            child_valid[i][j][t] = true;
                    }
                }
            }
            expanded = false;
        }
        static void uct(int* uct_values, const uct_node* current_node) {
            int i, j, t;
            for (i = 0; i < 3; i++) {
                for (j = 0; j < 3; j++) {
                    for (t = 0; t < 3; t++) {
                        if (current_node->child_valid[i][j][t]) {
                            uct_values[i * 9 + j * 3 + t] = -current_node->child_visits[i][j][t];
                        } else {
                            uct_values[i * 9 + j * 3 + t] = -5000000;
                        }
                    }
                }
            }
        }

        uct_node* select(){
            int uct_values[27],i,best_action=0;
            uct_node* current_node = this;
            while(true){
                uct(&uct_values[0], current_node);
                for(i=0;i<27;i++){
                    if(uct_values[i]>uct_values[best_action]) best_action = i;
                }
                if(uct_values[best_action]==-5000000){
                    if(current_node->parent != nullptr) {
                        current_node->parent->child_valid[current_node->you_snake_direction_num][*current_node->opp_snake_direction_num][*(current_node->opp_snake_direction_num+1)] = false; //opp_snake_direction 0-3
                        current_node = nullptr;
                        return current_node;
                    } else{
                        current_node->checked = true;
                        current_node = nullptr;
                        return current_node;
                    }
                }
                if(current_node->children[(best_action )/9][(best_action % 9)/3][best_action%3] == nullptr){
                    return current_node;
                } else {
                    current_node = current_node->children[(best_action)/9][(best_action % 9)/3][best_action%3];
                }
            }
        }
/*
        void expand(simulation_environment* env){
            if(!this->expanded){
                int i,j;
                int you_possible_action[3], opp_possible_action[3];
                get_possible_actions(&you_possible_action[0], this->you_snake_direction);
                get_possible_actions(&opp_possible_action[0], this->opp_snake_direction);
                for(i=0;i<3;i++){
                    for(j=0;j<3;j++){
                        env->set_state(&state[0][0], you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction);
                        if(env->step(you_possible_action[i], opp_possible_action[j])){
                            // game over
                            child_values[i][j] = board_control(&env->state[0][0], env->you_snake_head, env->opp_snake_head, env->you_snake_length, env->opp_snake_length, env->you_snake_health, env->opp_snake_health);
                            child_valid[i][j] = false;
                            child_visits[i][j] = 1;
                        } else{
                            // game not over
                            child_values[i][j] = board_control(&env->state[0][0], env->you_snake_head, env->opp_snake_head, env->you_snake_length, env->opp_snake_length, env->you_snake_health, env->opp_snake_health);
                            child_visits[i][j] = 1;
                            auto* p = new uct_node(&env->state[0][0], env->you_snake_head, env->opp_snake_head, env->you_snake_length, env->opp_snake_length, env->you_snake_health, env->opp_snake_health, you_possible_action[i], opp_possible_action[j], i, j);
                            children[i][j] = p;
                            p->parent = this;
                        }
                    }
                }
            }
            expanded = true;
        }
*/
        // void simulation(){
        //
        // }

        void backup(){
            float  val[3];
            int i,j;
            //bool flag = true, valid = false;
            uct_node* current_node = this;
            while(current_node->parent != nullptr){
                current_node->parent->child_visits[current_node->you_snake_direction_num][*current_node->opp_snake_direction_num][*(current_node->opp_snake_direction_num+1)] += 8;
                current_node->calculated_value(val);
                if(val[0] > 60)
                current_node->parent->child_values[current_node->you_snake_direction_num][*current_node->opp_snake_direction_num][*(current_node->opp_snake_direction_num+1)][0] = val[0] - 0.05f;
                else current_node->parent->child_values[current_node->you_snake_direction_num][*current_node->opp_snake_direction_num][*(current_node->opp_snake_direction_num+1)][0] = val[0] + 0.05f;
                if(val[1] > 60)
                    current_node->parent->child_values[current_node->you_snake_direction_num][*current_node->opp_snake_direction_num][*(current_node->opp_snake_direction_num+1)][1] = val[1] - 0.05f;
                else current_node->parent->child_values[current_node->you_snake_direction_num][*current_node->opp_snake_direction_num][*(current_node->opp_snake_direction_num+1)][1] = val[1] + 0.05f;
                if(val[2] > 60)
                    current_node->parent->child_values[current_node->you_snake_direction_num][*current_node->opp_snake_direction_num][*(current_node->opp_snake_direction_num+1)][2] = val[2] - 0.05f;
                else current_node->parent->child_values[current_node->you_snake_direction_num][*current_node->opp_snake_direction_num][*(current_node->opp_snake_direction_num+1)][2] = val[2] + 0.05f;
              /*   for(i=0;i<3;i++) {
                       for (j = 0; j < 3; j++) {
                           if(current_node->child_valid[i][j]){
                               valid = true;
                               if(current_node->child_deep[i][j] != current_node->self_deep){
                                   flag = false;
                               }
                           }
                       }
                   }
                   *//*
                if(valid && flag){
                    current_node->self_deep ++;
                    current_node->parent->child_deep[current_node->you_snake_direction_num][current_node->opp_snake_direction_num] ++;
                    //a_b_search(current_node);
                }*/
                current_node = current_node->parent;
            }
            /*
           flag = true;
           valid = false;
           for(i=0;i<3;i++) {
               for (j = 0; j < 3; j++) {
                   if(current_node->child_valid[i][j]){
                       valid = true;
                       if(current_node->child_deep[i][j] != current_node->self_deep){
                           flag = false;
                       }
                   }
               }
           }
           if(valid && flag){
               current_node->self_deep++;
           }
*/
        }

        int sum_child_visits(){
            int i,j,sum=0,t,d;
            for(i=0;i<3;i++) {
                for (j = 0; j < 3; j++) {
                    for(t=0;t<3;t++) {
                            sum += this->child_visits[i][j][t];
                    }
                }
            }
            return sum;
        }


        void calculated_value( float * val){

            int i ,j, t;
            int values_max_num2[3][3];
            int values_max_num[3]={0,0,0};
            int max =0;
            for(i=0;i<3;i++){ // min
                for(j=0;j<3;j++) { // min
                    values_max_num2[i][j] = 0;
                }
            }
            //cyc::calculated_action_rate(values_mean, values_rate);
            // rate for opp

            for(i=0;i<3;i++){ //min
                for(j=0;j<3;j++){ //min
                    for(t=0;t<3;t++) {
                        if (this->child_values[i][j][values_max_num2[i][j]][2] < this->child_values[i][j][t][2]) values_max_num2[i][j] = t;
                    }
                }
            }
            for(i=0;i<3;i++){ // min
                for(j=0;j<3;j++) { // min
                    if (this->child_values[i][values_max_num[i]][values_max_num2[i][values_max_num[i]]][1] < this->child_values[i][j][values_max_num2[i][j]][1]) values_max_num[i] = j;
                   //   this->child_values[i][j]                [values_max_num2[i][j                ]][values_max_num3[i][j]                [values_max_num2[i][j                ]]][1]
                }
            }

            for(i=0;i<3;i++){ //max
                if(this->child_values[max][values_max_num[max]][values_max_num2[max][values_max_num[max]]][0]  < this->child_values[i][values_max_num[i]][values_max_num2[i][values_max_num[i]]][0])  max  = i;
            }
            for(i=0;i<3;i++){
                *(val+i) = this->child_values[max][values_max_num[max]][values_max_num2[max][values_max_num[max]]][i];
            }
        }


        ~uct_node(){
            int i,j,t;
            for(i=0;i<3;i++) {
                for (j = 0; j < 3; j++) {
                    for(t=0;t<3;t++) {
                            if (children[i][j] != nullptr) {
                                delete children[i][j][t];
                        }
                    }
                }
            }
        }
    };
    void expand(simulation_environment* env, cyc::uct_node *current_node);

}


#endif //UNTITLED2_UCT_NODE_H
