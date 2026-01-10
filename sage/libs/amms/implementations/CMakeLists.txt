
cmake_minimum_required(VERSION 3.14)
project(isage_amms CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)
message(STATUS "=== isage_amms Build Configuration ===")
message(STATUS "CMAKE_BUILD_TYPE: ${CMAKE_BUILD_TYPE}")
message(STATUS "CMAKE_CXX_COMPILER: ${CMAKE_CXX_COMPILER}")

# Custom CMake modules
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake;${CMAKE_MODULE_PATH}")
include(cmake/macros.cmake)
include(cmake/default.cmake)
include(cmake/FindCuda.cmake)
include(cmake/FindTorch.cmake)

# Find PyTorch
find_package(Torch REQUIRED)
message(STATUS "Found Torch version: ${Torch_VERSION}")
message(STATUS "Torch libraries: ${TORCH_LIBRARIES}")
message(STATUS "Torch include directories: ${TORCH_INCLUDE_DIRS}")

# Add Torch dependencies
include_directories(${TORCH_INCLUDE_DIRS})
set(LIBRARIES ${LIBRARIES} ${TORCH_LIBRARIES})

# Unity Build for faster compilation
set(CMAKE_UNITY_BUILD ON)
set(CMAKE_UNITY_BUILD_BATCH_SIZE 2)
message(STATUS "Unity Build enabled with batch size: ${CMAKE_UNITY_BUILD_BATCH_SIZE}")

# C++ Standard and compiler flags
set(CMAKE_CXX_FLAGS "-std=c++20 -Wall -Werror=return-type -Werror=unused-variable -Werror=unused-parameter")

# Memory optimization flags (GCC-specific params will be ignored by Clang)
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    set(MEMORY_OPTIMIZATION_FLAGS "-g0 -O0 -fno-var-tracking -ftemplate-depth=128 --param ggc-min-expand=20 --param ggc-min-heapsize=32768")
else()
    set(MEMORY_OPTIMIZATION_FLAGS "-g0 -O0 -fno-var-tracking -ftemplate-depth=128")
endif()

set(CMAKE_CXX_FLAGS_DEBUG "${MEMORY_OPTIMIZATION_FLAGS} -DNO_RACE_CHECK -DLibAMM_DEBUG_MODE=1")
set(CMAKE_CXX_FLAGS_RELEASE "-Wno-ignored-qualifiers -Wno-sign-compare ${MEMORY_OPTIMIZATION_FLAGS}")

message(STATUS "CXX flags (Release): ${CMAKE_CXX_FLAGS_RELEASE}")

# OpenCL support (optional)
option(ENABLE_OPENCL "Enable OpenCL support" OFF)
if(NOT ENABLE_OPENCL)
    message(STATUS "OpenCL support: DISABLED")
    set(LibAMM_CL 0)
else()
    message(STATUS "OpenCL support: ENABLED")
    set(LibAMM_CL 1)
    set(LIBRARIES ${LIBRARIES} OpenCL)
endif()
configure_file(
    "${PROJECT_SOURCE_DIR}/include/opencl_config.h.in"
    "${PROJECT_BINARY_DIR}/include/opencl_config.h"
)

# PAPI support (optional)
option(ENABLE_PAPI "Enable PAPI hardware counters" OFF)
if(NOT ENABLE_PAPI)
    message(STATUS "PAPI support: DISABLED")
    set(LibAMM_PAPI 0)
else()
    message(STATUS "PAPI support: ENABLED")
    set(LibAMM_PAPI 1)

    find_package(PkgConfig QUIET)
    if(PKG_CONFIG_FOUND)
        pkg_check_modules(PAPI papi)
    endif()

    if(PAPI_FOUND)
        message(STATUS "Found PAPI: ${PAPI_LIBRARIES}")
        include_directories(${PAPI_INCLUDE_DIRS})
        link_directories(${PAPI_LIBRARY_DIRS})
        set(LIBRARIES ${LIBRARIES} ${PAPI_LIBRARIES})
    else()
        find_library(libPAPI NAMES papi libpapi.so
                     PATHS /usr/lib /usr/local/lib /usr/lib/x86_64-linux-gnu)
        if(libPAPI)
            message(STATUS "Found PAPI library: ${libPAPI}")
            set(LIBRARIES ${LIBRARIES} ${libPAPI})
        else()
            message(WARNING "PAPI requested but not found. Install with: sudo apt-get install libpapi-dev")
            set(LibAMM_PAPI 0)
        endif()
    endif()
endif()
configure_file(
    "${PROJECT_SOURCE_DIR}/include/papi_config.h.in"
    "${PROJECT_BINARY_DIR}/include/papi_config.h"
)

# PyBind11 support
option(ENABLE_PYBIND "Build Python bindings" OFF)

# Logging level
if(LibAMM_LOGGING_LEVEL)
    get_log_level_value(LibAMM_LOGGING_VALUE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DLibAMM_LOGGING_LEVEL=${LibAMM_LOGGING_VALUE}")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -DLibAMM_LOGGING_LEVEL=${LibAMM_LOGGING_VALUE}")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DLibAMM_LOGGING_LEVEL=${LibAMM_LOGGING_VALUE}")
    message(STATUS "Logging level: ${LibAMM_LOGGING_LEVEL}")
