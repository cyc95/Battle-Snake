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
        int state[11][11]{}, you_snake_head[2]{}, opp_snake_head[2]{}, you_snake_length, opp_snake_length, you_snake_health,
            opp_snake_health, you_snake_direction, opp_snake_direction, you_snake_direction_num,
            opp_snake_direction_num, child_visits[3][3]{};
        double  child_values[3][3]{};
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

        static void uct(double* uct_values, const uct_node* current_node, const int &test){
            int i,j, sum,t,d;
            for(i=0;i<3;i++){
                for(j=0;j<3;j++){
                    if(current_node->parent != nullptr){
                        sum = current_node->parent->child_visits[current_node->you_snake_direction_num][current_node->opp_snake_direction_num];
                    }else{
                        for(t=0;t<3;t++){
                            for(d=0;d<3;d++){
                                sum += current_node->child_visits[t][d];
                            }
                        }
                    }
                    if(!sum) {
                        if (current_node->child_valid[i][j]) {
                            uct_values[i * 3 + j] = current_node->child_values[i][j] * test / 121 + std::sqrt((log10(sum)/current_node->child_visits[i][j])) ;
                        } else {
                            uct_values[i * 3 + j] = -5000000;
                        }
                    }else{

                    }
                }
            }
        }

        uct_node* select(const int &test){
            int i,best_action=0;
            double uct_values[9];
            uct_node* current_node = this;
            while(true){
                uct(&uct_values[0], current_node, test);
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

       // void simulation(){
            //
       // }

       void backup(){
            float  val;
            uct_node* current_node = this;
            while(current_node->parent != nullptr){
                current_node->parent->child_visits[current_node->you_snake_direction_num][current_node->opp_snake_direction_num] += 8;
                val = (float) current_node->calculated_value();
              //  if(val>0) val -= 0.0005;
                //if(val<0) val += 0.0005;
                current_node->parent->child_values[current_node->you_snake_direction_num][current_node->opp_snake_direction_num] = val;
                if(val < -118 || val > 118) current_node->parent->child_valid[current_node->you_snake_direction_num][current_node->opp_snake_direction_num] = false;
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


        double calculated_value(){

            double values = -121;
            int i ,j;
            // rate for you
            if(0){ // rate
                double values_mean[3], values_rate[3];
                for(i=0;i<3;i++){ //mean
                    values_rate[i] = (double) 1/3;
                }
                //cyc::calculated_action_rate(values_mean, values_rate);
                // rate for opp
                for(i=0;i<3;i++){ //mean
                    values_mean[i] = - this->child_values[0][i] * values_rate[0] - this->child_values[1][i] * values_rate[1] - this->child_values[2][i]* values_rate[2];
                }
                calculated_action_rate(values_mean, values_rate);
                for(i=0;i<3;i++){ //mean
                    values_mean[i] = this->child_values[i][0]* values_rate[0]+this->child_values[i][1]* values_rate[1]+this->child_values[i][2]* values_rate[2];
                    if(values_mean[i]>values) values=values_mean[i];
                }
            }
            if(1){//min max
                double values_min[3];
                for(i=0;i<3;i++){ // min
                    values_min[i] =121;
                }
                //cyc::calculated_action_rate(values_mean, values_rate);
                // rate for opp
                for(i=0;i<3;i++){ //min
                    for(j=0;j<3;j++){ //min
                        if(values_min[i] > this->child_values[i][j])  values_min[i] = this->child_values[i][j];
                    }
                }

                for(i=0;i<3;i++){ //mean
                    if(values  < values_min[i])  values  = values_min[i];
                }
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
