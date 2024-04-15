import sys

def print_arr(arr, sizei, sizej):
    for i in range(0, sizei):
        for j in range(0, sizej):
            print("%3s" % arr[i][j], end="\t")
        print()

def parse_transitions(states_arr, symbols_arr):
    dka_arr = [[0 for i in range(len(symbols_arr))] for j in range(len(states_arr))]
    for line in sys.stdin:
        temp = line[:-1].split("->")
        curr = temp[0].split(",")
        nxt = temp[1]
        dka_arr[states_arr.index(curr[0])][symbols_arr.index(curr[1])] = states_arr.index(nxt)
    return dka_arr

def parse_acc_states(states_arr, acc_states_arr):
    new_arr = []
    for idx, state in enumerate(states_arr):
        if state in acc_states_arr:
            new_arr.insert(idx, 1)
        else:
            new_arr.insert(idx, 0)
    return new_arr

def dfs(visited, graph, node):
    if node not in visited:
        visited.add(node)
        for el in graph[node]:
            dfs(visited, graph, el)

def remove_unreachable(dka_arr, states_arr, acc_states_arr, init_state):
    visited = set()
    dfs(visited, dka_arr, init_state)
    new_dka_arr = []
    new_states_arr = []
    new_acc_states_arr = []
    for i in range(len(states_arr)):
        if i in visited:
            new_dka_arr.append(dka_arr[i])
            new_states_arr.append(states_arr[i])
            new_acc_states_arr.append(acc_states_arr[i])
    return new_dka_arr.copy(), new_states_arr.copy(), new_acc_states_arr.copy()

def marked_pair(dka_arr, triag_arr, i, j):
    for a in range(0, len(dka_arr[0])):
        if dka_arr[i][a] < dka_arr[j][a]:
            i, j = j, i
        if triag_arr[dka_arr[i][a]][dka_arr[j][a]] > 0:
            return True
    return False

def get_unt(same_states):
    arr1 = []
    arr2 = []
    for el in same_states:
        arr1.append(el[0])
        arr2.append(el[1])
    return arr1, arr2

def minimization(dka_arr, states_arr, symbols_arr, acc_states):
    triag_arr = [[-1 for i in range(len(states_arr))] for j in range(len(states_arr))]
    transitions_dict = {}
    for i in range(1, len(states_arr)):
        for j in range(0, i):
            triag_arr[i][j] = 0
    for i in range(1, len(states_arr)):
        for j in range(0, i):
            if acc_states[i] == 1 and acc_states[j] != 1:
                triag_arr[i][j] = 1
    for i in range(1, len(states_arr)):
        for j in range(0, i):
            if triag_arr[i][j] == 1:
                continue
            if marked_pair(dka_arr, triag_arr, i, j) == True:
                triag_arr[i][j] = 1
                if transitions_dict.get(str(i) + str(j)) != None:
                    for el in transitions_dict[str(i) + str(j)]:
                        triag_arr[el[0]][el[1]]
            else:
                for a in range(0, len(dka_arr[0])):
                    if dka_arr[i][a] != dka_arr[j][a]:
                        if transitions_dict.get(str(dka_arr[i][a]) + str(dka_arr[j][a])) != None:
                            transitions_dict[str(dka_arr[i][a]) + str(dka_arr[j][a])].append([i, j])
                        else:
                            transitions_dict[str(dka_arr[i][a]) + str(dka_arr[j][a])] = [[i, j]]
    same_states = []
    for i in range(1, len(states_arr)):
        for j in range(0, i):
            if triag_arr[i][j] == 0:
                same_states.append([i, j])

    new_dka = []
    new_states = []
    new_acc_states = []

    erase_states, merge_states = get_unt(same_states)

    idx = 0
    tmp = []
    while idx < len(states_arr):
        if idx not in erase_states:
            new_dka.append(dka_arr[idx])
            new_states.append(states_arr[idx])
            new_acc_states.append(acc_states[idx])
        else:
            if idx != len(states_arr) - 1:
                for i in range(len(symbols_arr)):
                    tmp.append(-1)
                new_dka.append(tmp.copy())
                tmp.clear()
                new_states.append(-1)
                new_acc_states.append(-1)
        idx += 1
    
    for state_el in same_states:
        for i in range(len(new_dka)):
            for j in range(len(symbols_arr)):
                if new_dka[i][j] == state_el[0]:
                    new_dka[i][j] = state_el[1]

    return new_dka.copy(), new_states.copy(), new_acc_states.copy()

def deparse(dka_arr, states_arr, symbols_arr, acc_st_arr, init_state):
    if len(states_arr) > 1:
        for idx, el in enumerate(states_arr):
            if el == -1:
                continue
            if idx == len(states_arr) - 1:
                print(el)
            else:
                print(el, end=",")
    else:
        print(states_arr[0])
    for idx, el in enumerate(symbols_arr):
        if el == -1:
            continue
        if idx == len(symbols_arr) - 1:
            print(el)
        else:
            print(el, end=",")
    if len(acc_st_arr) > 0:
        for idx, el in enumerate(states_arr):
            if el == -1:
                continue
            if acc_st_arr[idx] == 1:
                if idx == len(states_arr) - 1:
                    print(el)
                else:
                    print(el, end=",")
    else:
        print("")
    print(init_state)
    for i in range(len(states_arr)):
        for j in range(len(symbols_arr)):
            if dka_arr[i][j] == -1:
                break
            print("{},{}->{}".format(states_arr[i], symbols_arr[j], states_arr[dka_arr[i][j]]))


def main():
    states_arr = input("").split(',')
    symbols_arr = input("").split(',')
    acc_states_arr = input("").split(',')
    init_state = input("")
    dka_arr = parse_transitions(states_arr, symbols_arr)
    init_state_idx = states_arr.index(init_state)

    #print_arr(dka_arr, len(states_arr), len(symbols_arr))
    if (len(acc_states_arr) != 1 and acc_states_arr[0] != '') and len(acc_states_arr) < len(states_arr):
        dka_tr_arr, states_tr_arr, acc_states_parsed_tr_arr = remove_unreachable(dka_arr, states_arr, parse_acc_states(states_arr, acc_states_arr), init_state_idx)
        new_dka, new_states_arr, new_acc_st_arr = minimization(dka_tr_arr, states_tr_arr, symbols_arr, acc_states_parsed_tr_arr)
    else:
        new_states_arr = [init_state]
        new_dka = [[0 for i in range(len(symbols_arr))] for j in range(1)]
        if len(acc_states_arr) == len(states_arr):
            new_acc_st_arr = [1]
        else:
            new_acc_st_arr = []
    #print_arr(new_dka, len(new_states_arr), len(symbols_arr))

    deparse(new_dka, new_states_arr, symbols_arr, new_acc_st_arr, init_state)

    #print_arr(new_dka, len(new_states_arr), len(symbols_arr))
    #print(new_states_arr)
    #print(new_acc_st_arr)
    #print(symbols_arr)

if __name__ == "__main__":
    main()