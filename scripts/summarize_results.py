import glob
import re
import os

print("=" * 60)
print("VM vs CONTAINER PERFORMANCE SUMMARY")
print("=" * 60)

# ---------------- CPU ----------------
print("\nCPU PERFORMANCE")

for env in ["vm", "container"]:
    values = []

    for f in glob.glob(f"results/raw/cpu/{env}/run*.txt"):
        text = open(f).read()
        m = re.search(r"events per second:\s*([\d.]+)", text)
        if m:
            values.append(float(m.group(1)))

    if values:
        print(
            f"{env.upper():10} "
            f"Mean={sum(values)/len(values):.2f} "
            f"Min={min(values):.2f} "
            f"Max={max(values):.2f}"
        )

# ---------------- MEMORY ----------------
print("\nMEMORY PERFORMANCE")

for env in ["vm", "container"]:
    values = []

    for f in glob.glob(f"results/raw/memory/{env}/run*.txt"):
        text = open(f).read()

        # sysbench memory reports MiB/sec
        matches = re.findall(r"([\d.]+)\s+MiB/sec", text)

        if matches:
            values.append(float(matches[-1]))

    if values:
        print(
            f"{env.upper():10} "
            f"Mean={sum(values)/len(values):.2f} MiB/sec "
            f"Min={min(values):.2f} "
            f"Max={max(values):.2f}"
        )

# ---------------- DISK ----------------
print("\nDISK PERFORMANCE")

for env in ["vm", "container"]:
    for workload in ["seq-read", "seq-write", "random-read", "random-write"]:

        filename = f"results/raw/disk/{env}/{workload}.txt"

        if not os.path.exists(filename):
            continue

        text = open(filename).read()

        # fio bandwidth
        matches = re.findall(r"bw=([\d.]+)([KMG]iB/s)", text)

        if matches:
            print(f"{env.upper():10} {workload:15} {matches[0][0]} {matches[0][1]}")

# ---------------- NETWORK ----------------
print("\nNETWORK PERFORMANCE")

for env, filename in [
    ("VM", "results/raw/network-vm.txt"),
    ("Container", "results/raw/network-container.txt")
]:

    if os.path.exists(filename):
        text = open(filename).read()

        matches = re.findall(r"([\d.]+)\s+([KMG]bits/sec)", text)

        if matches:
            value = matches[-1]
            print(f"{env:10} {value[0]} {value[1]}")

# ---------------- API ----------------
print("\nAPI PERFORMANCE")

for filename in glob.glob("results/raw/api-*.txt"):

    text = open(filename).read()

    req = re.search(r"Requests per second:\s*([\d.]+)", text)
    latency = re.search(r"Time per request:\s*([\d.]+)", text)

    print(os.path.basename(filename))

    if req:
        print(f"  Requests/sec = {req.group(1)}")

    if latency:
        print(f"  Time/request = {latency.group(1)} ms")

print("\n" + "=" * 60)
print("SUMMARY COMPLETE")
print("=" * 60)
