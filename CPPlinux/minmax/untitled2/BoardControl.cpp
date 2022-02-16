//
// Created by Yuancong Chen on 2021/12/15.
//

#include "BoardControl.h"
#include <cmath>
void state_initialization(const int* input_state, int* state, int* control_state,const int* input_you_snake_head, const int* input_opp_snake_head);
void vector_initialization(const int* input_you_snake_head, const int* input_opp_snake_head, std::vector<cyc::position> &you_vector, std::vector<cyc::position> &opp_vector);
float calculate_field(std::vector<cyc::position> &you_vector, std::vector<cyc::position> &opp_vector, const int* input_state, int* state, int* control_state, const int &input_you_snake_length, const int &input_opp_snake_length, const int &input_you_snake_health,  const int &input_opp_snake_health, const int *input_you_snake_head, const int * input_opp_snake_head);
void get_valid_neighbors(int* valid_neighbors, const int &x, const int &y);

// input_state = 500 -> food
// input_state < 0 -> opp
// input_state > 0 -> you
float cyc::board_control(const int* input_state, const int* input_you_snake_head, const int* input_opp_snake_head, const int &input_you_snake_length, const int &input_opp_snake_length, const int &input_you_snake_health,  const int &input_opp_snake_health){
    // check if game is already won or lost
    if(!input_opp_snake_health && !input_you_snake_health){
        if(input_you_snake_length>input_opp_snake_length) return 120;
        if(input_you_snake_length<input_opp_snake_length) return -121;
        return -50;
    }
    if(!input_you_snake_health) return -121;
    if(!input_opp_snake_health) return 121;
    int state[121],control_state[121];
    float result;
    // control_state = 200 -> wall
    // control_state = -1 -> opp
    // control_state = 1 -> you
    // vector ist not efficient here
    std::vector<cyc::position> you_vector;
    std::vector<cyc::position> opp_vector;

    state_initialization(input_state, state, control_state,input_you_snake_head,input_opp_snake_head);
    vector_initialization(input_you_snake_head,input_opp_snake_head,you_vector,opp_vector);
    result = calculate_field(you_vector, opp_vector, input_state, state, control_state, input_you_snake_length, input_opp_snake_length, input_you_snake_health,  input_opp_snake_health, input_you_snake_head, input_opp_snake_head);

    return result;
}


void state_initialization(const int* input_state, int* state, int* control_state, const int* input_you_snake_head, const int* input_opp_snake_head){
    int i;
    for(i=0;i<121;i++){
             if(*(input_state+i) < 0) *(state+i) = -*(input_state+i);
             else *(state+i) = *(input_state+i);
             // 500 -> food
             if(*(input_state+i) == 0 || *(input_state+i) == 500) *(control_state+i) = 0;
             else *(control_state+i) =200;
    }
    *(control_state+*input_you_snake_head*11+*(input_you_snake_head+1))=1;
    *(control_state+*input_opp_snake_head*11+*(input_opp_snake_head+1))=-1;
}

void vector_initialization(const int* input_you_snake_head, const int* input_opp_snake_head, std::vector<cyc::position> &you_vector, std::vector<cyc::position> &opp_vector){
    you_vector.emplace_back(*(input_you_snake_head),*(input_you_snake_head+1));
    opp_vector.emplace_back(*(input_opp_snake_head),*(input_opp_snake_head+1));
}

