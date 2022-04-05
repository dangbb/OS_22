from OS.OS import *
from IO.IO import *

if __name__ == "__main__":
    input_path = "input.txt"

    inp = []

    with open(input_path, "r") as f:
        n_inp = read_line(f)[0]
        for i in range(n_inp):
            inp.append(read_line(f))
        method = f.readline()
        quantum = 12

        if method == "RR\n":
            quantum = read_line(f)[0]

    processes = []

    for i, val in enumerate(inp):
        arr = val[0]
        dur = val[1]
        processes.append({
            "id": i,
            "burst": dur,
            "arrival_time": arr
        })

    if method == "FCFS":
        FCFS(processes)
    elif method == "NonPremSTF":
        NonPremSTF(processes)
    elif method == "SRTF":
        SRTF(processes)
    elif method == "RR\n":
        RR(processes, quantum)
