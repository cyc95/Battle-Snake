//
// Created by Yuancong Chen on 2021/12/15.
//
#include "uct_node.h"
#include "simulator_environment.h"
#include <sys/time.h>
#include "mcts.h"
#include <pthread.h>
bool end = true;
bool flag_end[9];
cyc::uct_node *current_node;
int mcts(cyc::simulation_environment* env, cyc::uct_node* root_node, const int &simulation_time){
    int i = 0, j, sum=0;
    struct timeval time_now{};
    //SYSTEMTIME s_time;
    //GetLocalTime(&s_time);
    gettimeofday(&time_now, nullptr);
    int alt_time;
    end = true;
    pthread_t thread[9];
    //alt_time = (int) s_time.wSecond * 1000 + (int) s_time.wMilliseconds;
    alt_time = (int)(time_now.tv_sec * 1000) + (int)(time_now.tv_usec / 1000);
    int new_time = alt_time;
    current_node = root_node;
    for(i=0;i<9;i++){
        flag_end[i] = true;
    }
    pthread_create(&thread[0], nullptr, cyc::expand_thread1, nullptr);
    pthread_create(&thread[1], nullptr, cyc::expand_thread2, nullptr);
    pthread_create(&thread[2], nullptr, cyc::expand_thread3, nullptr);
    pthread_create(&thread[3], nullptr, cyc::expand_thread4, nullptr);
    pthread_create(&thread[4], nullptr, cyc::expand_thread5, nullptr);
    pthread_create(&thread[5], nullptr, cyc::expand_thread6, nullptr);
    pthread_create(&thread[6], nullptr, cyc::expand_thread7, nullptr);
    pthread_create(&thread[7], nullptr, cyc::expand_thread8, nullptr);
    pthread_create(&thread[8], nullptr, cyc::expand_thread9, nullptr);

    while((new_time - alt_time) < simulation_time && ! root_node->checked && i< 20000 && (i<9 || simulation_time >= 1)){
        if(i%100 == 0) {
           // GetLocalTime(&s_time);
            gettimeofday(&time_now, nullptr);
            //new_time = (int) s_time.wSecond * 1000 + (int) s_time.wMilliseconds;
            new_time = (int)(time_now.tv_sec * 1000) + (int)(time_now.tv_usec / 1000);
            if (new_time < alt_time) new_time = new_time + 60000;
        }
        current_node = root_node->select();
        i++;
        if(current_node == nullptr) continue;
        //cyc::expand(env,current_node);
        if(!current_node->expanded){
            for(j=0;j<9;j++){
                flag_end[j] = false;
            }
            while (!flag_end[0] || !flag_end[1] || !flag_end[2] || !flag_end[3] || !flag_end[4] || !flag_end[5] || !flag_end[6] || !flag_end[7] || !flag_end[8]){
            }
            current_node->expanded = true;
        }
        current_node->backup();
    }
    sum=root_node->sum_child_visits();
    end = false;
    for(j=0;j<9;j++){
        flag_end[j] = false;
    }
    for(i=0;i<9;i++) {
        pthread_join(thread[i], nullptr);
    }
    return sum;
}
//cyc::simulation_environment* env, cyc::uct_node *current_node, pthread_mutex_t *matt, pthread_mutex_t* matt_t
void *cyc::expand_thread1(void* arg){
    //pthread_exit(nullptr);
    int num=0,i=0,j=0;
    auto* env_test =new cyc::simulation_environment();
    while(true) {
        while (flag_end[num]){
        }
        if(!end)break; //
        int you_possible_action[3], opp_possible_action[3];
        cyc::get_possible_actions(&you_possible_action[0], (current_node)->you_snake_direction);
        cyc::get_possible_actions(&opp_possible_action[0], (current_node)->opp_snake_direction);
        env_test->set_state(&(current_node->state[0][0]), (current_node)->you_snake_head, (current_node)->opp_snake_head,
                               (current_node)->you_snake_length, (current_node)->opp_snake_length, (current_node)->you_snake_health,
                               (current_node)->opp_snake_health, (current_node)->you_snake_direction,
                               (current_node)->opp_snake_direction);
        if (env_test->step(you_possible_action[i], opp_possible_action[j])) {
            // game over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_valid[i][j] = false;
            (current_node)->child_visits[i][j] = 1;
        } else {
            // game not over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_visits[i][j] = 1;
            auto *p = new uct_node(&(env_test->state[0][0]), env_test->you_snake_head, env_test->opp_snake_head,
                                   env_test->you_snake_length, env_test->opp_snake_length, env_test->you_snake_health,
                                   env_test->opp_snake_health, you_possible_action[i], opp_possible_action[j],
                                   i,
                                   j);
            (current_node)->children[i][j] = p;
            p->parent = (current_node);
        }
        flag_end[num] = true;
    }
    delete env_test;
    pthread_exit(nullptr);
}
void *cyc::expand_thread2(void *arg){
    //pthread_exit(nullptr);
    int num=1,i=0,j=1;
    auto* env_test =new cyc::simulation_environment();
    while(true) {
        while (flag_end[num]){
        }
        if(!end)break; //
        int you_possible_action[3], opp_possible_action[3];
        cyc::get_possible_actions(&you_possible_action[0], (current_node)->you_snake_direction);
        cyc::get_possible_actions(&opp_possible_action[0], (current_node)->opp_snake_direction);
        env_test->set_state(&(current_node->state[0][0]), (current_node)->you_snake_head, (current_node)->opp_snake_head,
                            (current_node)->you_snake_length, (current_node)->opp_snake_length, (current_node)->you_snake_health,
                            (current_node)->opp_snake_health, (current_node)->you_snake_direction,
                            (current_node)->opp_snake_direction);
        if (env_test->step(you_possible_action[i], opp_possible_action[j])) {
            // game over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_valid[i][j] = false;
            (current_node)->child_visits[i][j] = 1;
        } else {
            // game not over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_visits[i][j] = 1;
            auto *p = new uct_node(&(env_test->state[0][0]), env_test->you_snake_head, env_test->opp_snake_head,
                                   env_test->you_snake_length, env_test->opp_snake_length, env_test->you_snake_health,
                                   env_test->opp_snake_health, you_possible_action[i], opp_possible_action[j],
                                   i,
                                   j);
            (current_node)->children[i][j] = p;
            p->parent = (current_node);
        }
        flag_end[num] = true;
    }
    delete env_test;
    pthread_exit(nullptr);
}

