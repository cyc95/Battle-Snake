# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/collins/.pyenv/versions/miniconda3-4.7.12/envs/ki-labor/lib/python3.8/site-packages/cmake/data/bin/cmake

# The command to remove a file.
RM = /home/collins/.pyenv/versions/miniconda3-4.7.12/envs/ki-labor/lib/python3.8/site-packages/cmake/data/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2

# Include any dependencies generated for this target.
include CMakeFiles/untitled2.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/untitled2.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/untitled2.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/untitled2.dir/flags.make

CMakeFiles/untitled2.dir/library.cpp.o: CMakeFiles/untitled2.dir/flags.make
CMakeFiles/untitled2.dir/library.cpp.o: library.cpp
CMakeFiles/untitled2.dir/library.cpp.o: CMakeFiles/untitled2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/untitled2.dir/library.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/untitled2.dir/library.cpp.o -MF CMakeFiles/untitled2.dir/library.cpp.o.d -o CMakeFiles/untitled2.dir/library.cpp.o -c /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/library.cpp

CMakeFiles/untitled2.dir/library.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/untitled2.dir/library.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/library.cpp > CMakeFiles/untitled2.dir/library.cpp.i

CMakeFiles/untitled2.dir/library.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/untitled2.dir/library.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/library.cpp -o CMakeFiles/untitled2.dir/library.cpp.s

CMakeFiles/untitled2.dir/simulator_environment.cpp.o: CMakeFiles/untitled2.dir/flags.make
CMakeFiles/untitled2.dir/simulator_environment.cpp.o: simulator_environment.cpp
CMakeFiles/untitled2.dir/simulator_environment.cpp.o: CMakeFiles/untitled2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/untitled2.dir/simulator_environment.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/untitled2.dir/simulator_environment.cpp.o -MF CMakeFiles/untitled2.dir/simulator_environment.cpp.o.d -o CMakeFiles/untitled2.dir/simulator_environment.cpp.o -c /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/simulator_environment.cpp

CMakeFiles/untitled2.dir/simulator_environment.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/untitled2.dir/simulator_environment.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/simulator_environment.cpp > CMakeFiles/untitled2.dir/simulator_environment.cpp.i

CMakeFiles/untitled2.dir/simulator_environment.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/untitled2.dir/simulator_environment.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/simulator_environment.cpp -o CMakeFiles/untitled2.dir/simulator_environment.cpp.s

CMakeFiles/untitled2.dir/BoardControl.cpp.o: CMakeFiles/untitled2.dir/flags.make
CMakeFiles/untitled2.dir/BoardControl.cpp.o: BoardControl.cpp
CMakeFiles/untitled2.dir/BoardControl.cpp.o: CMakeFiles/untitled2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/untitled2.dir/BoardControl.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/untitled2.dir/BoardControl.cpp.o -MF CMakeFiles/untitled2.dir/BoardControl.cpp.o.d -o CMakeFiles/untitled2.dir/BoardControl.cpp.o -c /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/BoardControl.cpp

CMakeFiles/untitled2.dir/BoardControl.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/untitled2.dir/BoardControl.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/BoardControl.cpp > CMakeFiles/untitled2.dir/BoardControl.cpp.i

CMakeFiles/untitled2.dir/BoardControl.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/untitled2.dir/BoardControl.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/BoardControl.cpp -o CMakeFiles/untitled2.dir/BoardControl.cpp.s

CMakeFiles/untitled2.dir/mcts.cpp.o: CMakeFiles/untitled2.dir/flags.make
CMakeFiles/untitled2.dir/mcts.cpp.o: mcts.cpp
CMakeFiles/untitled2.dir/mcts.cpp.o: CMakeFiles/untitled2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object CMakeFiles/untitled2.dir/mcts.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/untitled2.dir/mcts.cpp.o -MF CMakeFiles/untitled2.dir/mcts.cpp.o.d -o CMakeFiles/untitled2.dir/mcts.cpp.o -c /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/mcts.cpp

CMakeFiles/untitled2.dir/mcts.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/untitled2.dir/mcts.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/mcts.cpp > CMakeFiles/untitled2.dir/mcts.cpp.i

CMakeFiles/untitled2.dir/mcts.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/untitled2.dir/mcts.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/mcts.cpp -o CMakeFiles/untitled2.dir/mcts.cpp.s

CMakeFiles/untitled2.dir/uct_node.cpp.o: CMakeFiles/untitled2.dir/flags.make
CMakeFiles/untitled2.dir/uct_node.cpp.o: uct_node.cpp
CMakeFiles/untitled2.dir/uct_node.cpp.o: CMakeFiles/untitled2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building CXX object CMakeFiles/untitled2.dir/uct_node.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/untitled2.dir/uct_node.cpp.o -MF CMakeFiles/untitled2.dir/uct_node.cpp.o.d -o CMakeFiles/untitled2.dir/uct_node.cpp.o -c /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/uct_node.cpp

CMakeFiles/untitled2.dir/uct_node.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/untitled2.dir/uct_node.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/uct_node.cpp > CMakeFiles/untitled2.dir/uct_node.cpp.i

CMakeFiles/untitled2.dir/uct_node.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/untitled2.dir/uct_node.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/uct_node.cpp -o CMakeFiles/untitled2.dir/uct_node.cpp.s

# Object files for target untitled2
untitled2_OBJECTS = \
"CMakeFiles/untitled2.dir/library.cpp.o" \
"CMakeFiles/untitled2.dir/simulator_environment.cpp.o" \
"CMakeFiles/untitled2.dir/BoardControl.cpp.o" \
"CMakeFiles/untitled2.dir/mcts.cpp.o" \
"CMakeFiles/untitled2.dir/uct_node.cpp.o"

# External object files for target untitled2
untitled2_EXTERNAL_OBJECTS =

libuntitled2.so: CMakeFiles/untitled2.dir/library.cpp.o
libuntitled2.so: CMakeFiles/untitled2.dir/simulator_environment.cpp.o
libuntitled2.so: CMakeFiles/untitled2.dir/BoardControl.cpp.o
libuntitled2.so: CMakeFiles/untitled2.dir/mcts.cpp.o
libuntitled2.so: CMakeFiles/untitled2.dir/uct_node.cpp.o
libuntitled2.so: CMakeFiles/untitled2.dir/build.make
libuntitled2.so: CMakeFiles/untitled2.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Linking CXX shared library libuntitled2.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/untitled2.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/untitled2.dir/build: libuntitled2.so
.PHONY : CMakeFiles/untitled2.dir/build

CMakeFiles/untitled2.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/untitled2.dir/cmake_clean.cmake
.PHONY : CMakeFiles/untitled2.dir/clean

CMakeFiles/untitled2.dir/depend:
	cd /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2 /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2 /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2 /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2 /home/collins/Documents/ki_labor/battlesnake-gruppe-8/CPPlinux/minmax/untitled2/CMakeFiles/untitled2.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/untitled2.dir/depend
