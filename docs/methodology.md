# Methodology

The experiment compares the performance of a virtual machine and a Docker container under controlled workloads.

## Virtual Machine

- Ubuntu 22.04.5 LTS
- 4 vCPUs
- 8 GB RAM
- 60 GB virtual disk
- VMware Workstation
- NAT networking

## Container

- Ubuntu 24.04 based benchmark image
- 4 CPU limit
- 8 GB memory limit
- Docker

## Workloads

The following workloads were evaluated:

1. CPU performance
2. Memory performance
3. Sequential disk I/O
4. Random disk I/O
5. Network throughput
6. FastAPI application performance
7. Application startup time
8. API scalability

Each environment was tested using comparable workloads and resource limits.

## Performance Metrics

The measured metrics include:

- Events per second
- Memory throughput
- Disk bandwidth
- Network throughput
- API requests per second
- API latency
- Startup time

The results were stored as raw measurements and processed using Python and Pandas.