bool check_snake_alive(const int &low_wall_snake, const int &snake_food, const float &control_snake, std::vector<cyc::position> &snake_vector, std::vector<cyc::position> &snake_vector_new, const int *snake_head, const int* control_state, const int* state, const int &snake, const int &snake_length){
    if(low_wall_snake==1024 || snake_length <= (int)control_snake+1-snake_food) return true;
    if(low_wall_snake > (int)control_snake+1-snake_food) return false;
    bool flag = true;
    int control_check=0,i,j,nummer,w;
    bool check_state[121];
    cyc::position current_field;
    int valid_neighbors[4][2];
    int valid_neighbors_s[4][2];
    std::vector<cyc::position> wall_vector;
    snake_vector.emplace_back(*snake_head,*(snake_head+1));
    for(i=0;i<121;i++){
        check_state[i]= false;
    }
    while(flag){
        flag = false;
        while(!snake_vector.empty()){
            current_field = snake_vector.back();
            snake_vector.pop_back();
            get_valid_neighbors(&valid_neighbors[0][0],current_field.x,current_field.y);
            for(i=0;i<4;i++){
                if(valid_neighbors[i][0]!=-1) { //-1 -> not valid
                    j = valid_neighbors[i][0]*11+valid_neighbors[i][1];
                    if(*(control_state+j) == snake && !check_state[j] ){
                        flag = true;
                        nummer=0;
                        get_valid_neighbors(&valid_neighbors_s[0][0],valid_neighbors[i][0],valid_neighbors[i][1]);
                        for(w=0;w<4;w++){
                            if(valid_neighbors_s[w][0]!=-1) {
                                if(*(control_state+valid_neighbors_s[w][0]*11+valid_neighbors_s[w][1]) == snake){
                                    nummer++;
                                }
                            }
                        }
                        if(nummer>=3){
                            snake_vector.emplace_back(valid_neighbors[i][0],valid_neighbors[i][1]);
                            check_state[j] = true;
                            control_check++;
                        }else {
                            snake_vector_new.emplace_back(valid_neighbors[i][0], valid_neighbors[i][1]);
                            check_state[j] = true;
                        }
                    }
                    if(*(control_state+j) == 200 && !check_state[j]){
                        check_state[j] = true;
                        wall_vector.emplace_back(valid_neighbors[i][0],valid_neighbors[i][1]);
                    }
                }
            }
        }
        while(!wall_vector.empty()) {
            current_field = wall_vector.back();
            if(*(state+current_field.x*11+current_field.y) <= control_check +1){
                while(!snake_vector.empty()) snake_vector.pop_back();
                while(!snake_vector_new.empty()) snake_vector_new.pop_back();
                return true;
            }
            wall_vector.pop_back();
        }
        while(!snake_vector_new.empty()){
            current_field = snake_vector_new.back();
            snake_vector.push_back(current_field);
            snake_vector_new.pop_back();
            get_valid_neighbors(&valid_neighbors[0][0],current_field.x,current_field.y);
            for(w=0;w<4;w++){
                if(valid_neighbors[w][0]!=-1) {
                    j=valid_neighbors[w][0]*11+valid_neighbors[w][1];
                    if(*(control_state+j) == 200 && check_state[j]==0){
                        wall_vector.emplace_back(valid_neighbors[w][0],valid_neighbors[w][1]);
                        check_state[j] = true;
                    }
                }
            }
        }
        while(!wall_vector.empty()) {
            current_field = wall_vector.back();
            if(*(state+current_field.x*11+current_field.y) <= control_check +2){
                while(!snake_vector.empty()) snake_vector.pop_back();
                while(!snake_vector_new.empty()) snake_vector_new.pop_back();
                return true;
            }
            wall_vector.pop_back();
        }
        control_check = control_check + (int)snake_vector.size();
    }
    while(!snake_vector.empty()) snake_vector.pop_back();
    while(!snake_vector_new.empty()) snake_vector_new.pop_back();
    return false;
}