else()
    message(STATUS "Logging level: ALL (default)")
endif()

# Unit tests
option(ENABLE_UNIT_TESTS "Enable unit tests" OFF)
message(STATUS "Unit tests: ${ENABLE_UNIT_TESTS}")

# Print configuration summary
message(STATUS "Include directories:")
get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
foreach(dir ${dirs})
    message(STATUS "  - ${dir}")
endforeach()
message(STATUS "Libraries: ${LIBRARIES}")

# Build LibAMM shared library
add_subdirectory(src)

get_sources(LibAMM_SOURCE_FILES)
get_headers(LibAMM_HEADER_FILES)
add_library(LibAMM SHARED ${LibAMM_SOURCE_FILES} ${LibAMM_HEADER_FILES} ${CMAKE_CURRENT_BINARY_DIR})
set_property(TARGET LibAMM PROPERTY CXX_STANDARD 20)

# Exclude specific files from Unity Build to avoid conflicts
set_source_files_properties(
    "${PROJECT_SOURCE_DIR}/src/myVecAdd.cpp"
    "${PROJECT_SOURCE_DIR}/src/pythonBoundings.cpp"
    PROPERTIES SKIP_UNITY_BUILD_INCLUSION TRUE
)

target_include_directories(LibAMM PUBLIC 
    "include"
    "${CMAKE_CURRENT_BINARY_DIR}"
    "thirdparty/papi_build/include"
)
target_link_libraries(LibAMM PUBLIC ${LIBRARIES})

# Unit tests
if(ENABLE_UNIT_TESTS)
    add_subdirectory(test)
endif()

# Python bindings
if(NOT ENABLE_PYBIND)
    message(STATUS "Python bindings: DISABLED")
    set(LibAMM_PYBIND 0)
else()
    message(STATUS "Python bindings: ENABLED")
    
    # Find or fetch pybind11
    find_package(pybind11 CONFIG QUIET)
    if(NOT pybind11_FOUND)
        message(STATUS "Fetching pybind11...")
        include(FetchContent)
        FetchContent_Declare(
            pybind11
            GIT_REPOSITORY https://github.com/pybind/pybind11.git
            GIT_TAG v2.13.5
            GIT_SHALLOW TRUE
        )
        FetchContent_MakeAvailable(pybind11)
        if(NOT DEFINED pybind11_VERSION)
            set(pybind11_VERSION "2.13.5")
        endif()
    else()
        message(STATUS "Found pybind11: ${pybind11_VERSION}")
    endif()

    # Build PyAMM module
    pybind11_add_module(PyAMM ${PROJECT_SOURCE_DIR}/src/PyAMM.cpp)
    set_property(TARGET PyAMM PROPERTY CXX_STANDARD 20)
    set_target_properties(PyAMM PROPERTIES UNITY_BUILD OFF)
    
    # Find torch_python library
    find_library(TORCH_PYTHON_LIBRARY 
                 NAMES torch_python libtorch_python
                 PATHS 
                     "${TORCH_INSTALL_PREFIX}/lib"
                     "${Torch_DIR}/../../../lib"
                     "${CMAKE_PREFIX_PATH}/lib"
                 NO_DEFAULT_PATH)
    
    if(NOT TORCH_PYTHON_LIBRARY)
        find_library(TORCH_PYTHON_LIBRARY 
                     NAMES torch_python libtorch_python)
    endif()
    
    if(TORCH_PYTHON_LIBRARY)
        message(STATUS "Found torch_python: ${TORCH_PYTHON_LIBRARY}")
        target_link_libraries(PyAMM PUBLIC ${LIBRARIES} LibAMM ${TORCH_PYTHON_LIBRARY})
    else()
        message(WARNING "torch_python not found, linking without it")
        target_link_libraries(PyAMM PUBLIC ${LIBRARIES} LibAMM)
    endif()
    
    install(TARGETS PyAMM LIBRARY DESTINATION .)
    set(LibAMM_PYBIND 1)
endif()

configure_file(
    "${PROJECT_SOURCE_DIR}/include/pybind_config.h.in"
    "${PROJECT_BINARY_DIR}/include/pybind_config.h"
)

# Installation
install(DIRECTORY "include" DESTINATION "/LibAMM" COMPONENT LibAMM)

# Dataset copying (optional, for benchmarking)
option(LIBAMM_SKIP_DATASET_COPY "Skip copying benchmark datasets" OFF)
set(LIBAMM_DATASET_SOURCE_DIR "${CMAKE_SOURCE_DIR}/benchmark/datasets" CACHE PATH "Path to benchmark datasets")

if(NOT LIBAMM_SKIP_DATASET_COPY AND EXISTS "${LIBAMM_DATASET_SOURCE_DIR}")
    message(STATUS "Copying datasets from: ${LIBAMM_DATASET_SOURCE_DIR}")
    file(COPY "${LIBAMM_DATASET_SOURCE_DIR}/" DESTINATION "${CMAKE_BINARY_DIR}/benchmark/datasets/")
else()
    message(STATUS "Dataset copy: SKIPPED")
endif()