#!/bin/bash

sysbench memory \
    --memory-block-size=1M \
    --memory-total-size=10G \
    run
