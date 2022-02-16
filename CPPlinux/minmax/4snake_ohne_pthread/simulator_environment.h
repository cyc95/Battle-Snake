//
// Created by Yuancong Chen on 2021/12/13.
//

#ifndef UNTITLED2_SIMULATOR_ENVIRONMENT_H
#define UNTITLED2_SIMULATOR_ENVIRONMENT_H
#define UP 0
#define LEFT 1
#define RIGHT 2
#define DOWN 3


namespace cyc{
    // 0: UP y+1
    // 1: LEFT x-1
    // 2: RIGHT x+1
    // 3: DOWN y-1

    void get_new_position(int* old_position, const int &action);
    void get_possible_actions(int *possible_actions, const int &input_snake_direction);

    class simulation_environment{
    public:      //There are no private variables. The variables are directly used for speed
        int state[11][11]{}, you_snake_head[2]{}, opp_snake_head[6]{}, you_snake_length, opp_snake_length[3]{}, you_snake_health,
                opp_snake_health[3]{}, you_snake_direction, opp_snake_direction[3]{};

        simulation_environment(){
            int i,j;
            for(i=0;i<11;i++){
                for(j=0;j<11;j++){
                    state[i][j] = 0;
                }
            }
            you_snake_head[0] = 0;
            you_snake_head[1] = 0;
            opp_snake_head[0] = 0;
            opp_snake_head[1] = 0;
            opp_snake_head[2] = 0;
            opp_snake_head[3] = 0;
            opp_snake_head[4] = 0;
            opp_snake_head[5] = 0;
            you_snake_length = 0;
            opp_snake_length[0] = 0;
            opp_snake_length[1] = 0;
            opp_snake_length[2] = 0;
            you_snake_health = 0;
            opp_snake_health[0] = 0;
            opp_snake_health[1] = 0;
            opp_snake_health[2] = 0;
            you_snake_direction = 0;
            opp_snake_direction[0] = 0;
            opp_snake_direction[1] = 0;
            opp_snake_direction[2] = 0;

        }



        simulation_environment(const int* input_state, const int* input_you_snake_head, const int* input_opp_snake_head, const int &input_you_snake_length, const int *input_opp_snake_length, const int &input_you_snake_health,  const int *input_opp_snake_health, const int &input_you_snake_direction, const int *input_opp_snake_direction){
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
            you_snake_head[0] = *input_you_snake_head;
            you_snake_head[1] = *(input_you_snake_head + 1);
            opp_snake_head[0] = *input_opp_snake_head;
            opp_snake_head[1] = *(input_opp_snake_head + 1);
            opp_snake_head[2] = *(input_opp_snake_head + 2);
            opp_snake_head[3] = *(input_opp_snake_head + 3);
            opp_snake_head[4] = *(input_opp_snake_head + 4);
            opp_snake_head[5] = *(input_opp_snake_head + 5);
            you_snake_length = input_you_snake_length;
            opp_snake_length[0] = *input_opp_snake_length;
            opp_snake_length[1] = *(input_opp_snake_length + 1);
            opp_snake_length[2] = *(input_opp_snake_length + 2);
            you_snake_health = input_you_snake_health;
            opp_snake_health[0] = *input_opp_snake_health;
            opp_snake_health[1] = *(input_opp_snake_health + 1);
            opp_snake_health[2] = *(input_opp_snake_health + 2);
            you_snake_direction = input_you_snake_direction;
            opp_snake_direction[0] = *input_opp_snake_direction;
            opp_snake_direction[1] = *(input_opp_snake_direction + 1);
            opp_snake_direction[2] = *(input_opp_snake_direction + 2);

        }

        void set_state(const int* input_state, const int* input_you_snake_head, const int* input_opp_snake_head, const int &input_you_snake_length, const int *input_opp_snake_length, const int &input_you_snake_health, const int *input_opp_snake_health, const int &input_you_snake_direction, const int *input_opp_snake_direction){
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
            you_snake_head[0] = *input_you_snake_head;
            you_snake_head[1] = *(input_you_snake_head + 1);
            opp_snake_head[0] = *input_opp_snake_head;
            opp_snake_head[1] = *(input_opp_snake_head + 1);
            opp_snake_head[2] = *(input_opp_snake_head + 2);
            opp_snake_head[3] = *(input_opp_snake_head + 3);
            opp_snake_head[4] = *(input_opp_snake_head + 4);
            opp_snake_head[5] = *(input_opp_snake_head + 5);
            you_snake_length = input_you_snake_length;
            opp_snake_length[0] = *input_opp_snake_length;
            opp_snake_length[1] = *(input_opp_snake_length + 1);
            opp_snake_length[2] = *(input_opp_snake_length + 2);
            you_snake_health = input_you_snake_health;
            opp_snake_health[0] = *input_opp_snake_health;
            opp_snake_health[1] = *(input_opp_snake_health + 1);
            opp_snake_health[2] = *(input_opp_snake_health + 2);
            you_snake_direction = input_you_snake_direction;
            opp_snake_direction[0] = *input_opp_snake_direction;
            opp_snake_direction[1] = *(input_opp_snake_direction + 1);
            opp_snake_direction[2] = *(input_opp_snake_direction + 2);
        }


