import time

global isOK


def evaluateMetric(time_intervals, processes):
    num_process = len(processes)
    print("Throughput\t", num_process / (time_intervals[-1]["end"] + 1))
    print("-----------------------------------------------------------")

    print("Turnaround time")
    total_turnaround = 0
    for process in processes:
        last = 0
        for interval in time_intervals:
            if process["id"] == interval["id"]:
                last = interval["end"]
        print("P{}\t{}".format(process["id"] + 1, last - process["arrival_time"] + 1))
        total_turnaround = total_turnaround + last - process["arrival_time"] + 1
    print("Average\t", total_turnaround / num_process)
    print("-----------------------------------------------------------")

    print("Waiting time")
    total_waiting = 0
    for process in processes:
        last = process["arrival_time"]
        current_waiting = 0

        for interval in time_intervals:
            if process["id"] == interval["id"]:
                total_waiting = total_waiting + interval["start"] - last
                current_waiting = current_waiting + interval["start"] - last
                last = interval["end"] + 1

        print("P{}\t{}".format(process["id"] + 1, current_waiting))
    print("Average\t", total_waiting / num_process)
    print("-----------------------------------------------------------")

    print("Response time")
    total_response = 0
    for process in processes:
        last = process["arrival_time"]
        current_response = 0

        for interval in time_intervals:
            if process["id"] == interval["id"]:
                total_response = total_response + interval["start"] - last
                current_response = current_response + interval["start"] - last
                break

        print("P{}\t{}".format(process["id"] + 1, current_response))
    print("Average\t", total_response / num_process)
    print("-----------------------------------------------------------")

def logToConsole(time_intervals):
    print("Process by order\t", end="")
    for interval in time_intervals:
        print("P{}".format(interval["id"] + 1), end="\t")
    print()

    print("Start time\t", end="")
    for interval in time_intervals:
        print("{}".format(interval["start"]), end="\t")
    print()

    print("End time\t", end="")
    for interval in time_intervals:
        print("{}".format(interval["end"]), end="\t")
    print()


def FCFS(processes):
    processes = sorted(processes, key=lambda x: (x["arrival_time"], x["id"]))

    time_intervals = []
    start = 0
    timer = 0
    token = 0

    while token < len(processes):
        if processes[token]["arrival_time"] > timer:
            start = processes[token]["arrival_time"]
            timer = start + 1
            processes[token]["burst"] = processes[token]["burst"] - 1
            continue
        elif processes[token]["burst"] == 0:
            time_intervals.append({
                "start": start,
                "end": timer - 1,
                "id": processes[token]["id"]
            })
            start = timer
            token = token + 1
            continue
        timer = timer + 1
        processes[token]["burst"] = processes[token]["burst"] - 1

    logToConsole(time_intervals)
    evaluateMetric(time_intervals, processes)


def NonPremSTF(processes):
    processes = sorted(processes, key=lambda x: (x["arrival_time"], x["id"]))
    time_intervals = []
    start = 0
    timer = 0
    token = -1
    zero_count = 0

    while zero_count < len(processes):
        # print(token, timer)
        # if token != -1:
        #     print(processes[token]["burst"])

        if token != -1 and processes[token]["burst"] == 0:
            # print("hello check")
            zero_count = zero_count + 1
            time_intervals.append({
                "start": start,
                "end": timer - 1,
                "id": processes[token]["id"]
            })
            token = -1

        if token == -1:
            for i, process in enumerate(processes):
                if process["arrival_time"] <= timer and process["burst"] > 0:
                    if token != -1:
                        if process["burst"] < processes[token]["burst"]:
                            if start != timer:
                                time_intervals.append({
                                    "start": start,
                                    "end": timer - 1,
                                    "id": processes[token]["id"]
                                })
                            token = i
                            start = timer

                    else:
                        if process["burst"] > 0:
                            token = i
                            start = timer

        # time.sleep(1.0)

        timer = timer + 1
        if token != -1:
            processes[token]["burst"] = processes[token]["burst"] - 1

    logToConsole(time_intervals)
    evaluateMetric(time_intervals, processes)


def SRTF(processes):
    processes = sorted(processes, key=lambda x: (x["arrival_time"], x["id"]))
    time_intervals = []
    start = 0
    timer = 0
    token = -1
    zero_count = 0

    while zero_count < len(processes):
        # print(token, timer)
        # if token != -1:
        #     print(processes[token]["burst"])

        if token != -1 and processes[token]["burst"] == 0:
            # print("hello check")
            zero_count = zero_count + 1
            time_intervals.append({
                "start": start,
                "end": timer - 1,
                "id": processes[token]["id"]
            })
            token = -1

        for i, process in enumerate(processes):
            if process["arrival_time"] <= timer and process["burst"] > 0:
                if token != -1:
                    if process["burst"] < processes[token]["burst"]:
                        if start != timer:
                            time_intervals.append({
                                "start": start,
                                "end": timer - 1,
                                "id": processes[token]["id"]
                            })
                        token = i
                        start = timer

                else:
                    if process["burst"] > 0:
                        token = i
                        start = timer

        # time.sleep(1.0)

        timer = timer + 1
        if token != -1:
            processes[token]["burst"] = processes[token]["burst"] - 1

    logToConsole(time_intervals)
    evaluateMetric(time_intervals, processes)


def RR(processes, quantum):
    processes = sorted(processes, key=lambda x: (x["arrival_time"], x["id"]))
    time_intervals = []
    zero_process = 0

    timer = 0
    countdown = 0
    start = 0
    isHold = False
    index_queue = []

    while zero_process < len(processes):
        for i in range(len(processes)):
            if i not in index_queue:
                if processes[i]["burst"] == 0 or processes[i]["arrival_time"] > timer:
                    continue
                index_queue.append(i)

        if not isHold:
            # find next candidate
            while len(index_queue) > 0 and processes[index_queue[0]]["burst"] == 0:
                index_queue.pop()

            if len(index_queue) == 0:
                timer = timer + 1
                continue

            start = timer
            countdown = quantum
            isHold = True
        else:
            if processes[index_queue[0]]["burst"] == 0:
                time_intervals.append({
                    "start": start,
                    "end": timer - 1,
                    "id": processes[index_queue[0]]["id"]
                })
                index_queue.pop(0)
                isHold = False
                zero_process = zero_process + 1

            elif countdown == 0:
                time_intervals.append({
                    "start": start,
                    "end": timer - 1,
                    "id": processes[index_queue[0]]["id"]
                })
                token = index_queue[0]
                index_queue.pop(0)
                index_queue.append(token)
                isHold = False
            else:
                processes[index_queue[0]]["burst"] = processes[index_queue[0]]["burst"] - 1
                countdown = countdown - 1
                timer = timer + 1

    logToConsole(time_intervals)
    evaluateMetric(time_intervals, processes)