void *cyc::expand_thread3(void *arg){
    //pthread_exit(nullptr);
    int num=2,i=0,j=2;
    auto* env_test =new cyc::simulation_environment();
    while(true) {
        while (flag_end[num]){
        }
        if(!end)break; //
        int you_possible_action[3], opp_possible_action[3];
        cyc::get_possible_actions(&you_possible_action[0], (current_node)->you_snake_direction);
        cyc::get_possible_actions(&opp_possible_action[0], (current_node)->opp_snake_direction);
        env_test->set_state(&(current_node->state[0][0]), (current_node)->you_snake_head, (current_node)->opp_snake_head,
                            (current_node)->you_snake_length, (current_node)->opp_snake_length, (current_node)->you_snake_health,
                            (current_node)->opp_snake_health, (current_node)->you_snake_direction,
                            (current_node)->opp_snake_direction);
        if (env_test->step(you_possible_action[i], opp_possible_action[j])) {
            // game over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_valid[i][j] = false;
            (current_node)->child_visits[i][j] = 1;
        } else {
            // game not over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_visits[i][j] = 1;
            auto *p = new uct_node(&(env_test->state[0][0]), env_test->you_snake_head, env_test->opp_snake_head,
                                   env_test->you_snake_length, env_test->opp_snake_length, env_test->you_snake_health,
                                   env_test->opp_snake_health, you_possible_action[i], opp_possible_action[j],
                                   i,
                                   j);
            (current_node)->children[i][j] = p;
            p->parent = (current_node);
        }
        flag_end[num] = true;
    }
    delete env_test;
    pthread_exit(nullptr);
}

void *cyc::expand_thread4(void *arg){
    //pthread_exit(nullptr);
    int num=3,i=1,j=0;
    auto* env_test =new cyc::simulation_environment();
    while(true) {
        while (flag_end[num]){
        }
        if(!end)break; //
        int you_possible_action[3], opp_possible_action[3];
        cyc::get_possible_actions(&you_possible_action[0], (current_node)->you_snake_direction);
        cyc::get_possible_actions(&opp_possible_action[0], (current_node)->opp_snake_direction);
        env_test->set_state(&(current_node->state[0][0]), (current_node)->you_snake_head, (current_node)->opp_snake_head,
                            (current_node)->you_snake_length, (current_node)->opp_snake_length, (current_node)->you_snake_health,
                            (current_node)->opp_snake_health, (current_node)->you_snake_direction,
                            (current_node)->opp_snake_direction);
        if (env_test->step(you_possible_action[i], opp_possible_action[j])) {
            // game over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_valid[i][j] = false;
            (current_node)->child_visits[i][j] = 1;
        } else {
            // game not over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_visits[i][j] = 1;
            auto *p = new uct_node(&(env_test->state[0][0]), env_test->you_snake_head, env_test->opp_snake_head,
                                   env_test->you_snake_length, env_test->opp_snake_length, env_test->you_snake_health,
                                   env_test->opp_snake_health, you_possible_action[i], opp_possible_action[j],
                                   i,
                                   j);
            (current_node)->children[i][j] = p;
            p->parent = (current_node);
        }
        flag_end[num] = true;
    }
    delete env_test;
    pthread_exit(nullptr);
}

