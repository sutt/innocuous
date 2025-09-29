uv pip uninstall llama-cpp-python

export CMAKE_ARGS='-DGGML_BLAS=OFF -DGGML_OPENMP=OFF -DLLAMA_NATIVE=OFF -DLLAMA_AVX=ON -DLLAMA_AVX2=ON -DLLAMA_FMA=ON -DLLAMA_F16C=ON -DCMAKE_BUILD_TYPE=Release'
export CFLAGS='-ffloat-store -fno-unsafe-math-optimizations -ffp-contract=off'
export CXXFLAGS="$CFLAGS"
export FORCE_CMAKE=1

uv pip install --no-cache-dir --no-binary=llama-cpp-python 'llama-cpp-python==0.3.16'
