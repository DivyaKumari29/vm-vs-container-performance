import pandas as pd
import os

print("=" * 60)
print("VM vs CONTAINER PERFORMANCE DIFFERENCES")
print("=" * 60)


# ============================================================
# CPU
# ============================================================

cpu_file = "results/processed/cpu_statistics.csv"

if os.path.exists(cpu_file):

    cpu = pd.read_csv(
        cpu_file,
        index_col=0
    )

    if "vm" in cpu.index and "container" in cpu.index:

        vm = cpu.loc["vm", "mean"]
        container = cpu.loc["container", "mean"]

        difference = ((container - vm) / vm) * 100

        print("\nCPU:")
        print(f"VM mean        : {vm:.2f} events/sec")
        print(f"Container mean : {container:.2f} events/sec")
        print(f"Difference     : {difference:.2f}%")

    else:
        print("\nCPU:")
        print("VM or Container data not found.")


# ============================================================
# MEMORY
# ============================================================

memory_file = "results/processed/memory_statistics.csv"

if os.path.exists(memory_file):

    memory = pd.read_csv(
        memory_file,
        index_col=0
    )

    if "vm" in memory.index and "container" in memory.index:

        vm = memory.loc["vm", "mean"]
        container = memory.loc["container", "mean"]

        difference = ((container - vm) / vm) * 100

        print("\nMemory:")
        print(f"VM mean        : {vm:.2f} MiB/sec")
        print(f"Container mean : {container:.2f} MiB/sec")
        print(f"Difference     : {difference:.2f}%")

    else:
        print("\nMemory:")
        print("VM or Container data not found.")


# ============================================================
# NETWORK
# ============================================================

network_file = "results/processed/network_results.csv"

if os.path.exists(network_file):

    network = pd.read_csv(network_file)

    vm_row = network[
        network["environment"].str.lower() == "vm"
    ]

    container_row = network[
        network["environment"].str.lower() == "container"
    ]

    if not vm_row.empty and not container_row.empty:

        vm = vm_row.iloc[0]["throughput"]
        container = container_row.iloc[0]["throughput"]

        difference = ((container - vm) / vm) * 100

        print("\nNetwork:")
        print(f"VM           : {vm:.2f}")
        print(f"Container    : {container:.2f}")
        print(f"Difference   : {difference:.2f}%")

    else:
        print("\nNetwork:")
        print("VM or Container data not found.")


# ============================================================
# DISK
# ============================================================

disk_file = "results/processed/disk_results.csv"

if os.path.exists(disk_file):

    disk = pd.read_csv(disk_file)

    print("\nDisk Performance:")

    for workload in disk["workload"].unique():

        data = disk[
            disk["workload"] == workload
        ]

        vm_row = data[
            data["environment"].str.lower() == "vm"
        ]

        container_row = data[
            data["environment"].str.lower() == "container"
        ]

        if not vm_row.empty and not container_row.empty:

            vm = vm_row.iloc[0]["bandwidth"]
            container = container_row.iloc[0]["bandwidth"]

            difference = ((container - vm) / vm) * 100

            print(f"\n{workload}:")
            print(f"  VM         : {vm:.2f}")
            print(f"  Container  : {container:.2f}")
            print(f"  Difference : {difference:.2f}%")


# ============================================================
# API PERFORMANCE
# ============================================================

api_file = "results/processed/api_results.csv"

if os.path.exists(api_file):

    api = pd.read_csv(api_file)

    print("\nAPI Performance:")

    for _, row in api.iterrows():

        print(f"\nTest: {row['test']}")
        print(
            f"  Requests/sec : "
            f"{row['requests_per_sec']:.2f}"
        )

        if pd.notna(row["time_per_request_ms"]):
            print(
                f"  Time/request : "
                f"{row['time_per_request_ms']:.2f} ms"
            )

        if pd.notna(row["failed_requests"]):
            print(
                f"  Failed       : "
                f"{int(row['failed_requests'])}"
            )


# ============================================================
# STARTUP TIME
# ============================================================

print("\nStartup Time:")
print("Docker startup : 0.363 seconds")
print("Health response: 0.055 seconds")
print("VM startup     : Not recorded")


# ============================================================
# FINAL NOTE
# ============================================================

print("\n" + "=" * 60)
print("INTERPRETATION")
print("=" * 60)

print("""
Positive percentage  = Container performed higher
Negative percentage  = Container performed lower

Percentage formula:

((Container - VM) / VM) * 100

Only metrics with actual VM and Container
measurements are compared.
""")

print("=" * 60)
