#!/bin/bash

mkdir -p results/raw/disk/manual

echo "Sequential write"
dd if=/dev/zero of=/tmp/testfile bs=1M count=1024 conv=fdatasync

echo "Sequential read"
dd if=/tmp/testfile of=/dev/null bs=1M

rm -f /tmp/testfile
