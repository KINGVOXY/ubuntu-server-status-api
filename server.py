import os
import json
import subprocess

import uvicorn
from fastapi import FastAPI

import psutil


'''
鯖の状況を返すAPI
url: localhost:8200/api/server/status
'''


app = FastAPI()


# sadfコマンドで情報をjsonで持ってくる
def get_sadf_data():
    text = subprocess.getoutput("sadf -T -j -- -b -n DEV")
    data = json.loads(text)
    info = data["sysstat"]["hosts"][0]
    statistics = info["statistics"]
    new_stats = statistics[len(statistics)-1]
    io = new_stats["io"]

    sysname =       info["sysname"]
    release =       info["release"]
    machine =       info["machine"]
    num_of_cpus =   str(info["number-of-cpus"])
    io_reads =      io["io-reads"]
    io_writes =     io["io-writes"]
    ifaces =        new_stats["network"]["net-dev"]
    return sysname, release, machine, num_of_cpus, io_reads, io_writes, ifaces


# interfaceの情報組み合わせてjson配列で返す
def get_ifaces_data(network, ifaces):
    results = []
    try:
        for iface in ifaces:
            nic_name = iface["iface"]
            result = {
                "name":         nic_name,
                "bytesSent":    str(network[nic_name][0]),
                "bytesRecv":    str(network[nic_name][1]),
                "packetsSent":  str(network[nic_name][2]),
                "packetsRecv":  str(network[nic_name][3]),
                "rxkb":         str(iface["rxkB"]),
                "txkb":         str(iface["txkB"])
            }
            results.append(result)
            
    except Exception as e:
        print(e)

    return results


@app.get('/api/server/status')
async def get_status():
    loadavg1    = str(os.getloadavg()[0])
    loadavg5    = str(os.getloadavg()[1])
    loadavg15   = str(os.getloadavg()[2])
    cpu_percent =       str(psutil.cpu_percent(interval=1))
    cpu_temperature =   str(psutil.sensors_temperatures()['coretemp'][0][2])
    memory_percent =    str(psutil.virtual_memory().percent)
    disk_usage =        str(psutil.disk_usage('/').percent)
    swap_free =         str(psutil.swap_memory().free)
    network =           psutil.net_io_counters(pernic=True)
    sysname, release, machine, num_of_cpus, io_reads, io_writes, ifaces = get_sadf_data()
    interfaces = get_ifaces_data(network, ifaces)
    io_reads = dict([i, str(v)] for i, v in io_reads.items())
    io_writes = dict([i, str(v)] for i, v in io_writes.items())


    
    return {
        "sysname":          sysname,
        "release":          release,
        "machine":          machine,
        "numOfCpus":        num_of_cpus,
        "ioReads":          io_reads,
        "ioWrites":         io_writes,
        "loadavg1":         loadavg1,
        "loadavg5":         loadavg5,
        "loadavg15":        loadavg15,
        "cpuPercent":       cpu_percent,
        "cpuTemperature":   cpu_temperature,
        "memoryPercent":    memory_percent,
        "swapFree":         swap_free,
        "diskPercent":      disk_usage,
        "interfaces":       interfaces
    }


if __name__ == "__main__":
    uvicorn.run("server:app", port=8200)
