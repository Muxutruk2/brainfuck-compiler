#!/bin/env bash

# Create folders
mkdir -p build-c build

# Clean build
rm -f build-c/* 
rm -f build/*

# Compile bf to C
for f in src/*.bf; do
    python3 main.py $f --output build-c/$(basename $f ".bf") > /dev/null
done

# Compile C
for c in build-c/*.c; do
    gcc $c -o build/$(basename $c .c)
done
