import sys

def print_arr(arr, sizei, sizej):
    for i in range(0, sizei):
        for j in range(0, sizej):
            print("%11s" % arr[i][j], end="\t")
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
            new_arr[idx] = 1
        else:
            new_arr[idx] = 0
    return new_arr

#def minimization(dka_arr, states_arr, acc_states_arr):
#    states_set = []
#    for 


def main():
    states_arr = input("").split(',')
    symbols_arr = input("").split(',')
    acc_states_arr = input("").split(',')
    init_state = input("")

    dka_arr = parse_transitions(states_arr, symbols_arr)

    print_arr(dka_arr, len(states_arr), len(symbols_arr))

#    minimization(dka_arr, states_arr, parse_acc_states(states_arr, acc_states_arr))

    

if __name__ == "__main__":
    main()