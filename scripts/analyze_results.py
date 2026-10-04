import pandas as pd

data = []

# VM CPU results
for i in range(1, 11):
    filename = f"results/raw/cpu/vm/run{i}.txt"

    with open(filename) as f:
        for line in f:
            if "events per second:" in line:
                value = float(line.split(":")[1].strip())
                data.append(["VM", 4, i, value])
                break

# Container CPU results
for i in range(1, 11):
    filename = f"results/raw/cpu/container/run{i}.txt"

    with open(filename) as f:
        for line in f:
            if "events per second:" in line:
                value = float(line.split(":")[1].strip())
                data.append(["Container", 4, i, value])
                break

df = pd.DataFrame(
    data,
    columns=["environment", "threads", "run", "events_per_second"]
)

df.to_csv(
    "results/processed/cpu_results.csv",
    index=False
)

print("\nCPU Results:")
print(df)

print("\nStatistics:")
print(
    df.groupby("environment")["events_per_second"]
      .agg(["mean", "median", "min", "max", "std"])
)
