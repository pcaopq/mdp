# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /Applications/CMake.app/Contents/bin/cmake

# The command to remove a file.
RM = /Applications/CMake.app/Contents/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end

# Include any dependencies generated for this target.
include CMakeFiles/imageseg.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/imageseg.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/imageseg.dir/flags.make

CMakeFiles/imageseg.dir/imageseg.cpp.o: CMakeFiles/imageseg.dir/flags.make
CMakeFiles/imageseg.dir/imageseg.cpp.o: imageseg.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/imageseg.dir/imageseg.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/imageseg.dir/imageseg.cpp.o -c /Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end/imageseg.cpp

CMakeFiles/imageseg.dir/imageseg.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/imageseg.dir/imageseg.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end/imageseg.cpp > CMakeFiles/imageseg.dir/imageseg.cpp.i

CMakeFiles/imageseg.dir/imageseg.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/imageseg.dir/imageseg.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end/imageseg.cpp -o CMakeFiles/imageseg.dir/imageseg.cpp.s

CMakeFiles/imageseg.dir/imageseg.cpp.o.requires:

.PHONY : CMakeFiles/imageseg.dir/imageseg.cpp.o.requires

CMakeFiles/imageseg.dir/imageseg.cpp.o.provides: CMakeFiles/imageseg.dir/imageseg.cpp.o.requires
	$(MAKE) -f CMakeFiles/imageseg.dir/build.make CMakeFiles/imageseg.dir/imageseg.cpp.o.provides.build
.PHONY : CMakeFiles/imageseg.dir/imageseg.cpp.o.provides

CMakeFiles/imageseg.dir/imageseg.cpp.o.provides.build: CMakeFiles/imageseg.dir/imageseg.cpp.o


# Object files for target imageseg
imageseg_OBJECTS = \
"CMakeFiles/imageseg.dir/imageseg.cpp.o"

# External object files for target imageseg
imageseg_EXTERNAL_OBJECTS =

imageseg: CMakeFiles/imageseg.dir/imageseg.cpp.o
imageseg: CMakeFiles/imageseg.dir/build.make
imageseg: /usr/local/lib/libopencv_videostab.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_superres.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_stitching.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_shape.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_photo.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_objdetect.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_calib3d.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_features2d.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_ml.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_highgui.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_videoio.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_imgcodecs.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_flann.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_video.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_imgproc.3.1.0.dylib
imageseg: /usr/local/lib/libopencv_core.3.1.0.dylib
imageseg: CMakeFiles/imageseg.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable imageseg"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/imageseg.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/imageseg.dir/build: imageseg

.PHONY : CMakeFiles/imageseg.dir/build

CMakeFiles/imageseg.dir/requires: CMakeFiles/imageseg.dir/imageseg.cpp.o.requires

.PHONY : CMakeFiles/imageseg.dir/requires

CMakeFiles/imageseg.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/imageseg.dir/cmake_clean.cmake
.PHONY : CMakeFiles/imageseg.dir/clean

CMakeFiles/imageseg.dir/depend:
	cd /Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end /Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end /Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end /Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end /Users/Bruce/Documents/mdp-newspaper-segmentation/code/end_to_end/CMakeFiles/imageseg.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/imageseg.dir/depend

