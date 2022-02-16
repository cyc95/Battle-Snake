//
// Created by Yuancong Chen on 2021/12/13.
//

#include "simulator_environment.h"

void cyc::get_new_position(int* old_position, const int &action){
    if(action==UP) *(old_position+1) += 1;
    if(action==LEFT) *old_position -= 1;
    if(action==RIGHT) *old_position += 1;
    if(action==DOWN) *(old_position+1) -= 1;
}

void cyc::get_possible_actions(int *possible_actions, const int &input_snake_direction){
    if(input_snake_direction==UP){
        *possible_actions = UP;
        *(possible_actions+1) = LEFT;
        *(possible_actions+2) = RIGHT;
    }
    if(input_snake_direction==LEFT){
        *possible_actions = UP;
        *(possible_actions+1) = LEFT;
        *(possible_actions+2) = DOWN;
    }
    if(input_snake_direction==RIGHT){
        *possible_actions = UP;
        *(possible_actions+1) = RIGHT;
        *(possible_actions+2) = DOWN;
    }
    if(input_snake_direction==3){
        *possible_actions = LEFT;
        *(possible_actions+1) = RIGHT;
        *(possible_actions+2) = DOWN;
    }
}