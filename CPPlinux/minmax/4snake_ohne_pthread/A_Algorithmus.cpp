//
// Created by Yuancong Chen on 2021/12/23.
//
#include "A_Algorithmus.h"
#include "BoardControl.h"
#include <vector>
#include "simulator_environment.h"

void get_valid_neighbors_A(int* valid_neighbors, const int &x, const int &y);
void check_neighbors_A(std::vector<cyc::position> &snake_vector, std::vector<cyc::position> &snake_vector_new, int* control_state, const int* input_state, const int & action_num, bool * find_food);
void state_initialization_A(const int* input_state,  int* control_state, int* control_state2, int* control_state3);
void vector_initialization_A(int* control_state, int* control_state2, int* control_state3, const int* input_you_snake_head, const int &you_snake_direction, std::vector<cyc::position> &you_vector1, std::vector<cyc::position> &you_vector2, std::vector<cyc::position> &you_vector3, bool *action_A_search, int* input_state);
void sort_A(std::vector<cyc::position> &opp_vector, std::vector<cyc::position> &opp_vector_new, std::vector<cyc::position> &opp_vector2, std::vector<cyc::position> &opp_vector_new2, std::vector<cyc::position> &opp_vector3, std::vector<cyc::position> &opp_vector_new3);


void cyc::action_A_algorithm(int* input_state, int* input_you_snake_head, bool *action_A_search, int you_snake_direction){
    int control_state1[121],control_state2[121],control_state3[121];

    std::vector<cyc::position> you_vector1;
    std::vector<cyc::position> you_vector_new1;
    std::vector<cyc::position> you_vector2;
    std::vector<cyc::position> you_vector_new2;
    std::vector<cyc::position> you_vector3;
    std::vector<cyc::position> you_vector_new3;
    state_initialization_A(input_state,control_state1,control_state2,control_state3);
    vector_initialization_A(control_state1, control_state2, control_state3, input_you_snake_head, you_snake_direction, you_vector1, you_vector2, you_vector3,action_A_search,input_state);
    while (!*action_A_search && !(*(action_A_search+1)) && !(*(action_A_search+2))){
        if(you_vector1.empty() && you_vector2.empty() && you_vector3.empty()) break;
        check_neighbors_A(you_vector1,you_vector_new1, control_state1, input_state, 1, action_A_search);
        check_neighbors_A(you_vector2,you_vector_new2, control_state2, input_state, 2, (action_A_search+1));
        check_neighbors_A(you_vector3,you_vector_new3, control_state3, input_state, 3, (action_A_search+2));
        sort_A(you_vector1,you_vector_new1,you_vector2,you_vector_new2,you_vector3,you_vector_new3);
    }
}

void state_initialization_A(const int* input_state,  int* control_state, int* control_state2, int* control_state3){
    int i;
    for(i=0;i<121;i++){
        // 500 -> food
        if(*(input_state+i) == 0 || *(input_state+i) == 500) {
            *(control_state+i) = 0;
            *(control_state2+i) = 0;
            *(control_state3+i) = 0;
        }
        else {
            *(control_state+i) =200;
            *(control_state2+i) =200;
            *(control_state3+i) =200;
        }
    }

}

void vector_initialization_A(int* control_state, int* control_state2, int* control_state3, const int* input_you_snake_head, const int &you_snake_direction, std::vector<cyc::position> &you_vector1, std::vector<cyc::position> &you_vector2, std::vector<cyc::position> &you_vector3, bool *action_A_search, int* input_state){
    int you_possible_action[3],i;
    int you_head1[2], you_head2[2],you_head3[2];
    you_head1[0] = (int)*input_you_snake_head;
    you_head2[0] = (int)*input_you_snake_head;
    you_head3[0] = (int)*input_you_snake_head;
    you_head1[1] = (int)*(input_you_snake_head+1);
    you_head2[1] = (int)*(input_you_snake_head+1);
    you_head3[1] = (int)*(input_you_snake_head+1);
    cyc::get_possible_actions(&you_possible_action[0], you_snake_direction);
    cyc::get_new_position(you_head1, you_possible_action[0]);
    cyc::get_new_position(you_head2, you_possible_action[1]);
    cyc::get_new_position(you_head3, you_possible_action[2]);
    if(you_head1[0]>=0 && you_head1[0] <=10 && you_head1[1]>=0 && you_head1[1] <=10){
        if(*(input_state + you_head1[0] * 11 + you_head1[1]) == 500 ) *action_A_search = true;
        if(*(control_state + you_head1[0] * 11 + you_head1[1]) != 200 ){
            you_vector1.emplace_back(you_head1[0],you_head1[1]);
            *(control_state + you_head1[0] * 11 + you_head1[1]) = 1;
        }
    }
    if(you_head2[0]>=0 && you_head2[0] <=10 && you_head2[1]>=0 && you_head2[1] <=10){
        if(*(input_state + you_head2[0] * 11 + you_head2[1]) == 500 ) *(action_A_search+1) = true;
        if(*(control_state + you_head2[0] * 11 + you_head2[1]) != 200 ){
            you_vector2.emplace_back(you_head2[0],you_head2[1]);
            *(control_state2 + you_head2[0] * 11 + you_head2[1]) = 2;
        }
    }
    if(you_head3[0]>=0 && you_head3[0] <=10 && you_head3[1]>=0 && you_head3[1] <=10){
        if(*(input_state + you_head3[0] * 11 + you_head3[1]) == 500 ) *(action_A_search+2) = true;
        if(*(control_state + you_head3[0] * 11 + you_head3[1]) != 200 ){
            you_vector3.emplace_back(you_head3[0],you_head3[1]);
            *(control_state3 + you_head3[0] * 11 + you_head3[1]) = 3;
        }
    }


}

