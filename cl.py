from pynvml import *
from py3nvml import *
import psutil

nvmlInit()
device_count = nvmlDeviceGetCount()

free_gpus = ", ".join([str(i) for (i, b) in enumerate(get_free_gpus()) if b])
gpu_util = []
for i in range(device_count):
    handle = nvmlDeviceGetHandleByIndex(i)
    mem_info = nvmlDeviceGetMemoryInfo(handle)
    gpu_util.append(nvmlDeviceGetUtilizationRates(handle).gpu)

gpu_util = ", ".join([str(util) for util in gpu_util])

print(f"{device_count};{free_gpus};{round(mem_info.used / mem_info.total * 100, 2)};{gpu_util};{psutil.cpu_percent()};")
