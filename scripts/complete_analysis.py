import os
import re
import glob
import pandas as pd
import matplotlib.pyplot as plt

RAW = "results/raw"
PROCESSED = "results/processed"
FIGURES = "results/figures"

os.makedirs(PROCESSED, exist_ok=True)
os.makedirs(FIGURES, exist_ok=True)


# ============================================================
# 1. CPU
# ============================================================

cpu_rows = []

for environment in ["vm", "container"]:
    files = glob.glob(f"{RAW}/cpu/{environment}/run*.txt")

    for filename in sorted(files):
        text = open(filename, errors="ignore").read()

        match = re.search(
            r"events per second:\s*([\d.]+)",
            text
        )

        if match:
            run = re.search(r"run(\d+)", filename)
            cpu_rows.append({
                "environment": environment,
                "threads": 4,
                "run": int(run.group(1)) if run else 0,
                "events_per_second": float(match.group(1))
            })

cpu_df = pd.DataFrame(cpu_rows)

if not cpu_df.empty:
    cpu_df.to_csv(
        f"{PROCESSED}/cpu_results.csv",
        index=False
    )

    summary = cpu_df.groupby("environment")[
        "events_per_second"
    ].agg(["mean", "median", "min", "max", "std"])

    summary.to_csv(
        f"{PROCESSED}/cpu_statistics.csv"
    )

    plt.figure()

    for environment in cpu_df["environment"].unique():
        data = cpu_df[
            cpu_df["environment"] == environment
        ]

        plt.plot(
            range(1, len(data) + 1),
            data["events_per_second"],
            marker="o",
            label=environment
        )

    plt.title("CPU Performance Across Repeated Runs")
    plt.xlabel("Run Number")
    plt.ylabel("Events per Second")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(
        f"{FIGURES}/cpu_performance.png",
        dpi=300
    )
    plt.close()


# ============================================================
# 2. CPU SCALABILITY
# ============================================================

scale_rows = []

for environment in ["vm", "container"]:

    files = glob.glob(
        f"{RAW}/cpu/scalability/{environment}/*_threads.txt"
    )

    for filename in files:

        text = open(filename, errors="ignore").read()

        thread_match = re.search(
            r"(\d+)_threads",
            filename
        )

        event_match = re.search(
            r"events per second:\s*([\d.]+)",
            text
        )

        if thread_match and event_match:

            scale_rows.append({
                "environment": environment,
                "threads": int(thread_match.group(1)),
                "events_per_second":
                    float(event_match.group(1))
            })

scale_df = pd.DataFrame(scale_rows)

if not scale_df.empty:

    scale_df = scale_df.sort_values(
        ["environment", "threads"]
    )

    scale_df.to_csv(
        f"{PROCESSED}/cpu_scalability.csv",
        index=False
    )

    plt.figure()

    for environment in scale_df["environment"].unique():

        data = scale_df[
            scale_df["environment"] == environment
        ]

        plt.plot(
            data["threads"],
            data["events_per_second"],
            marker="o",
            label=environment
        )

    plt.title("CPU Performance vs Number of Threads")
    plt.xlabel("Number of Threads")
    plt.ylabel("Events per Second")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        f"{FIGURES}/cpu_scalability.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 3. MEMORY
# ============================================================

memory_rows = []

for environment in ["vm", "container"]:

    files = glob.glob(
        f"{RAW}/memory/{environment}/run*.txt"
    )

    for filename in sorted(files):

        text = open(filename, errors="ignore").read()

        matches = re.findall(
            r"([\d.]+)\s+MiB/sec",
            text
        )

        if matches:

            run = re.search(
                r"run(\d+)",
                filename
            )

            memory_rows.append({
                "environment": environment,
                "run": int(run.group(1)) if run else 0,
                "MiB_per_sec": float(matches[-1])
            })

memory_df = pd.DataFrame(memory_rows)

