# Custom install script for llama-cpp-python.
# Eliminates model drift caused by different compile options 
# across platforms / architectures.

uv pip uninstall llama-cpp-python

# Optional: env vars for the build
# enabling these should allow for a build log to print during install
export CMAKE_MESSAGE_LOG_LEVEL=VERBOSE
export SCIKIT_BUILD_CORE_NO_CLEAN=1
export NINJAFLAGS=-v      # if Ninja is used
export VERBOSE=1          # if Make is used

# Optional: make logs chatty and keep build dir so you can inspect CMakeCache.txt
export CMAKE_MESSAGE_LOG_LEVEL=VERBOSE
export SCIKIT_BUILD_CORE_NO_CLEAN=1

# Optional: Ensure same compilers on both hosts (adjust paths if needed)
# export CC=${CC:-/usr/bin/cc}
# export CXX=${CXX:-/usr/bin/c++}

# Note: the flags are passed to llama.cpp and the flag names are recently
# updated in that library in the form of:
# LLAMA_XXX -> GGML_XXX

# Explicit pip install command
# use --no-config to avoid taking config from pyproject.toml here
uv pip install -v \
  --no-config \
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
