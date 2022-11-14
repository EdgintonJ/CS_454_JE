"""
Program: CS-454 Project 01
Author: Jordan Edginton
Description: This program will ask the user to select the problem they wish to perform and creates a DFA
to solve the problem. For problem one, we find the amount of strings where every 6 characters include the entire
language (a, b, c, d). For problem two, we find the shortest multiple  that only contains integers from the
language they determine.
"""

import sys


class DFA_P1:
    '''
    This is the DFA for the first problem. We have a defined language, but we will encode the string into base 4,
    where a = 4**i, b = 2*4**i, c = 3*4**i, and d = 4*4**i.
    '''

    language = ["a", "b", "c", "d"]
    states = []                                         # our encoded states
    states_label = []                                   # our states in string form
    i = 0

    # the string encoded here is the maximum possible that could be successful: dddcb
    # so we only need that many states
    while i <= 4**6 + 4**5 + 4**4 + 3 * 4**2 + 2 * 4:
        states.append(i)
        i += 4

    def __init__(self):
        # when we initialize the DFA, we create our accepting states, as well as populate our string labels
        self.accepting_states = []
        self.generate_accepting(self.accepting_states, 0, 1, 0, 0, 0, 0, 0, 0)
        self.states_label = self.generate_start_queue()

    def generate_accepting(self, arr, curr, lvl, a, b, c, d, dub, trip):
        # Here we recursively go through every string encoding and populate our accepting state array
        # with successful strings. To translate the variables, a-d represent the amount of each char, lvl is
        # the current position, and dub and trip are how many of each char is in the string currently.
        if lvl == 7:
            arr.append(curr)
            return

        if a == 0:
            self.generate_accepting(arr, curr + (1 * 4 ** lvl), lvl + 1, a + 1, b, c, d, dub, trip)
        elif a == 1 and dub < 2 and trip == 0:
            self.generate_accepting(arr, curr + (1 * 4 ** lvl), lvl + 1, a + 1, b, c, d, dub + 1, trip)
        elif a == 2 and dub == 1:
            self.generate_accepting(arr, curr + (1 * 4 ** lvl), lvl + 1, a + 1, b, c, d, 0, 1)

        if b == 0:
            self.generate_accepting(arr, curr + (2 * 4 ** lvl), lvl + 1, a, b + 1, c, d, dub, trip)
        elif b == 1 and dub < 2 and trip == 0:
            self.generate_accepting(arr, curr + (2 * 4 ** lvl), lvl + 1, a, b + 1, c, d, dub + 1, trip)
        elif b == 2 and dub == 1:
            self.generate_accepting(arr, curr + (2 * 4 ** lvl), lvl + 1, a, b + 1, c, d, 0, 1)

        if c == 0:
            self.generate_accepting(arr, curr + (3 * 4 ** lvl), lvl + 1, a, b, c + 1, d, dub, trip)
        elif c == 1 and dub < 2 and trip == 0:
            self.generate_accepting(arr, curr + (3 * 4 ** lvl), lvl + 1, a, b, c + 1, d, dub + 1, trip)
        elif c == 2 and dub == 1:
            self.generate_accepting(arr, curr + (3 * 4 ** lvl), lvl + 1, a, b, c + 1, d, 0, 1)

        if d == 0:
            self.generate_accepting(arr, curr + (4 * 4 ** lvl), lvl + 1, a, b, c, d + 1, dub, trip)
        elif d == 1 and dub < 2 and trip == 0:
            self.generate_accepting(arr, curr + (4 * 4 ** lvl), lvl + 1, a, b, c, d + 1, dub + 1, trip)
        elif d == 2 and dub == 1:
            self.generate_accepting(arr, curr + (4 * 4 ** lvl), lvl + 1, a, b, c, d + 1, 0, 1)

        return

    def generate_strings(self, n):
        # This is where we count the amount of possible strings of length n. We don't create and test
        # every string possible, instead we have an array prev which stores all possible strings that could be
        # possible at that iteration. We then check to see in any char added would put it in an accepting
        # state and if True, we add the prev amount to the new index in the nex array. After each iteration,
        # we replace the values in prev with the values in nex and continue until we reach n.
        total_strings = 0
        prev = []
        nex = []

        for t in range(len(self.states)):
            prev.append(0)
            nex.append(0)

        for u in range(335, len(self.states)):                  # We start the array at 335 since it's the smallest
            curr = self.states[u]                               # possible success, reducing operations.
            if curr + (4 ** 6) in self.accepting_states:
                temp = self.states_label[u][1:] + "a"           # this is where we initialize our prev with all
                idx = self.buffer(temp)                         # possible strings at n = 6. This is really the
                prev[idx] += 1                                  # amount of states prev[u] can tarnsfer to.
            if curr + (2 * 4 ** 6) in self.accepting_states:
                temp = self.states_label[u][1:] + "b"
                idx = self.buffer(temp)
                prev[idx] += 1
            if curr + (3 * 4 ** 6) in self.accepting_states:
                temp = self.states_label[u][1:] + "c"
                idx = self.buffer(temp)
                prev[idx] += 1
            if curr + (4 * 4 ** 6) in self.accepting_states:
                temp = self.states_label[u][1:] + "d"
                idx = self.buffer(temp)
                prev[idx] += 1

        for i in range(n - 6):
            for j in range(335, len(self.states)):              # After we have our state transfers in order, we can
                curr = self.states[j]                           # determine the total amount of strings.
                if curr + 4 ** 6 in self.accepting_states:
                    temp = self.states_label[j][1:] + "a"
                    idx = self.buffer(temp)
                    nex[idx] += prev[j]
                if curr + 2 * 4 ** 6 in self.accepting_states:
                    temp = self.states_label[j][1:] + "b"
                    idx = self.buffer(temp)
                    nex[idx] += prev[j]
                if curr + 3 * 4 ** 6 in self.accepting_states:
                    temp = self.states_label[j][1:] + "c"
                    idx = self.buffer(temp)
                    nex[idx] += prev[j]
                if curr + 4 * 4 ** 6 in self.accepting_states:
                    temp = self.states_label[j][1:] + "d"
                    idx = self.buffer(temp)
                    nex[idx] += prev[j]

            for r in range(335, len(nex)):                      # Here we swap prev with nex, and reset nex.
                x = nex[r]
                prev[r] = x
                nex[r] = 0

        for b in range(len(prev)):                              # This counts the total amount on strings from prev
            total_strings += prev[b]

        return total_strings

    def generate_start_queue(self):
        # This generates our starting queue, featuring all possible 5-char strings.
        arr = [""]
        for i in range(4**4 + 4**3 + 4**2 + 5):
            x = arr[i]
            arr.append(x + 'a')
            arr.append(x + 'b')
            arr.append(x + 'c')
            arr.append(x + 'd')
        return arr

    def conv(self, inp):
        # This converts a given char to their encoded number
        if inp == "a":
            return 1
        if inp == "b":
            return 2
        if inp == "c":
            return 3
        return 4

    def buffer(self, buf):
        # This takes the new string that is to become the buffer for the next iteration, encodes it,
        # and returns the index of the string.
        ret = 0
        for i in range(len(buf)):
            ret += self.conv(buf[-1 - i]) * 4 ** (i + 1)
        return int(ret / 4)


