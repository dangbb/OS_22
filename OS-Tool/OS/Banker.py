import numpy as np


def print_matrix(matrix, n_process, n_resource):
    print(end="\t")
    for i in range(n_resource):
        print("R{}".format(i), end="\t")
    print("")

    for i in range(n_process):
        print("P{}".format(i), end="\t")
        for j in range(n_resource):
            print(matrix[i][j], end="\t")
        print()


def banker(n_process, n_resource, cmax, allocation, available):
    need = cmax - allocation

    assert allocation.shape == (n_process, n_resource), "Allocation shape unmatch, {} and {}".format(allocation.shape, (n_process, n_resource))
    assert available.shape == (n_resource,), "Resource shape unmatch, {} and {}".format(available.shape, n_resource)
    assert cmax.shape == (n_process, n_resource), "Cmax shape unmatch, {} and {}".format(cmax.shape, (n_process, n_resource))

    if n_resource == 1:
        print("Max:\t", cmax.squeeze().tolist())
        print("Allocation:\t", allocation.squeeze().tolist())
        print("Available:\t", available.tolist())
        print("Need:\t", need.squeeze().tolist())
    else:
        print("Max:")
        print_matrix(cmax, n_process, n_resource)
        print("Allocation:")
        print_matrix(allocation, n_process, n_resource)
        print("Available:\n", available)
        print("Need:")
        print_matrix(need, n_process, n_resource)

    # Step 1: Assign variable to work
    work = available.copy()
    finish = np.zeros(n_process, dtype=np.bool)

    print("1. Work = Available = {}, Finish = {}".format(work.tolist(), finish.tolist()))

    while True:
        # Step 2: Find i
        chosen = -1
        for i in range(n_process):
            if finish[i]:
                continue
            current = i
            for j in range(n_resource):
                if need[i][j] > work[j]:
                    current = -1
                    break
            if current == i:
                chosen = i
                break

        if chosen != -1:
            print("2. i = {}".format(chosen))

            # Step 3: Calc new work, update finish
            work = work + allocation[chosen]
            finish[chosen] = True
            print("3. Work = Work + Allocation[{}] = {}, Finish = {}".format(chosen, work.tolist(), finish.tolist()))
        else:
            print("2. Can't find i. Go to 4.")
            unfinish = []
            for i in range(n_process):
                if not finish[i]:
                    unfinish.append(i)

            if len(unfinish) == 0:
                print("4. All Finish[i] is true. The system is in safe state.")
                return True
            else:
                print("4. Process {} if not done. The system is in unsafe state.".format(unfinish))
                return False
            break


def check_granted(n_process, n_resource, cmax, allocation, available, pos, request):
    assert request.shape == (n_resource,), "Request shape not match, {} and {}".format(request.shape, (n_resource,))
    assert 0 <= pos < n_process, "Position out of range, {} for range [{},{}]".format(pos, 0, n_process - 1)

    allocation[pos] = allocation[pos] + request
    available = available - request

    if banker(n_process=n_process, n_resource=n_resource, cmax=cmax, allocation=allocation, available=available):
        print("This request can be granted")
        return True
    else:
        print("This request can't be granted")
        return False


def check_granted_2(n_process, n_resource, cmax, allocation, available, pos, request, pos2, request2):
    assert request.shape == (n_resource,), "Request shape not match, {} and {}".format(request.shape, (n_resource,))
    assert 0 <= pos < n_process, "Position out of range, {} for range [{},{}]".format(pos, 0, n_process - 1)

    allocation[pos] = allocation[pos] + request
    available = available - request

    if banker(n_process=n_process, n_resource=n_resource, cmax=cmax, allocation=allocation, available=available):

        if check_granted(n_process, n_resource, cmax, allocation, available, pos2, request2):
            print("Both requests can be granted")
        else:
            print("Both request can't be granted")
    else:
        print("Both request can't be granted")


def check_deadlock(n_process, n_resource, allocation, request, available):

    assert allocation.shape == (n_process, n_resource), "Allocation shape unmatch, {} and {}".format(allocation.shape, (n_process, n_resource))
    assert available.shape == (n_resource,), "Resource shape unmatch, {} and {}".format(available.shape, n_resource)
    assert request.shape == (n_process, n_resource), "Request shape unmatch, {} and {}".format(request.shape, (n_process, n_resource))

    if n_resource == 1:
        print("Allocation:\t", allocation.squeeze().tolist())
        print("Available:\t", available.tolist())
        print("Request:\t", request.tolist())
    else:
        print("Allocation:")
        print_matrix(allocation, n_process, n_resource)
        print("Available:\n", available)
        print("Request:")
        print_matrix(request, n_process, n_resource)

    # Step 1: Assign variable to work
    work = available.copy()
    finish = np.zeros(n_process, dtype=np.bool)

    print("1. Work = Available = {}, Finish = {}".format(work.tolist(), finish.tolist()))

    while True:
        # Step 2: Find i
        chosen = -1
        for i in range(n_process):
            if finish[i]:
                continue
            current = i
            for j in range(n_resource):
                if request[i][j] > work[j]:
                    current = -1
                    break
            if current == i:
                chosen = i
                break

        if chosen != -1:
            print("2. i = {}".format(chosen))

            # Step 3: Calc new work, update finish
            work = work + allocation[chosen]
            finish[chosen] = True
            print("3. Work = Work + Allocation[{}] = {}, Finish = {}".format(chosen, work.tolist(), finish.tolist()))
        else:
            print("2. Can't find i. Go to 4.")
            unfinish = []
            for i in range(n_process):
                if not finish[i]:
                    unfinish.append(i)

            if len(unfinish) == 0:
                print("4. All Finish[i] is true. The system is in safe state.")
                return True
            else:
                print("4. Process {} if not done. The system is in unsafe state.".format(unfinish))
                return False
            break


def check_request_deadlock(n_process, n_resource, allocation, request, available, pos, add_request):
    assert 0 <= pos < n_process, "Position invalid, {} not in range [{}, {}]".format(pos, 0, n_process - 1)
    assert add_request.shape == (n_resource,), "Add request invalid shape, {} and {}".format(add_request.shape, (n_resource,))

    request[pos] = request[pos] + add_request

    if check_deadlock(n_process, n_resource, allocation, request, available):
        print("This request can be granted")
    else:
        print("This request can't be granted")



if __name__ == "__main__":
    path = "input_c4.txt"

    n_process = 5
    n_resource = 3
    cmax = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])
    allocation = np.array([
        [0, 1, 2],
        [2, 0, 0],
        [3, 0, 1],
        [2, 1, 1],
        [0, 0, 1]
    ])
    request = np.array([
        [1, 0, 0],
        [2, 0, 2],
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 2]
    ])
    available = np.array([
        3, 3, 2
    ])

    # banker(n_process=n_process, n_resource=n_resource, cmax=cmax, allocation=allocation, available=available)

    # check_granted(n_process=n_process, n_resource=n_resource, cmax=cmax, allocation=allocation, available=available, pos=4, request=np.array([1, 0, 0], dtype=np.int))

    check_granted_2(n_process=n_process, n_resource=n_resource, cmax=cmax, allocation=allocation, available=available, pos=1, request=np.array([1, 0, 2], dtype=np.int), pos2=0, request2=np.array([0, 2, 0], dtype=np.int))


    # check_deadlock(n_process=5, n_resource=3, allocation=allocation, request=request, available=available)
    # check_request_deadlock(n_process=n_process, n_resource=n_resource, allocation=allocation, request=request, available=available, pos=2, add_request=np.array([0, 0, 1], dtype=np.int))