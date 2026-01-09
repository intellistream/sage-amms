# FindCuda.cmake - Find CUDA toolkit
# This module defines:
#  CUDA_FOUND - System has CUDA
#  CUDA_INCLUDE_DIRS - CUDA include directories
#  CUDA_LIBRARIES - CUDA libraries
#  CUDA_VERSION - CUDA version

# Enable CUDA support
option(ENABLE_CUDA
       "Enable CUDA support for GPU acceleration"
       OFF
)

if(NOT ENABLE_CUDA)
    message(STATUS "CUDA support is disabled")
    set(CUDA_FOUND FALSE)
    return()
endif()

# Try to find CUDA using CMake's built-in FindCUDA or FindCUDAToolkit
if(CMAKE_VERSION VERSION_GREATER_EQUAL "3.17")
    # Use modern CUDAToolkit (CMake 3.17+)
    find_package(CUDAToolkit QUIET)
    if(CUDAToolkit_FOUND)
        set(CUDA_FOUND TRUE)
        set(CUDA_VERSION ${CUDAToolkit_VERSION})
        set(CUDA_INCLUDE_DIRS ${CUDAToolkit_INCLUDE_DIRS})
        set(CUDA_LIBRARIES CUDA::cudart CUDA::cublas)
        message(STATUS "Found CUDA ${CUDA_VERSION} at ${CUDAToolkit_INCLUDE_DIRS}")
    endif()
else()
    # Fallback to older FindCUDA
    find_package(CUDA QUIET)
    if(CUDA_FOUND)
        message(STATUS "Found CUDA ${CUDA_VERSION} at ${CUDA_INCLUDE_DIRS}")
    endif()
endif()

if(NOT CUDA_FOUND)
    message(WARNING "CUDA was requested but not found. Building without CUDA support.")
    set(ENABLE_CUDA OFF CACHE BOOL "Enable CUDA support" FORCE)
endif()
