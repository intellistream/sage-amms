#!/bin/bash
# Please make sure cuda is fully installed at /usr/local/cuda !!!!

set -e

get_mem_available_gib() {
    awk '/MemAvailable:/ {printf "%.0f", $2/1024/1024}' /proc/meminfo
}

# Function to get the major and minor version of CUDA using nvcc
get_cuda_version() {
    # Check if nvcc is available
    if command -v /usr/local/cuda/bin/nvcc &> /dev/null; then
        # Use nvcc to extract the version number
        cuda_version=$(/usr/local/cuda/bin/nvcc --version | grep "release" | grep -oP 'release \K[0-9]+\.[0-9]+')
    else
        echo "CUDA is not installed or nvcc is not in your PATH."
        exit 1
    fi
    echo $cuda_version
}

# Extract the major and minor version of CUDA
cuda_version=$(get_cuda_version)
echo "First, make sure you have sudo"
sudo ls
echo "Detected CUDA Version: $cuda_version"

# Replace dots with hyphens for the package versioning format used by Ubuntu packages
package_version=${cuda_version//./-}

# Formulate the package name
libcublas_package="libcublas-$package_version"

# Install the corresponding libcublas package
echo "Installing $libcublas_package..."
sudo apt-get update
sudo apt-get install -y $libcublas_package

if [ $? -eq 0 ]; then
    echo "$libcublas_package installation successful."
else
    echo "Failed to install $libcublas_package."
fi
echo "Installing others..."
sudo apt install -y liblapack-dev libblas-dev
sudo apt-get install -y graphviz
sudo apt-get install -y libcudnn8 libcudnn8-dev
python -m pip install matplotlib pandas==2.0.0
python -m pip install "torch>=1.13.0"
echo "Build LIBAMM and PyAMM"
# Step 1: Configure the project
export CUDACXX=/usr/local/cuda/bin/nvcc
FAST_BUILD_MEMORY_GB=${AMMS_FAST_BUILD_MEMORY_GB:-48}
AVAILABLE_GB=$(get_mem_available_gib)

if [ "$AVAILABLE_GB" -ge "$FAST_BUILD_MEMORY_GB" ]; then
    AMMS_LOW_MEMORY_BUILD=${AMMS_LOW_MEMORY_BUILD:-0}
else
    AMMS_LOW_MEMORY_BUILD=${AMMS_LOW_MEMORY_BUILD:-1}
fi

mkdir build
cd build &&cmake -DCMAKE_PREFIX_PATH=`python3 -c 'import torch;print(torch.utils.cmake_prefix_path)'` -DENABLE_HDF5=ON -DENABLE_PYBIND=ON -DCMAKE_INSTALL_PREFIX=/usr/local/lib -DENABLE_PAPI=OFF -DAMMS_LOW_MEMORY_BUILD=${AMMS_LOW_MEMORY_BUILD} ..

# Step 2: Determine threads
if [ -n "${AMMS_MAX_JOBS}" ]; then
    max_threads=${AMMS_MAX_JOBS}
elif [ "$AMMS_LOW_MEMORY_BUILD" = "1" ]; then
    max_threads=1
else
    max_threads=$(( $(nproc) / 2 ))
    if [ "$max_threads" -lt 1 ]; then
        max_threads=1
    fi
fi

echo "Build mode: AMMS_LOW_MEMORY_BUILD=${AMMS_LOW_MEMORY_BUILD}, MemAvailable=${AVAILABLE_GB}GiB, jobs=${max_threads}"

# Step 3: Build the project
cmake --build . --parallel $max_threads
