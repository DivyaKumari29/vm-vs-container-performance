#!/bin/bash

set -e

echo "Updating packages..."
sudo apt update

echo "Installing benchmark dependencies..."
sudo apt install -y \
    sysbench \
    fio \
    iperf3 \
    curl \
    python3 \
    python3-pip

echo "Installing Python packages..."
pip3 install --user pandas psutil matplotlib

echo "VM environment setup completed."o
