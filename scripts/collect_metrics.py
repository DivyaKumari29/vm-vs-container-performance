import platform
import psutil
from datetime import datetime

print("========================================")
print("SYSTEM METRICS")
print("========================================")

print("Timestamp:", datetime.now())
print("System:", platform.system())
print("Release:", platform.release())
print("CPU cores:", psutil.cpu_count())
print("Memory GB:", round(psutil.virtual_memory().total / (1024**3), 2))

print("========================================")
