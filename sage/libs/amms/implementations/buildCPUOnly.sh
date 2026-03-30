#!/bin/bash

set -e

get_mem_available_gib() {
	awk '/MemAvailable:/ {printf "%.0f", $2/1024/1024}' /proc/meminfo
}

echo "First, make sure you have sudo"
sudo ls
echo "Installing others..."
sudo apt-get install -y graphviz
python -m pip install matplotlib pandas==2.0.0
python -m pip install "torch>=1.13.0" --index-url https://download.pytorch.org/whl/cpu
echo "Build LibAMM and PyAMM"
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
