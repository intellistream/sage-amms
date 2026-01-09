# FindTorch.cmake - Find PyTorch C++ libraries
# This module is used to locate PyTorch when it's not automatically found

# PyTorch is typically found via CMAKE_PREFIX_PATH set by setup.py
# This file provides additional search hints if needed

if(NOT Torch_FOUND)
    # Try to find torch using Python
    execute_process(
        COMMAND python3 -c "import torch; print(torch.utils.cmake_prefix_path, end='')"
        OUTPUT_VARIABLE TORCH_PREFIX_PATH
        ERROR_QUIET
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    
    if(TORCH_PREFIX_PATH)
        message(STATUS "Found Torch prefix path from Python: ${TORCH_PREFIX_PATH}")
        set(CMAKE_PREFIX_PATH "${TORCH_PREFIX_PATH};${CMAKE_PREFIX_PATH}")
    endif()
endif()

# Now try to find Torch
# Note: The actual find_package(Torch REQUIRED) is called in the main CMakeLists.txt
