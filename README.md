# Performance Analysis of Virtual Machines and Containers

## Abstract

This project evaluates the performance of virtual machines and Docker containers under comparable workloads. The study measures CPU, memory, disk I/O, network throughput, application performance, startup time, and API scalability.

## Objectives

- Compare VM and container performance.
- Measure CPU and memory performance.
- Evaluate disk I/O and network throughput.
- Compare FastAPI application performance.
- Measure application startup time.
- Analyze scalability under different workloads.
- Present the measured results using statistical analysis and graphs.

## Experimental Environment

### Virtual Machine

- VMware Workstation
- Ubuntu 22.04.5 LTS
- 4 vCPUs
- 8 GB RAM
- 60 GB virtual disk
- NAT networking

### Docker Container

- Ubuntu 24.04 based benchmark image
- 4 CPU limit
- 8 GB memory limit

## Workloads

The following workloads were evaluated:

1. CPU
2. Memory
3. Disk I/O
4. Network
5. FastAPI application
6. Startup time
7. API scalability

## Analysis

The benchmark results were stored as raw data and processed using Python, Pandas, and Matplotlib.

The project includes:

- Raw benchmark results
- Processed CSV files
- Statistical analysis
- Performance graphs
- Jupyter notebook
- VM and Docker benchmark scripts

## Conclusion

The experiment demonstrates the performance differences between virtual machines and containers under controlled workloads. Containers generally provide lightweight execution and faster startup, while virtual machines provide stronger isolation through a complete guest operating system.

The final conclusions are based on the actual measurements collected during the experiments.

## Project Structure

```text
vm-vs-container-performance/
├── analysis/
├── api/
├── docker/
├── docs/
├── results/
├── scripts/
├── vm/
├── workloads/
├── .gitignore
└── README.md