void *cyc::expand_thread5(void *arg){
    //pthread_exit(nullptr);
    int num=4,i=1,j=1;
    auto* env_test =new cyc::simulation_environment();
    while(true) {
        while (flag_end[num]){
        }
        if(!end)break; //
        int you_possible_action[3], opp_possible_action[3];
        cyc::get_possible_actions(&you_possible_action[0], (current_node)->you_snake_direction);
        cyc::get_possible_actions(&opp_possible_action[0], (current_node)->opp_snake_direction);
        env_test->set_state(&(current_node->state[0][0]), (current_node)->you_snake_head, (current_node)->opp_snake_head,
                            (current_node)->you_snake_length, (current_node)->opp_snake_length, (current_node)->you_snake_health,
                            (current_node)->opp_snake_health, (current_node)->you_snake_direction,
                            (current_node)->opp_snake_direction);
        if (env_test->step(you_possible_action[i], opp_possible_action[j])) {
            // game over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_valid[i][j] = false;
            (current_node)->child_visits[i][j] = 1;
        } else {
            // game not over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_visits[i][j] = 1;
            auto *p = new uct_node(&(env_test->state[0][0]), env_test->you_snake_head, env_test->opp_snake_head,
                                   env_test->you_snake_length, env_test->opp_snake_length, env_test->you_snake_health,
                                   env_test->opp_snake_health, you_possible_action[i], opp_possible_action[j],
                                   i,
                                   j);
            (current_node)->children[i][j] = p;
            p->parent = (current_node);
        }
        flag_end[num] = true;
    }
    delete env_test;
    pthread_exit(nullptr);
}

void *cyc::expand_thread6(void *arg){
    //pthread_exit(nullptr);
    int num=5,i=1,j=2;
    auto* env_test =new cyc::simulation_environment();
    while(true) {
        while (flag_end[num]){
        }
        if(!end)break; //
        int you_possible_action[3], opp_possible_action[3];
        cyc::get_possible_actions(&you_possible_action[0], (current_node)->you_snake_direction);
        cyc::get_possible_actions(&opp_possible_action[0], (current_node)->opp_snake_direction);
        env_test->set_state(&(current_node->state[0][0]), (current_node)->you_snake_head, (current_node)->opp_snake_head,
                            (current_node)->you_snake_length, (current_node)->opp_snake_length, (current_node)->you_snake_health,
                            (current_node)->opp_snake_health, (current_node)->you_snake_direction,
                            (current_node)->opp_snake_direction);
        if (env_test->step(you_possible_action[i], opp_possible_action[j])) {
            // game over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_valid[i][j] = false;
            (current_node)->child_visits[i][j] = 1;
        } else {
            // game not over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_visits[i][j] = 1;
            auto *p = new uct_node(&(env_test->state[0][0]), env_test->you_snake_head, env_test->opp_snake_head,
                                   env_test->you_snake_length, env_test->opp_snake_length, env_test->you_snake_health,
                                   env_test->opp_snake_health, you_possible_action[i], opp_possible_action[j],
                                   i,
                                   j);
            (current_node)->children[i][j] = p;
            p->parent = (current_node);
        }
        flag_end[num] = true;
    }
    delete env_test;
    pthread_exit(nullptr);
}

