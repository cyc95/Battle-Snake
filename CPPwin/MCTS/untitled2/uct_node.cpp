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