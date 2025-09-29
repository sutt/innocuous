#!/usr/bin/env bash
set -euo pipefail

ver(){ if command -v "$1" &>/dev/null; then printf "%-12s %s\n" "$1" "$("$@" | head -n1)"; else printf "%-12s %s\n" "$1" "not found\n"; fi; }

echo "=== System ==="
printf "Hostname:  %s\n" "$(hostname -f 2>/dev/null || hostname)"
printf "Kernel:    %s\n" "$(uname -srvmo)"
printf "Arch:      %s\n" "$(uname -m)"
[ -f /etc/os-release ] && . /etc/os-release && printf "OS:        %s %s (%s %s)\n" "$NAME" "$VERSION" "$ID" "$VERSION_ID"
ver ldd --version   # shows glibc/musl

echo
echo "=== Toolchain ==="
ver gcc --version
ver g++ --version
ver make --version
ver cmake --version
ver ninja --version
ver pkg-config --version
ver python3 --version
ver pip --version
ver uv --version

echo
echo "=== BLAS (best-effort) ==="
command -v ldconfig &>/dev/null && ldconfig -p 2>/dev/null | grep -i openblas | head -n3 || true
python3 - <<'PY' 2>/dev/null || true
try:
    import numpy, numpy.__config__ as c
    print("numpy", numpy.__version__)
    c.show()
except Exception:
    pass
PY