void *cyc::expand_thread7(void *arg){
    //pthread_exit(nullptr);
    int num=6,i=2,j=0;
    auto* env_test =new cyc::simulation_environment();
    while(true) {
        while (flag_end[num]){
        }
        if(!end)break; //
        int you_possible_action[3], opp_possible_action[3];
        cyc::get_possible_actions(&you_possible_action[0], (current_node)->you_snake_direction);
        cyc::get_possible_actions(&opp_possible_action[0], (current_node)->opp_snake_direction);
        env_test->set_state(&(current_node->state[0][0]), (current_node)->you_snake_head, (current_node)->opp_snake_head,
                            (current_node)->you_snake_length, (current_node)->opp_snake_length, (current_node)->you_snake_health,
                            (current_node)->opp_snake_health, (current_node)->you_snake_direction,
                            (current_node)->opp_snake_direction);
        if (env_test->step(you_possible_action[i], opp_possible_action[j])) {
            // game over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_valid[i][j] = false;
            (current_node)->child_visits[i][j] = 1;
        } else {
            // game not over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_visits[i][j] = 1;
            auto *p = new uct_node(&(env_test->state[0][0]), env_test->you_snake_head, env_test->opp_snake_head,
                                   env_test->you_snake_length, env_test->opp_snake_length, env_test->you_snake_health,
                                   env_test->opp_snake_health, you_possible_action[i], opp_possible_action[j],
                                   i,
                                   j);
            (current_node)->children[i][j] = p;
            p->parent = (current_node);
        }
        flag_end[num] = true;
    }
    delete env_test;
    pthread_exit(nullptr);
}

void *cyc::expand_thread8(void *arg){
    //pthread_exit(nullptr);
    int num=7,i=2,j=1;
    auto* env_test =new cyc::simulation_environment();
    while(true) {
        while (flag_end[num]){
        }
        if(!end)break; //
        int you_possible_action[3], opp_possible_action[3];
        cyc::get_possible_actions(&you_possible_action[0], (current_node)->you_snake_direction);
        cyc::get_possible_actions(&opp_possible_action[0], (current_node)->opp_snake_direction);
        env_test->set_state(&(current_node->state[0][0]), (current_node)->you_snake_head, (current_node)->opp_snake_head,
                            (current_node)->you_snake_length, (current_node)->opp_snake_length, (current_node)->you_snake_health,
                            (current_node)->opp_snake_health, (current_node)->you_snake_direction,
                            (current_node)->opp_snake_direction);
        if (env_test->step(you_possible_action[i], opp_possible_action[j])) {
            // game over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_valid[i][j] = false;
            (current_node)->child_visits[i][j] = 1;
        } else {
            // game not over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_visits[i][j] = 1;
            auto *p = new uct_node(&(env_test->state[0][0]), env_test->you_snake_head, env_test->opp_snake_head,
                                   env_test->you_snake_length, env_test->opp_snake_length, env_test->you_snake_health,
                                   env_test->opp_snake_health, you_possible_action[i], opp_possible_action[j],
                                   i,
                                   j);
            (current_node)->children[i][j] = p;
            p->parent = (current_node);
        }
        flag_end[num] = true;
    }
    delete env_test;
    pthread_exit(nullptr);
}

void *cyc::expand_thread9(void *arg){
    //pthread_exit(nullptr);
    int num=8,i=2,j=2;
    auto* env_test =new cyc::simulation_environment();
    while(true) {
        while (flag_end[num]){
        }
        if(!end)break; //
        int you_possible_action[3], opp_possible_action[3];
        cyc::get_possible_actions(&you_possible_action[0], (current_node)->you_snake_direction);
        cyc::get_possible_actions(&opp_possible_action[0], (current_node)->opp_snake_direction);
        env_test->set_state(&(current_node->state[0][0]), (current_node)->you_snake_head, (current_node)->opp_snake_head,
                            (current_node)->you_snake_length, (current_node)->opp_snake_length, (current_node)->you_snake_health,
                            (current_node)->opp_snake_health, (current_node)->you_snake_direction,
                            (current_node)->opp_snake_direction);
        if (env_test->step(you_possible_action[i], opp_possible_action[j])) {
            // game over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_valid[i][j] = false;
            (current_node)->child_visits[i][j] = 1;
        } else {
            // game not over
            (current_node)->child_values[i][j] = cyc::board_control(&(env_test->state[0][0]),
                                                                    env_test->you_snake_head,
                                                                    env_test->opp_snake_head,
                                                                    env_test->you_snake_length,
                                                                    env_test->opp_snake_length,
                                                                    env_test->you_snake_health,
                                                                    env_test->opp_snake_health);
            (current_node)->child_visits[i][j] = 1;
            auto *p = new uct_node(&(env_test->state[0][0]), env_test->you_snake_head, env_test->opp_snake_head,
                                   env_test->you_snake_length, env_test->opp_snake_length, env_test->you_snake_health,
                                   env_test->opp_snake_health, you_possible_action[i], opp_possible_action[j],
                                   i,
                                   j);
            (current_node)->children[i][j] = p;
            p->parent = (current_node);
        }
        flag_end[num] = true;
    }
    delete env_test;
    pthread_exit(nullptr);
}