        // 0: UP y+1
        // 1: LEFT x-1
        // 2: RIGHT x+1
        // 3: DOWN y-1
        bool step(const int &you_action, const int &opp_action1, const int &opp_action2, const int &opp_action3){
            if(!you_snake_health || (!*opp_snake_health && !*(opp_snake_health+1) && !*(opp_snake_health+2))) return true;
            int i,j;
            bool you_get_food = false;
            bool opp_get_food[3] = {false, false, false};
            you_snake_direction = you_action;
            *opp_snake_direction = opp_action1;
            *(opp_snake_direction+1) = opp_action2;
            *(opp_snake_direction+2) = opp_action3;
            get_new_position(&you_snake_head[0], you_action);
            if(*opp_snake_health) get_new_position(&opp_snake_head[0], opp_action1);
            if(*(opp_snake_health+1)) get_new_position(&opp_snake_head[2], opp_action2);
            if(*(opp_snake_health+2)) get_new_position(&opp_snake_head[4], opp_action3);
            if(you_snake_head[0]<0 || you_snake_head[0]>10 || you_snake_head[1]<0 || you_snake_head[1]>10){
                you_snake_health = 0;
            }
            if(opp_snake_head[0]<0 || opp_snake_head[0]>10 || opp_snake_head[1]<0 || opp_snake_head[1]>10){
                *opp_snake_health = 0;
            }
            if(opp_snake_head[2]<0 || opp_snake_head[2]>10 || opp_snake_head[3]<0 || opp_snake_head[3]>10){
                *(opp_snake_health+1) = 0;
            }
            if(opp_snake_head[4]<0 || opp_snake_head[4]>10 || opp_snake_head[5]<0 || opp_snake_head[5]>10){
                *(opp_snake_health+2) = 0;
            }
            if(opp_snake_head[0]==you_snake_head[0] && opp_snake_head[1]==you_snake_head[1]){
                if(*(opp_snake_length) > you_snake_length) you_snake_health = 0;
                if(*(opp_snake_length) < you_snake_length)  *opp_snake_health = 0;
                if(*(opp_snake_length) == you_snake_length){
                    *(opp_snake_health) = 0;
                    you_snake_health = 0;
                }

            }
            if(opp_snake_head[2]==you_snake_head[0] && opp_snake_head[3]==you_snake_head[1]){
                if(*(opp_snake_length+1) > you_snake_length) you_snake_health = 0;
                if(*(opp_snake_length+1) < you_snake_length)  *(opp_snake_health+1) = 0;
                if(*(opp_snake_length+1) == you_snake_length){
                    *(opp_snake_health+1) = 0;
                    you_snake_health = 0;
                }
            }
            if(opp_snake_head[4]==you_snake_head[0] && opp_snake_head[5]==you_snake_head[1]){
                if(*(opp_snake_length+2) > you_snake_length) you_snake_health = 0;
                if(*(opp_snake_length+2) < you_snake_length)  *(opp_snake_health+2) = 0;
                if(*(opp_snake_length+2) == you_snake_length){
                    *(opp_snake_health+2) = 0;
                    you_snake_health = 0;
                }
            }
            if(opp_snake_head[0]==opp_snake_head[2] && opp_snake_head[1]==opp_snake_head[3]){
                if(*(opp_snake_length+1) > *(opp_snake_length)) *(opp_snake_health) = 0;
                if(*(opp_snake_length+1) < *(opp_snake_length))  *(opp_snake_health+1) = 0;
                if(*(opp_snake_length+1) == *(opp_snake_length)){
                    *(opp_snake_health+1) = 0;
                    *(opp_snake_health) = 0;
                }
            }
            if(opp_snake_head[0]==opp_snake_head[4] && opp_snake_head[1]==opp_snake_head[5]){
                if(*(opp_snake_length+2) > *(opp_snake_length)) *(opp_snake_health) = 0;
                if(*(opp_snake_length+2) < *(opp_snake_length))  *(opp_snake_health+2) = 0;
                if(*(opp_snake_length+2) == *(opp_snake_length)){
                    *(opp_snake_health+2) = 0;
                    *(opp_snake_health) = 0;
                }
            }
            if(opp_snake_head[2]==opp_snake_head[4] && opp_snake_head[3]==opp_snake_head[5]){
                if(*(opp_snake_length+1) > *(opp_snake_length+2)) *(opp_snake_health+2) = 0;
                if(*(opp_snake_length+1) < *(opp_snake_length+2))  *(opp_snake_health+1) = 0;
                if(*(opp_snake_length+1) == *(opp_snake_length+2)){
                    *(opp_snake_health+1) = 0;
                    *(opp_snake_health+2) = 0;
                }
            }
            if(!you_snake_health || (!*opp_snake_health && !*(opp_snake_health+1) && !*(opp_snake_health+2))) return true;
            if(state[you_snake_head[0]][you_snake_head[1]] == 500){  //500 -> food
                you_get_food = true;
            }
            if(state[opp_snake_head[0]][opp_snake_head[1]] == 500 && *opp_snake_health) {
                opp_get_food[0] = true;
            }
            if(state[opp_snake_head[2]][opp_snake_head[3]] == 500 && *(opp_snake_health+1)) {
                opp_get_food[1] = true;
            }
            if(state[opp_snake_head[4]][opp_snake_head[5]] == 500 && *(opp_snake_health+2)) {
                opp_get_food[2] = true;
            }
            for(i=0;i<11;i++){
                for(j=0;j<11;j++){
                    if(state[i][j] && state[i][j] != 500){
                        if(state[i][j]>0 && !you_get_food){
                            state[i][j]--;
                        }
                        if(state[i][j]<0 && state[i][j] > -100 && !opp_get_food[0]){
                            state[i][j]++;
                        }
                        if(state[i][j]<= -100 && state[i][j] > -200 && !opp_get_food[1]){
                            state[i][j]++;
                        }
                        if(state[i][j]<= -200 && !opp_get_food[2]){
                            state[i][j]++;
                        }
                        if(state[i][j] == -100 || state[i][j] == -200){
                            state[i][j] = 0;
                        }
                    }
                }
            }
            if(!you_get_food){
                if(state[you_snake_head[0]][you_snake_head[1]]){
                    you_snake_health = 0;
                } else{
                    you_snake_health --;
                    state[you_snake_head[0]][you_snake_head[1]] = you_snake_length;
                }
            } else{
                you_snake_health = 100;
                you_snake_length++;
                state[you_snake_head[0]][you_snake_head[1]] = you_snake_length;
                for(i=0;i<11;i++){
                    for(j=0;j<11;j++){
                        if(state[i][j] == 1){
                            state[i][j] = 0;
                        }
                    }
                }
            }
            if(*opp_snake_health) {
                if (!opp_get_food[0]) {
                    if (state[opp_snake_head[0]][opp_snake_head[1]]) {
                        *opp_snake_health = 0;
                    } else {
                        *opp_snake_health -= 1;
                        state[opp_snake_head[0]][opp_snake_head[1]] = -*opp_snake_length;
                    }
                } else {
                    *opp_snake_health = 100;
                    *opp_snake_length += 1;
                    state[opp_snake_head[0]][opp_snake_head[1]] = -*opp_snake_length;
                    for(i=0;i<11;i++){
                        for(j=0;j<11;j++){
                            if(state[i][j] == -1){
                                state[i][j] = 0;
                            }
                        }
                    }
                }
            }
            if(*(opp_snake_health+1)) {
                if (!opp_get_food[1]) {
                    if (state[opp_snake_head[2]][opp_snake_head[3]]) {
                        *(opp_snake_health + 1) = 0;
                    } else {
                        *(opp_snake_health + 1) -= 1;
                        state[opp_snake_head[2]][opp_snake_head[3]] = -*(opp_snake_length + 1) - 100;
                    }
                } else {
                    *(opp_snake_health + 1) = 100;
                    *(opp_snake_length + 1) += 1;
                    state[opp_snake_head[2]][opp_snake_head[3]] = -*(opp_snake_length + 1) - 100;
                    for(i=0;i<11;i++){
                        for(j=0;j<11;j++){
                            if(state[i][j] == -101){
                                state[i][j] = 0;
                            }
                        }
                    }
                }
            }
            if(*(opp_snake_health+2)) {
                if (!opp_get_food[2]) {
                    if (state[opp_snake_head[4]][opp_snake_head[5]]) {
                        *(opp_snake_health + 2) = 0;
                    } else {
                        *(opp_snake_health + 2) -= 1;
                        state[opp_snake_head[4]][opp_snake_head[5]] = -*(opp_snake_length + 2) - 200;
                    }
                } else {
                    *(opp_snake_health + 2) = 100;
                    *(opp_snake_length + 2) += 1;
                    state[opp_snake_head[4]][opp_snake_head[5]] = -*(opp_snake_length + 2) - 200;
                    for(i=0;i<11;i++){
                        for(j=0;j<11;j++){
                            if(state[i][j] == -201){
                                state[i][j] = 0;
                            }
                        }
                    }
                }
            }
            if(!you_snake_health || (!*opp_snake_health && !*(opp_snake_health+1) && !*(opp_snake_health+2))) return true;
            return false;
        }

    }; // class simulation_environment


}
#endif //UNTITLED2_SIMULATOR_ENVIRONMENT_H
