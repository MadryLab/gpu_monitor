# GPU Monitor
Minimal version of a gpu monitor for the deep-gpu-* machines.

Uses the tool from 
https://github.com/rossumai/nvgpu
with an additional column for memory usage, added as in [this PR](https://github.com/rossumai/nvgpu/pull/16)

Updates `/data/theory/robustopt/gpu_monitor/gpu_monitor.html` which is served on https://people.csail.mit.edu/krisgrg/gpu_monitor.html

# To run
On each machine run `FLASK_APP=nvgpu.webapp nohup flask run --host 0.0.0.0 --port 1080 >> flask-deep-gpu-<n>.log 2>&1 &`
from `/data/theory/robustopt/gpu_monitor/flask_logs`

Then run `nohup python nvgpu_combine.py >> flask_logs/flask-master.log 2>&1 &` from `/data/theory/robustopt/gpu_monitor/` (the original combination using flask from the repo didn't work for me, hence this combine script)