void check_neighbors(std::vector<cyc::position> &snake_vector, std::vector<cyc::position> &snake_vector_new, int &snake_food, float &control_snake, int* control_state, const int* state, int &low_wall_snake, const int &i, int snake){
    cyc::position current_field;
    int valid_neighbors[4][2];
    int w,j;
    while(!snake_vector.empty()){
        current_field = snake_vector.back();
        snake_vector.pop_back();
        get_valid_neighbors(&valid_neighbors[0][0],current_field.x,current_field.y);
        for(w=0;w<4;w++){
            if(valid_neighbors[w][0]!=-1){ //-1 -> not valid
                j = valid_neighbors[w][0]*11+valid_neighbors[w][1];
                if(*(control_state+j) == 0) {
                    *(control_state + j) = snake;
                    if (*(state+j) == 500) snake_food++;//500->food
                    control_snake ++;
                    snake_vector_new.emplace_back(valid_neighbors[w][0],valid_neighbors[w][1]);
                }
                if(*(control_state+j) == 200){
                    if(*(state+j) <= i+1) {
                        *(control_state + j) = snake;
                        control_snake ++;
                        snake_vector_new.emplace_back(valid_neighbors[w][0],valid_neighbors[w][1]);
                    }
                    else{
                        if(*(state+j) < low_wall_snake) low_wall_snake = *(state+j);
                    }
                }
            }
        }
    }
}


void sort(std::vector<cyc::position> &you_vector, std::vector<cyc::position> &you_vector_new, std::vector<cyc::position> &opp_vector, std::vector<cyc::position> &opp_vector_new){
    while(!you_vector_new.empty()) {
        you_vector.push_back(you_vector_new.back());
        you_vector_new.pop_back();
    }
    while(!opp_vector_new.empty()) {
        opp_vector.push_back(opp_vector_new.back());
        opp_vector_new.pop_back();
    }
}


