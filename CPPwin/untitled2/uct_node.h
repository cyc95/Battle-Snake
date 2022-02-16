//
// Created by Yuancong Chen on 2021/12/14.
//

#ifndef UNTITLED2_UCT_NODE_H
#define UNTITLED2_UCT_NODE_H
#include "simulator_environment.h"
#include "BoardControl.h"
#include<memory>
// 0: UP y+1
// 1: LEFT x-1
// 2: RIGHT x+1
// 3: DOWN y-1
namespace cyc {
    class uct_node {
    public:      //There are no private variables. The variables are directly used for speed //health -> 0 = death
        int state[11][11]{}, you_snake_head[2]{}, opp_snake_head[2]{}, you_snake_length, opp_snake_length, you_snake_health,
            opp_snake_health, you_snake_direction, opp_snake_direction, you_snake_direction_num,
            opp_snake_direction_num, child_visits[3][3]{};
        float  child_values[3][3]{};
        uct_node* parent = nullptr;
        uct_node* children[3][3]{};
        bool child_valid[3][3]{}; //child_valid = false -> all node checked
        bool expanded, checked=false;

        uct_node(const int* input_state, const int* input_you_snake_head, const int* input_opp_snake_head, const int &input_you_snake_length, const int &input_opp_snake_length, const int &input_you_snake_health, const int &input_opp_snake_health, const int &input_you_snake_direction, const int &input_opp_snake_direction, const int &input_you_snake_direction_num, const int &input_opp_snake_direction_num){
            int i,j;
            for(i=0;i<11;i++){
                for(j=0;j<11;j++){
                    state[i][j] = *(input_state+i*11+j);
                }
            }
            you_snake_head[0] = *input_you_snake_head;
            you_snake_head[1] = *(input_you_snake_head+1);
            opp_snake_head[0] = *input_opp_snake_head;
            opp_snake_head[1] = *(input_opp_snake_head+1);
            you_snake_length = input_you_snake_length;
            opp_snake_length = input_opp_snake_length;
            you_snake_health = input_you_snake_health;
            opp_snake_health = input_opp_snake_health;
            you_snake_direction = input_you_snake_direction;
            opp_snake_direction = input_opp_snake_direction;
            you_snake_direction_num = input_you_snake_direction_num;
            opp_snake_direction_num = input_opp_snake_direction_num;
            for(i=0;i<3;i++){
                for(j=0;j<3;j++){
                    children[i][j] = nullptr;
                    child_values[i][j] = (float) 0;
                    child_visits[i][j] = 0;
                    child_valid[i][j] = true;
                }
            }
            expanded = false;
        }

        static void uct(int* uct_values, const uct_node* current_node){
            int i,j;
            for(i=0;i<3;i++){
                for(j=0;j<3;j++){
                    if(current_node->child_valid[i][j]){
                        uct_values[i*3+j] = - current_node->child_visits[i][j];
                    } else{
                        uct_values[i*3+j] = - 5000000;
                    }
                }
            }
        }

        uct_node* select(){
            int uct_values[9],i,best_action=0;
            uct_node* current_node = this;
            while(true){
                uct(&uct_values[0], current_node);
                for(i=0;i<9;i++){
                    if(uct_values[i]>uct_values[best_action]) best_action = i;
                }
                if(uct_values[best_action]==-5000000){
                    if(current_node->parent != nullptr) {
                        current_node->parent->child_valid[current_node->you_snake_direction_num][current_node->opp_snake_direction_num] = false; //opp_snake_direction 0-3
                        current_node = nullptr;
                        return current_node;
                    } else{
                        current_node->checked = true;
                        current_node = nullptr;
                        return current_node;
                    }
                }
                if(current_node->children[best_action/3][best_action%3] == nullptr){
                    return current_node;
                } else {
                    current_node = current_node->children[best_action/3][best_action%3];
                }
            }
        }

        void expand(simulation_environment* env){
            if(!this->expanded){
                int i,j;
                int you_possible_action[3], opp_possible_action[3];
                get_possible_actions(&you_possible_action[0], this->you_snake_direction);
                get_possible_actions(&opp_possible_action[0], this->opp_snake_direction);
                for(i=0;i<3;i++){
                    for(j=0;j<3;j++){
                        int you_head[2],opp_head[2];
                        env->set_state(&state[0][0], you_snake_head, opp_snake_head, you_snake_length, opp_snake_length, you_snake_health, opp_snake_health, you_snake_direction, opp_snake_direction);
                        if(env->step(you_possible_action[i], opp_possible_action[j])){
                            // game over
                            child_values[i][j] = board_control(&env->state[0][0], env->you_snake_head, env->opp_snake_head, env->you_snake_length, env->opp_snake_length, env->you_snake_health, env->opp_snake_health);
                            child_valid[i][j] = false;
                            child_visits[i][j] = 1;
                        } else{
                            // game over
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

       // void simulation(){
            //
       // }

       void backup(){
            float  val;
            uct_node* current_node = this;
            while(current_node->parent != nullptr){
                current_node->parent->child_visits[current_node->you_snake_direction_num][current_node->opp_snake_direction_num] += 8;
                val = (float) current_node->calculated_value();
                //if(val>0) val -= 0.05;
                //if(val<0) val += 0.05;
                current_node->parent->child_values[current_node->you_snake_direction_num][current_node->opp_snake_direction_num] = val;
                if(val == -121 || val == 121) current_node->parent->child_valid[current_node->you_snake_direction_num][current_node->opp_snake_direction_num] = false;
                current_node = current_node->parent;
            }
        }

        int sum_child_visits(){
            int i,j,sum=0;
            for(i=0;i<3;i++) {
                for (j = 0; j < 3; j++) {
                    sum += this->child_visits[i][j];
                }
            }
            return sum;
        }


        float calculated_value(){
            int i;
            for(i=0;i<3;i++){
                if(this->child_values[i][0] >= 118 && this->child_values[i][1] >= 118 && this->child_values[i][2] >= 118)
                    return (this->child_values[i][0]+this->child_values[i][1]+this->child_values[i][2])/3;
                if(this->child_values[0][i] <= -118 && this->child_values[1][i] <= -118 && this->child_values[2][i] <= -118)
                    return (this->child_values[0][i]+this->child_values[1][i]+this->child_values[2][i])/3;
            }
            float values = -121, val;
            for(i=0;i<3;i++){ //mean
                val = (this->child_values[i][0]+this->child_values[i][1]+this->child_values[i][2])/3;
                if(val > values) values = val;
            }
            return values;
        }

        ~uct_node(){
            int i,j;
            for(i=0;i<3;i++) {
                for (j = 0; j < 3; j++) {
                    if(children[i][j] != nullptr){
                        delete children[i][j];
                    }
                }
            }
        }
    };
}


#endif //UNTITLED2_UCT_NODE_H
