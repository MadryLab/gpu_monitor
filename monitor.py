from pynvml import *
from py3nvml import *
import pandas as pd
import numpy as np
import paramiko
import psutil
import time
from datetime import datetime
from multiprocessing import Pool


def populate_df(client, machine): 
    i = int(machine.split('-')[-1])
    flag_done = False 
    _, stdout, stderr = client.exec_command('source /data/theory/robustopt/krisgrg/.zshrc \n conda activate rob \n python3 /data/theory/robustopt/gpu_monitor/cl.py')
    for _ in range(20):
        time.sleep(1)
        if stdout.channel.eof_received:
            stdout.channel.close()
            z = stdout.readline()
            device_count, free_gpus, mem_used, gpu_util, cpu_util, __ = z.split(';')

            df.at[i, 'node'] = machine
            z = [float(util) for (i, util) in enumerate(gpu_util.split(', '))]
            df.at[i, 'GPU utilization (only taken)'] = str(np.mean(z)) + '%'
            df.at[i, 'CPU utilization'] = str(cpu_util) + '%'
            df.at[i, 'Memory Utilization'] = mem_used + '%'
            df.at[i, 'Free GPUs'] = free_gpus
            num_free_gpus = len(free_gpus.split(', ')) if free_gpus != '' else 0
            df.at[i, 'GPUs used'] = str(int(device_count) - num_free_gpus) + '/' + device_count

            flag_done = True
            break

    if not flag_done:
        df.at[i, 'node'] = machine
        df.at[i, ''] = 'UNREACHABLE'
        df.at[i, 'GPU utilization (only taken)'] = ''
        df.at[i, 'CPU utilization'] = ''
        df.at[i, 'Memory Utilization'] = ''
        df.at[i, 'Free GPUs'] = ''
        df.at[i, 'GPUs used'] = ''
    else:
        df.at[i, ''] = ''

    return df
        
if __name__ == '__main__':
    with open('/data/theory/robustopt/krisgrg/pass.txt', 'r') as fp:
        pswd = fp.read().rstrip()

    nvmlInit()
    df = pd.DataFrame(columns=['node', 'GPUs used' , 'Free GPUs', 'Memory Utilization', 'GPU utilization (only taken)', 'CPU utilization', ''])

    list_machines = ['deep-gpu-1', 'deep-gpu-2', 'deep-gpu-3', 'deep-gpu-4', 'deep-gpu-5', 'deep-gpu-6', 'deep-gpu-7', 'deep-gpu-8', 'deep-gpu-9', 'deep-gpu-10']
    ssh_clients = []
    for machine in list_machines:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=machine,username='krisgrg', password=pswd)
        ssh_clients.append(ssh_client)
    
    while True:
        # unfortunately, ssh_clients are not pickle-able, so multiprocessing can't be used, unless we establish the ssh connection inside every time
        # with Pool(processes=len(list_machines)) as p:
        #     dfs  = p.starmap(populate_df, [(client, list_machines[i]) for (i, client) in enumerate(ssh_clients)])

        for (i, ssh_client) in enumerate(ssh_clients):
            try:
                populate_df(ssh_client, list_machines[i])
            except:
                print('timeout')
                ssh_clients = []
                for machine in list_machines:
                    ssh_client = paramiko.SSHClient()
                    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh_client.connect(hostname=machine,username='krisgrg', password=pswd)
                    ssh_clients.append(ssh_client)
        
        html_table = df.to_html(index=False)

        # making the table look nicer
        html_table = html_table.replace("<tr>", "<tr class='mdc-data-table__row'>") # kinda jank
        html_table = html_table.replace("<th>", "<th class='mdc-data-table__header-cell' role='columnheader' scope='col'>")
        html_table = html_table.replace("<tbody>", "<tbody class='mdc-data-table__content'>")
        html_table = html_table.replace("<td>", "<td class='mdc-data-table__cell'>")
        html_table = html_table.replace("<tr style=\"text-align: right;\">", "<tr class='mdc-data-table__header-row'>")
        html_table = html_table.replace("<table border=\"1\" class=\"dataframe\">", "<table class='mdc-data-table__table'>")

        html_top = "<html>\
            <head>\
            <link href='https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css' rel='stylesheet'>\
            <script src='https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js'></script>\
            <link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'>\
            </head>\
            <meta http-equiv='refresh' content='60' />\
            <body>\
            <div class='mdc-data-table'>"

        html_str = html_top + html_table + f"</div> Last pulled\
        {datetime.now().__str__()} UTC  \
            <script src='color.js'></script>\
        </body>"
        with open('/data/theory/robustopt/gpu_monitor/cluster.html', 'w') as fp:
            fp.write(html_str)

