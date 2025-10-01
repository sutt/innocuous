echo "starting hash..."
sha256sum .venv/lib/python3.12/site-packages/llama_cpp/lib/libggml-base.so 

uv pip uninstall llama-cpp-python

# v1 compile flags
# export CMAKE_ARGS='-DGGML_BLAS=OFF -DGGML_OPENMP=OFF -DLLAMA_NATIVE=OFF -DLLAMA_AVX=ON -DLLAMA_AVX2=ON -DLLAMA_FMA=ON -DLLAMA_F16C=ON -DCMAKE_BUILD_TYPE=Release'

# v2 compile flags 
export CMAKE_ARGS='-DGGML_BLAS=OFF -DGGML_OPENMP=OFF -DLLAMA_NATIVE=OFF -DLLAMA_AVX=OFF -DLLAMA_AVX2=OFF -DLLAMA_FMA=OFF -DLLAMA_F16C=OFF -DCMAKE_BUILD_TYPE=Release'

# non version compile flags
export CFLAGS='-ffloat-store -fno-unsafe-math-optimizations -ffp-contract=off'
export CXXFLAGS="$CFLAGS"
export FORCE_CMAKE=1

# More CMake messages during configure & generate
export CMAKE_MESSAGE_LOG_LEVEL=VERBOSE
export CMAKE_VERBOSE_MAKEFILE=ON
export NINJAFLAGS=-v

uv pip install -v --no-cache-dir --no-binary=llama-cpp-python 'llama-cpp-python==0.3.16'

echo "ending hash..."
sha256sum .venv/lib/python3.12/site-packages/llama_cpp/lib/libggml-base.so 

# local, installing with all flags commented out:
# start: 55ad727f51cb5bc37a0d9b3aef0a767915c52c13c50a8c75a69d4e880d01ef36
# end:   cd1d4eb79c133129e1f1b013d3ac1fa642bf6eedfbd3c1c415d57035e152a65f 

# local, installing with all flags uncommented:
# start: cd1d4eb79c133129e1f1b013d3ac1fa642bf6eedfbd3c1c415d57035e152a65f 
# enc: 7b35b65744b20dd6b1083226d0dfb537830e46d275d8b5d4a7aeb0e7ce01ceef
# output: align-local-2

# local, v2 flags enabled
# output:align-local-3.txt
