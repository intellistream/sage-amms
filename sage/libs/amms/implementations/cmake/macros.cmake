# Custom CMake macros for LibAMM project

# Global lists to collect source and header files
set(GLOBAL_SOURCE_FILES "" CACHE INTERNAL "List of all source files")
set(GLOBAL_HEADER_FILES "" CACHE INTERNAL "List of all header files")

# Macro to add source files to the global list
macro(add_sources)
    file(RELATIVE_PATH _relPath "${PROJECT_SOURCE_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
    foreach(_src ${ARGN})
        if(_relPath)
            list(APPEND GLOBAL_SOURCE_FILES "${_relPath}/${_src}")
        else()
            list(APPEND GLOBAL_SOURCE_FILES "${_src}")
        endif()
    endforeach()
    set(GLOBAL_SOURCE_FILES ${GLOBAL_SOURCE_FILES} CACHE INTERNAL "List of all source files")
endmacro()

# Macro to add header files to the global list
macro(add_headers)
    file(RELATIVE_PATH _relPath "${PROJECT_SOURCE_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
    foreach(_hdr ${ARGN})
        if(_relPath)
            list(APPEND GLOBAL_HEADER_FILES "${_relPath}/${_hdr}")
        else()
            list(APPEND GLOBAL_HEADER_FILES "${_hdr}")
        endif()
    endforeach()
    set(GLOBAL_HEADER_FILES ${GLOBAL_HEADER_FILES} CACHE INTERNAL "List of all header files")
endmacro()

# Function to retrieve all collected source files
function(get_sources out_var)
    set(${out_var} ${GLOBAL_SOURCE_FILES} PARENT_SCOPE)
endfunction()

# Function to retrieve all collected header files
function(get_headers out_var)
    set(${out_var} ${GLOBAL_HEADER_FILES} PARENT_SCOPE)
endfunction()
