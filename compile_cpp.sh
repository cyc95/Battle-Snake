#!/bin/bash

# ./CPPlinux/minmax/4snake_ohne_pthread
cd "./CPPlinux/minmax/4snake_ohne_pthread"
cmake . > /dev/null
make > /dev/null
cd ../../..
rm "./agents/KILabAgentGroup8/shared_objects/libsnake_4_old.so" 2> /dev/null
mv "./agents/KILabAgentGroup8/shared_objects/libsnake_4.so" "./agents/KILabAgentGroup8/shared_objects/libsnake_4_old.so" 2> /dev/null
mv "./CPPlinux/minmax/4snake_ohne_pthread/libsnake_4.so" "./agents/KILabAgentGroup8/shared_objects/"


# ./CPPlinux/minmax/duel_ohne_pthread
cd "./CPPlinux/minmax/duel_ohne_pthread"
cmake . > /dev/null
make > /dev/null
cd ../../..
rm "./agents/KILabAgentGroup8/shared_objects/libuntitled_old.so" 2> /dev/null
mv "./agents/KILabAgentGroup8/shared_objects/libuntitled.so" "./agents/KILabAgentGroup8/shared_objects/libuntitled_old.so" 2> /dev/null
mv "./CPPlinux/minmax/duel_ohne_pthread/libuntitled.so" "./agents/KILabAgentGroup8/shared_objects/"

# ./CPPlinux/minmax/3snake_ohne_pthread
cd "./CPPlinux/minmax/3snake_ohne_pthread"
cmake . > /dev/null
make > /dev/null
cd ../../..
rm "./agents/KILabAgentGroup8/shared_objects/lib3snake_old.so" 2> /dev/null
mv "./agents/KILabAgentGroup8/shared_objects/lib3snake.so" "./agents/KILabAgentGroup8/shared_objects/lib3snake_old.so" 2> /dev/null
mv "./CPPlinux/minmax/3snake_ohne_pthread/lib3snake.so" "./agents/KILabAgentGroup8/shared_objects/"