if not memory_df.empty:

    memory_df.to_csv(
        f"{PROCESSED}/memory_results.csv",
        index=False
    )

    memory_summary = memory_df.groupby(
        "environment"
    )["MiB_per_sec"].agg(
        ["mean", "median", "min", "max", "std"]
    )

    memory_summary.to_csv(
        f"{PROCESSED}/memory_statistics.csv"
    )

    plt.figure()

    memory_summary["mean"].plot(
        kind="bar"
    )

    plt.title("Average Memory Performance")
    plt.xlabel("Environment")
    plt.ylabel("MiB/sec")
    plt.tight_layout()

    plt.savefig(
        f"{FIGURES}/memory_performance.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 4. DISK
# ============================================================

disk_rows = []

for environment in ["vm", "container"]:

    for workload in [
        "seq-read",
        "seq-write",
        "random-read",
        "random-write"
    ]:

        filename = (
            f"{RAW}/disk/{environment}/{workload}.txt"
        )

        if not os.path.exists(filename):
            continue

        text = open(filename, errors="ignore").read()

        matches = re.findall(
            r"bw=([\d.]+)([KMG]iB/s)",
            text
        )

        if matches:

            value, unit = matches[0]

            disk_rows.append({
                "environment": environment,
                "workload": workload,
                "bandwidth": float(value),
                "unit": unit
            })

disk_df = pd.DataFrame(disk_rows)

if not disk_df.empty:

    disk_df.to_csv(
        f"{PROCESSED}/disk_results.csv",
        index=False
    )

    for workload in disk_df["workload"].unique():

        data = disk_df[
            disk_df["workload"] == workload
        ]

        plt.figure()

        plt.bar(
            data["environment"],
            data["bandwidth"]
        )

        plt.title(
            f"Disk Performance - {workload}"
        )

        plt.xlabel("Environment")
        plt.ylabel("Bandwidth")
        plt.tight_layout()

        plt.savefig(
            f"{FIGURES}/disk_{workload}.png",
            dpi=300
        )

        plt.close()


# ============================================================
# 5. NETWORK
# ============================================================

network_rows = []

network_files = {
    "VM": f"{RAW}/network-vm.txt",
    "Container": f"{RAW}/network-container.txt"
}

for environment, filename in network_files.items():

    if not os.path.exists(filename):
        continue

    text = open(filename, errors="ignore").read()

    matches = re.findall(
        r"([\d.]+)\s+([KMG]bits/sec)",
        text
    )

    if matches:

        value, unit = matches[-1]

        network_rows.append({
            "environment": environment,
            "throughput": float(value),
            "unit": unit
        })

network_df = pd.DataFrame(network_rows)

if not network_df.empty:

    network_df.to_csv(
        f"{PROCESSED}/network_results.csv",
        index=False
    )

    plt.figure()

    plt.bar(
        network_df["environment"],
        network_df["throughput"]
    )

    plt.title("Network Throughput: VM vs Container")
    plt.xlabel("Environment")
    plt.ylabel("Throughput")
    plt.tight_layout()

    plt.savefig(
        f"{FIGURES}/network_throughput.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 6. API PERFORMANCE
# ============================================================

api_rows = []

for filename in glob.glob(
    f"{RAW}/api-*.txt"
):

    text = open(filename, errors="ignore").read()

    request_match = re.search(
        r"Requests per second:\s*([\d.]+)",
        text
    )

    latency_match = re.search(
        r"Time per request:\s*([\d.]+)",
        text
    )

    failed_match = re.search(
        r"Failed requests:\s*(\d+)",
        text
    )

    if request_match:

        name = os.path.basename(filename)

        api_rows.append({
            "test": name,
            "requests_per_sec":
                float(request_match.group(1)),
            "time_per_request_ms":
                float(latency_match.group(1))
                if latency_match else None,
            "failed_requests":
                int(failed_match.group(1))
                if failed_match else None
        })

api_df = pd.DataFrame(api_rows)

if not api_df.empty:

    api_df.to_csv(
        f"{PROCESSED}/api_results.csv",
        index=False
    )

    plt.figure()

    plt.bar(
        api_df["test"],
        api_df["requests_per_sec"]
    )

    plt.title("FastAPI Requests per Second")
    plt.xlabel("Test")
    plt.ylabel("Requests/sec")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(
        f"{FIGURES}/api_requests_per_second.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 7. FINAL PERFORMANCE DIFFERENCE
# ============================================================

print("\n========================================")
print("ANALYSIS COMPLETE")
print("========================================")

if not cpu_df.empty:

    print("\nCPU Statistics:")
    print(
        cpu_df.groupby("environment")[
            "events_per_second"
        ].agg(
            ["mean", "median", "min", "max", "std"]
        )
    )

if not memory_df.empty:

    print("\nMemory Statistics:")
    print(
        memory_df.groupby("environment")[
            "MiB_per_sec"
        ].agg(
            ["mean", "median", "min", "max", "std"]
        )
    )

if not network_df.empty:

    print("\nNetwork:")
    print(network_df)

if not api_df.empty:

    print("\nAPI:")
    print(api_df)

print("\nGenerated files:")
print(f"Processed data → {PROCESSED}/")
print(f"Graphs → {FIGURES}/")
