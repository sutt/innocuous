
uv pip uninstall llama-cpp-python

export CMAKE_MESSAGE_LOG_LEVEL=VERBOSE
export SCIKIT_BUILD_CORE_NO_CLEAN=1
export NINJAFLAGS=-v      # if Ninja is used
export VERBOSE=1          # if Make is used

# uv pip install -v \
#   --no-binary=llama-cpp-python \
#   --force-reinstall \
#   --config-settings=build-type=Release \
#   --config-settings=cmake.generator="Unix Makefiles" \
#   --config-settings=cmake.define.GGML_BLAS=OFF \
#   --config-settings=cmake.define.GGML_OPENMP=OFF \
#   --config-settings=cmake.define.LLAMA_NATIVE=OFF \
#   --config-settings=cmake.define.LLAMA_AVX=ON \
#   --config-settings=cmake.define.LLAMA_AVX2=ON \
#   --config-settings=cmake.define.LLAMA_FMA=ON \
#   --config-settings=cmake.define.LLAMA_F16C=ON \
#   llama-cpp-python==0.3.16

# Optional: make logs chatty and keep build dir so you can inspect CMakeCache.txt
export CMAKE_MESSAGE_LOG_LEVEL=VERBOSE
export SCIKIT_BUILD_CORE_NO_CLEAN=1

# Ensure same compilers on both hosts (adjust paths if needed)
# export CC=${CC:-/usr/bin/cc}
# export CXX=${CXX:-/usr/bin/c++}

# uv pip install -v \
#   --no-cache-dir \
#   --no-binary=llama-cpp-python \
#   --force-reinstall \
#   --config-settings=cmake.define.CMAKE_BUILD_TYPE=Release \
#   --config-settings=cmake.args="-GUnix Makefiles" \
#   --config-settings=cmake.verbose=true \
#   --config-settings=cmake.define.GGML_NATIVE=OFF \
#   --config-settings=cmake.define.GGML_OPENMP=OFF \
#   --config-settings=cmake.define.GGML_BLAS=OFF \
#   --config-settings=cmake.define.GGML_AVX=ON \
#   --config-settings=cmake.define.GGML_AVX2=ON \
#   --config-settings=cmake.define.GGML_F16C=ON \
#   --config-settings=cmake.define.GGML_FMA=OFF \
#   llama-cpp-python==0.3.16


uv pip install -v \
  --no-cache-dir \
  --no-binary=llama-cpp-python \
  --force-reinstall \
  --config-settings=cmake.define.CMAKE_BUILD_TYPE=Release \
  --config-settings=cmake.verbose=true \
  --config-settings=cmake.define.GGML_NATIVE=OFF \
    --config-settings=cmake.define.GGML_CPU_NO_DISPATCH=ON \
    --config-settings=cmake.define.GGML_OPENMP=OFF \
    --config-settings=cmake.define.GGML_BLAS=OFF \
    --config-settings=cmake.define.GGML_AVX=OFF \
    --config-settings=cmake.define.GGML_AVX2=OFF \
    --config-settings=cmake.define.GGML_F16C=OFF \
    --config-settings=cmake.define.GGML_FMA=OFF \
    --config-settings=cmake.define.GGML_AVX512=OFF \
  llama-cpp-python==0.3.16