void get_valid_neighbors(int* valid_neighbors, const int &x, const int &y){
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

void find_not_checked_position(int* control_state, const int* input_state, float &control_you, float &control_opp, std::vector<cyc::position> &you_vector, std::vector<cyc::position> &opp_vector){
    int i,j,w;
    bool flag_you, flag_opp;
    int valid_neighbors[4][2];
    for(i=0;i<121;i++){
        if(*(control_state+i)==200){
            if(*(input_state+i) > 0){
                *(control_state+i) = 1;
            } else{
                *(control_state+i) = -1;
            }
        }
    }
    for(i=0;i<11;i++){
        for(j=0;j<11;j++){
            if(*(control_state+i*11+j)==0){
                flag_you = false;
                flag_opp = false;
                get_valid_neighbors(&valid_neighbors[0][0],i,j);
                for(w=0;w<4;w++){
                    if(valid_neighbors[w][0]!=-1){ //-1 -> not valid
                        if(*(control_state+valid_neighbors[w][0]*11+valid_neighbors[w][1]) == 1) flag_you = true;
                        if(*(control_state+valid_neighbors[w][0]*11+valid_neighbors[w][1]) == -1) flag_opp = true;
                    }
                }
                if(flag_you && !flag_opp){
                    *(control_state+i*11+j) = 1;
                    control_you ++;
                    you_vector.emplace_back(i,j);
                }
                if(!flag_you && flag_opp){
                    *(control_state+i*11+j) = -1;
                    control_opp ++;
                    opp_vector.emplace_back(i,j);
                }
            }
        }
    }
}

float calculate_field(std::vector<cyc::position> &you_vector, std::vector<cyc::position> &opp_vector, const int* input_state, int* state, int* control_state, const int &input_you_snake_length, const int &input_opp_snake_length, const int &input_you_snake_health,  const int &input_opp_snake_health, const int *input_you_snake_head, const int * input_opp_snake_head){
    float control_you=0, control_opp=0;
    //I don’t use maps here to improve efficiency
    int low_wall_you = 1024;
    int low_wall_opp = 1024;
    bool you_alive = true;
    bool you_alive_checked = false;
    bool opp_alive = true;
    bool opp_alive_checked = false;
    int you_food = 0;
    int opp_food = 0;
    int i,j;
    std::vector<cyc::position> you_vector_new;
    std::vector<cyc::position> opp_vector_new;
    bool you_longer;
    you_longer = input_you_snake_length > input_opp_snake_length;
    if(you_longer){
        for(i=0;i<121;i++){
            if(you_vector.empty() && opp_vector.empty()) break;
            if(you_vector.empty() && !you_alive_checked){
                you_alive=check_snake_alive(low_wall_you, you_food, control_you, you_vector, you_vector_new, input_you_snake_head, control_state, state, 1, input_you_snake_length);
                you_alive_checked = true;
            }
            if(opp_vector.empty() && !opp_alive_checked){
                opp_alive=check_snake_alive(low_wall_opp, opp_food, control_opp, opp_vector, opp_vector_new, input_opp_snake_head, control_state, state, -1, input_opp_snake_length);
                opp_alive_checked = true;
            }
            check_neighbors(you_vector, you_vector_new, you_food, control_you, control_state, state, low_wall_you, i, 1);
            check_neighbors(opp_vector, opp_vector_new, opp_food, control_opp, control_state, state, low_wall_opp, i, -1);
            sort(you_vector, you_vector_new, opp_vector, opp_vector_new);
        }
    }else{
        for(i=0;i<121;i++){
            if(you_vector.empty() && opp_vector.empty()) break;
            if(you_vector.empty() && !you_alive_checked){
                you_alive = check_snake_alive(low_wall_you, you_food, control_you, you_vector, you_vector_new, input_you_snake_head, control_state, state, 1, input_you_snake_length);
                you_alive_checked = true;
            }
            if(opp_vector.empty() && !opp_alive_checked){
                opp_alive=check_snake_alive(low_wall_opp, opp_food, control_opp, opp_vector, opp_vector_new, input_opp_snake_head, control_state, state, -1, input_opp_snake_length);
                opp_alive_checked = true;
            }
            check_neighbors(opp_vector, opp_vector_new,  opp_food, control_opp, control_state, state, low_wall_opp, i, -1);
            check_neighbors(you_vector, you_vector_new,  you_food, control_you, control_state, state, low_wall_you, i, 1);
            sort(you_vector, you_vector_new, opp_vector, opp_vector_new);
        }
    }
    find_not_checked_position(control_state, input_state, control_you, control_opp, you_vector, opp_vector);
    if(false){
        for(i=0;i<121;i++){
            if(you_vector.empty() && opp_vector.empty()) break;
            check_neighbors(you_vector, you_vector_new, you_food, control_you, control_state, state, low_wall_you, i, 1);
            check_neighbors(opp_vector, opp_vector_new, opp_food, control_opp, control_state, state, low_wall_opp, i, -1);
            sort(you_vector, you_vector_new, opp_vector, opp_vector_new);
        }
    }else{
        for(i=0;i<121;i++){
            if(you_vector.empty() && opp_vector.empty()) break;
            check_neighbors(opp_vector, opp_vector_new,  opp_food, control_opp, control_state, state, low_wall_opp, i, -1);
            check_neighbors(you_vector, you_vector_new,  you_food, control_you, control_state, state, low_wall_you, i, 1);
            sort(you_vector, you_vector_new, opp_vector, opp_vector_new);
        }
    }
    float food_values=0, result;
    if(input_you_snake_health <70) food_values --;
    if(input_you_snake_health <50) food_values -= 2;
    if(input_you_snake_health <30) food_values -= 5;
    if(input_you_snake_health <15) food_values -= 10;
    if(input_you_snake_length-input_opp_snake_length < 4 && input_opp_snake_length < 16 && input_you_snake_length < 16) food_values = food_values + (float)input_you_snake_length * 5 - (float) input_opp_snake_length * 5;
    if(you_alive==opp_alive) result = control_you - control_opp;
    else{
        if(!you_alive) result = control_you  - 120;
        if(!opp_alive) result = 120 - control_opp ;
    }

    result = result +  3 * food_values * (121 - std::abs(result)) / 121;
    return result;
}