class DFA_P2:
    '''
        This is the DFA for the second problem. We have a user defined language and state amount. We use a BFS-style
        algorithm to determine the smallest multiple of a given number using the given language.
    '''

    def smallestMultiple(self, arr, k):
        # This is where we take our inputs from the user and determine the smallest multiple. We first initialize
        # the language and visited, parent, and label arrays. After that we initialize our first iteration
        # into the parent and lebel arrays, then use our delta function and BFS search to find the smallest multiple.
        found = False
        visited = []                            # visited array
        # language = self.set_language(arr)
        for w in range(k):
            visited.append(False)
        q = []                                  # queue
        nex = -1
        par = list(range(k))                    # parent array
        lab = list(range(k))                    # label array

        for p in arr:                      # here we set up our first iteration
            nex = self.delta(0, p, k)
            visited[p] = True
            q.append(p)
            par[nex] = 0
            lab[nex] = p
        if q[0] == 0:                           # if 0 is in the language, we take 0 out of the front of the queue
            q.pop(0)

        while len(q) > 0:                       # while our queue has items, we use our delta function to find the
            curr = q.pop(0)                     # next iteration. If the next iteration has already been visited, we
            if nex == 0:                        # continue. If the next iteration is 0, we exit the while loop.
                break
            for y in arr:
                nex = self.delta(curr, y, k)
                if nex == 0:
                    par[0] = curr
                    lab[0] = y
                    found = True
                    break
                if not visited[nex]:
                    visited[nex] = True
                    par[nex] = curr
                    lab[nex] = y
                    q.append(nex)

        ret = ""                                # our return string
        if found:                               # if a number was found, we iterate through the parent and label arrays
            mult_rev = ""                       # to get our result, in reverse. We then reverse the string and return.
            mult_rev += str(lab[0])
            i = par[0]
            while i != 0:
                mult_rev += str(lab[i])
                i = par[i]
            for d in range(len(mult_rev)):
                ret += mult_rev[- d - 1]

        return ret

    def delta(self, curr, nex, k):
        # this is our delta function (18 * j + a) % k
        return (10 * curr + nex) % k


def count(n):
    '''
    This is the function that creates the DFA for problem 1. It takes the input from main() and uses it as input
    for the generate_strings function. Since all strings are accepted if n < 6, if the user inputs a number
    less than 6, we just return 4**n.
    '''
    if int(n) < 6:
        print('n =', n, '\tAnswer: ', 4**int(n))
        return
    dfa = DFA_P1()
    print('n =', n, '\tAnswer: ', dfa.generate_strings(int(n)))


def MinString():
    '''
    This is the function that creaates the DFA for problem 2. We ask the user for the k input, then for the specified
    language to use. We then input those into our DFA and determine the smallest multiple. If no multiple is found
    (it returns ""), we print that there is no solution.
    '''
    inp1 = int(input('Please input a number between 1-99999: '))
    while inp1 < 1 or inp1 > 99999:
        inp1 = int(input('Invalid input\nPlease input a number between 1-99999: '))
    inp2 = str(input("Please input the language separated by comma's or spaces (x,y,z...): "))
    arr = []
    for i in range(len(inp2)):
        if inp2[i] != " " and inp2[i] != ",":
            arr.append(int(inp2[i]))
    dfa = DFA_P2()
    mult = DFA_P2.smallestMultiple(dfa, arr, inp1)
    if mult == "":
        print("No solution")
    else:
        print(mult)


def main():
    '''
    This is our main function. We have an eternal while loop that will only be exited if the user inputs the exit
    command. We ask the user to choose the problem they'd like to solve and run the program accordingly.
    '''
    while 1:
        inp1 = str(input('Please select program: (1) Problem 1, (2) Problem 2, (3) Quit: '))
        while inp1 != "1" and inp1 != "2" and inp1 != "3":
            inp1 = str(input('Invalid input\nPlease select program: (1) Problem 1, (2) Problem 2, (3) Quit: '))
        if inp1 == "1":
            inp2 = str(input('Please input length of string for DFA: '))
            count(inp2)
        if inp1 == "2":
            MinString()
        if inp1 == "3":
            exit(0)


main()
