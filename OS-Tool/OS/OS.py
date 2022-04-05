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
    sorted(processes, key=lambda x: (x["arrival_time"], x["id"]))
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
    sorted(processes, key=lambda x: (x["arrival_time"], x["id"]))
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
    sorted(processes, key=lambda x: (x["arrival_time"], x["id"]))
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
    sorted(processes, key=lambda x: (x["arrival_time"], x["id"]))
    time_intervals = []
    zero_process = 0

    timer = 0
    countdown = 0
    start = 0
    token = 0
    isHold = False

    while zero_process < len(processes):
        # time.sleep(1.0)
        if isHold:
            if processes[token]["burst"] == 0:
                time_intervals.append({
                    "start": start,
                    "end": timer - 1,
                    "id": processes[token]["id"]
                })

                token = token + 1
                if token == len(processes):
                    token = 0
                zero_process = zero_process + 1
                isHold = False

            elif countdown == 0:
                time_intervals.append({
                    "start": start,
                    "end": timer - 1,
                    "id": processes[token]["id"]
                })

                token = token + 1
                if token == len(processes):
                    token = 0
                isHold = False

            else:
                timer = timer + 1
                countdown = countdown - 1
                processes[token]["burst"] = processes[token]["burst"] - 1

                continue

        isOK = False
        for process in processes:
            if process["arrival_time"] <= timer and process["burst"] > 0:
                isOK = True
                break
        if not isOK:
            timer = timer + 1
            continue

        while True:
            if token >= len(processes):
                token = 0

            if processes[token]["arrival_time"] > timer or processes[token]["burst"] == 0:
                token = token + 1
                continue
            countdown = quantum
            start = timer
            isHold = True
            break

    logToConsole(time_intervals)
    evaluateMetric(time_intervals, processes)