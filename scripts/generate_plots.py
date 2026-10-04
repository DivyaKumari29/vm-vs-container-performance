import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/processed/cpu_results.csv")

# Average CPU performance
summary = df.groupby("environment")["events_per_second"].mean()

plt.figure()
summary.plot(kind="bar")
plt.title("Average CPU Performance: VM vs Container")
plt.xlabel("Environment")
plt.ylabel("Events per Second")
plt.tight_layout()
plt.savefig("results/figures/cpu_performance.png", dpi=300)
plt.close()

# CPU scalability
scalability = df.groupby(
    ["environment", "threads"]
)["events_per_second"].mean().reset_index()

plt.figure()

for environment in scalability["environment"].unique():
    data = scalability[scalability["environment"] == environment]
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
plt.savefig("results/figures/cpu_scalability.png", dpi=300)
plt.close()

print("Graphs generated successfully!")

