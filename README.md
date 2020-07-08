# gpu_monitor
Minimal version of a gpu monitor for the deep-gpu-* machines.

Uses paramiko to ssh into machines and pynvml/py3nvml to get gpu info.

Updates `/afs/csail.mit.edu/u/k/krisgrg/public_html/cluster.html` which is
served on

https://people.csail.mit.edu/krisgrg/cluster.html


color.js sits in afs as well, duplicated here for versioning. 

conda create --name <env> --file requirements.txt 
and then pip install-ing pynvml and py3nvml

should give a working setup
