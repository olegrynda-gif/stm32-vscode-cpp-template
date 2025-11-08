#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil

# File names
input_file = "Makefile"
backup_file = "Makefile.cubemx"
output_file = "Makefile"

# Create a backup
shutil.copyfile(input_file, backup_file)

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []

# Steps 1-4
inserted_cpp_sources = False
gcc_path_block = False
c_includes_start = False
c_includes_done = False
cxxflags_start = False
cxxflags_done = False
libs_done = False
list_cpp_objects_done = False
cpp_build_dir_start = False
cpp_build_dir_done = False
set_cpp_link_done = False

for i, line in enumerate(lines):
    stripped = line.strip()

    # 1. Insert CPP_SOURCES block before # ASM sources
    if not inserted_cpp_sources and stripped.startswith("# ASM sources"):
        cpp_block = [
            "# CPP sources\n",
            "CPP_SOURCES = \\\n",
            "$(wildcard App/Src/**/*.cpp App/Src/*.cpp)\n\n"
        ]
        new_lines.extend(cpp_block)
        inserted_cpp_sources = True

    # 2. Add CXX in the GCC_PATH block
    if stripped.startswith("ifdef GCC_PATH"):
        gcc_path_block = True

    if gcc_path_block:
        # After the CC = ... line, insert CXX
        if stripped.startswith("CC = $(GCC_PATH)/$(PREFIX)gcc"):
            new_lines.append(line)
            new_lines.append("CXX = $(GCC_PATH)/$(PREFIX)g++\n")
            continue
        # End of block
        if stripped.startswith("else"):
            gcc_path_block = False

    # 3. Add CXX = $(PREFIX)g++ after CC = $(PREFIX)gcc in else
    if stripped.startswith("else"):
        new_lines.append(line)
        # Add line after CC in else
        next_line = lines[i+1].strip() if i+1 < len(lines) else ""
        if next_line.startswith("CC = $(PREFIX)gcc"):
            new_lines.append(lines[i+1])
            new_lines.append("CXX = $(PREFIX)g++\n")
            # Skip already added line to avoid duplication
            continue
        continue

    # 4. Add -IApp/Inc in C_INCLUDES
    if not c_includes_start and stripped.startswith("C_INCLUDES ="):
        new_lines.append(line)
        c_includes_start = True
        continue

    if c_includes_start and not c_includes_done:
        if line.endswith("\\\n"):
            new_lines.append(line)
            continue
        else:
            new_lines.append(line.rstrip("\n") + " \\\n")
            new_lines.append("-IApp/Inc")
            c_includes_done = True
            continue

    # 5. Add CXXFLAGS
    if not cxxflags_start and stripped.startswith("# Generate dependency information"):
        new_lines.append(line)
        cxxflags_start = True
        continue

    if cxxflags_start and not cxxflags_done:
        if stripped == "":
            new_lines.append(line)
            new_lines.append("# Define g++ flags\n")
            new_lines.append("CXXFLAGS = $(CFLAGS) -std=c++17 -fno-exceptions -fno-rtti\n")
            cxxflags_done = True
            continue
        else: 
            new_lines.append(line)
            continue

    # 6. Add CPP libs to LIBS
    if not libs_done and stripped.startswith("LIBS ="):
        new_lines.append(line.rstrip("\n") + "-lstdc++\n")
        libs_done = True
        continue

    # 7. Add list of CPP objects
    if not list_cpp_objects_done and stripped.startswith("vpath %.c $(sort $(dir $(C_SOURCES)))"):
        new_lines.append(line)
        new_lines.append("# list of CPP objects\n")
        new_lines.append("OBJECTS += $(addprefix $(BUILD_DIR)/,$(notdir $(CPP_SOURCES:.cpp=.o)))\n")
        new_lines.append("vpath %.cpp $(sort $(dir $(CPP_SOURCES)))\n")
        list_cpp_objects_done = True
        continue

    # 7. Add BUILD_DIR for CPP objects
    if not cpp_build_dir_start and stripped.lstrip().startswith("$(CC) -c $(CFLAGS)"):
        new_lines.append(line)
        cpp_build_dir_start = True
        continue
    
    if cpp_build_dir_start and not cpp_build_dir_done:  
        new_lines.append(line)
        new_lines.append("$(BUILD_DIR)/%.o: %.cpp Makefile | $(BUILD_DIR)\n")
        new_lines.append("	$(CXX) -c $(CXXFLAGS) -Wa,-a,-ad,-alms=$(BUILD_DIR)/$(notdir $(<:.cpp=.lst)) $< -o $@\n\n")
        cpp_build_dir_done = True
        continue

    # 8. Set linker to CPP
    if not set_cpp_link_done and stripped.lstrip().startswith("$(CC) $(OBJECTS) $(LDFLAGS)"):
        new_lines.append(line.replace("$(CC)", "$(CXX)"))
        set_cpp_link_done = True
        continue 

    # Default line copy
    new_lines.append(line)

# Write result
with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Makefile successfully transformed. Original saved as Makefile.cubemx")
