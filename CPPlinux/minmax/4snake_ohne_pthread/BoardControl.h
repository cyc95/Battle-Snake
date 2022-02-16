//
// Created by Yuancong Chen on 2021/12/15.
//

#ifndef UNTITLED2_BOARDCONTROL_H
#define UNTITLED2_BOARDCONTROL_H
#include <vector>

namespace cyc{
    class position{
    public:
        int x;
        int y;
        position(){
            x=-1;
            y=-1;
        }
        position(const int&input_x, const int& input_y){
            x=input_x;
            y=input_y;
        }
        position(const position &A) {
            x = A.x;
            y = A.y;
        }
    };


    void board_control(float* result,const int* input_state, const int* input_you_snake_head, const int* input_opp_snake_head, const int &input_you_snake_length, const int *input_opp_snake_length, const int &input_you_snake_health,  const int *input_opp_snake_health);
}
#endif //UNTITLED2_BOARDCONTROL_H