void check_neighbors_A(std::vector<cyc::position> &snake_vector, std::vector<cyc::position> &snake_vector_new, int* control_state, const int* input_state, const int & action_num, bool * find_food){
    cyc::position current_field;
    int valid_neighbors[4][2], valid_neighbors_t[4][2];
    int w,j,i;
    while(!snake_vector.empty()){
        current_field = snake_vector.back();
        snake_vector.pop_back();
        get_valid_neighbors_A(&valid_neighbors[0][0],current_field.x,current_field.y);
        for(w=0;w<4;w++){
            if(valid_neighbors[w][0]!=-1){ //-1 -> not valid
                j = valid_neighbors[w][0]*11+valid_neighbors[w][1];
                if(*(control_state+j) == 0) {
                    get_valid_neighbors_A(&valid_neighbors_t[0][0], valid_neighbors[w][0], valid_neighbors[w][1]);
                    bool flag = true;
                    for (i = 0; i < 4; i++) {
                        if(valid_neighbors_t[i][0] != -1) {
                            if (*(control_state + valid_neighbors_t[i][0] * 11 + valid_neighbors_t[i][1]) != 0 &&
                                *(control_state + valid_neighbors_t[i][0] * 11 + valid_neighbors_t[i][1]) != 200 &&
                                *(control_state + valid_neighbors_t[i][0] * 11 + valid_neighbors_t[i][1]) != 4 &&
                                *(control_state + valid_neighbors_t[i][0] * 11 + valid_neighbors_t[i][1]) !=
                                action_num) {
                                flag = false;
                            }
                        }
                    }
                    if (flag){
                        *(control_state+j) = action_num;
                        snake_vector_new.emplace_back(valid_neighbors[w][0], valid_neighbors[w][1]);
                    }
                    else *(control_state+j) = 4;
                }
                if(*(input_state+j) == 500) *find_food = true;
            }
        }
    }
}

void sort_A(std::vector<cyc::position> &opp_vector, std::vector<cyc::position> &opp_vector_new, std::vector<cyc::position> &opp_vector2, std::vector<cyc::position> &opp_vector_new2, std::vector<cyc::position> &opp_vector3, std::vector<cyc::position> &opp_vector_new3){
    while(!opp_vector_new.empty()) {
        opp_vector.push_back(opp_vector_new.back());
        opp_vector_new.pop_back();
    }
    while(!opp_vector_new2.empty()) {
        opp_vector2.push_back(opp_vector_new2.back());
        opp_vector_new2.pop_back();
    }
    while(!opp_vector_new3.empty()) {
        opp_vector3.push_back(opp_vector_new3.back());
        opp_vector_new3.pop_back();
    }
}

void get_valid_neighbors_A(int* valid_neighbors, const int &x, const int &y){
    // 0: UP y+1
    if(y!=10){
        *(valid_neighbors) = x;
        *(valid_neighbors+1) = y +1;
    }else {
        *(valid_neighbors) = -1;
        *(valid_neighbors + 1) = -1;
    }
    // 1: LEFT x-1
    if(x!=0){
        *(valid_neighbors+2) = x -1;
        *(valid_neighbors+3) = y;
    }else{
        *(valid_neighbors+2) = -1;
        *(valid_neighbors+3) = -1;
    }
    // 2: RIGHT x+1
    if(x!=10){
        *(valid_neighbors+4) = x + 1;
        *(valid_neighbors+5) = y;
    }else{
        *(valid_neighbors+4) = -1;
        *(valid_neighbors+5) = -1;
    }
    // 3: DOWN y-1
    if(y!=0){
        *(valid_neighbors+6) = x;
        *(valid_neighbors+7) = y - 1;
    }else {
        *(valid_neighbors+6) = -1;
        *(valid_neighbors + 7) = -1;
    }
}