#!/bin/bash

$WASI_SDK_PATH/bin/clang \
    --target=wasm32-wasi \
    --sysroot=$WASI_SDK_PATH/share/wasi-sysroot \
    -msimd128 \
    -nostartfiles \
    -O3 \
    -flto \
    -o transport.wasm \
    transport.cpp
