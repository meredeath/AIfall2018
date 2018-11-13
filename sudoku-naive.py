#! /usr/bin/python3
import sys

##############Opening Files#####################
inputfile = open(sys.argv[1],'r')
outputfile = open(sys.argv[2],'w+')
name = sys.argv[3]

stuff = inputfile.read()
board = []
if not stuff:
    print("Error: your input file has nothing in it!")
else:
    things = stuff.strip().split("\n")
    found = False
    c1 = 0
    length = len(things)
    while c1 < length:
        if len(things[c1])>0 and things[c1][0:4] == "name":
            if things[c1] == name:
                found = True
                counter = 1
                while counter < 10:
                    temp = things[c1+counter].split(",")
                    board += temp
                    counter+=1
        c1+=1
    if not found:
        print("Error: your requested board was not found inside of the input file.")

cliques=[[0,1,2,3,4,5,6,7,8],
[9,10,11,12,13,14,15,16,17],
[18,19,20,21,22,23,24,25,26],
[27,28,29,30,31,32,33,34,35],
[36,37,38,39,40,41,42,43,44],
[45,46,47,48,49,50,51,52,53],
[54,55,56,57,58,59,60,61,62],
[63,64,65,66,67,68,69,70,71],
[72,73,74,75,76,77,78,79,80],
[0,9,18,27,36,45,54,63,72],
[1,10,19,28,37,46,55,64,73],
[2,11,20,29,38,47,56,65,74],
[3,12,21,30,39,48,57,66,75],
[4,13,22,31,40,49,58,67,76],
[5,14,23,32,41,50,59,68,77],
[6,15,24,33,42,51,60,69,78],
[7,16,25,34,43,52,61,70,79],
[8,17,26,35,44,53,62,71,80],
[0,1,2,9,10,11,18,19,20],
[3,4,5,12,13,14,21,22,23],
[6,7,8,15,16,17,24,25,26],
[27,28,29,36,37,38,45,46,47],
[30,31,32,39,40,41,48,49,50],
[33,34,35,42,43,44,51,52,53],
[54,55,56,63,64,65,72,73,74],
[57,58,59,66,67,68,75,76,77],
[60,61,62,69,70,71,78,79,80]
]

cliqdict = {}
c2 = 0
while c2 < 81:
    for i in cliques:
        if c2 in i:
            if c2 not in cliqdict:
                cliqdict[c2] = []
                cliqdict[c2].append(i)
            else:
                cliqdict[c2].append(i)
    c2 += 1

    
def solve(index, cur):
    if index > 80:
        print("No solution found")
        return False
    if cur[index] == "_":
        c4 = 1
        can = True
        while c4 < 10:
            for i in cliqdict[index]:
                print("i in cliqdict[index]: ")
                print(i)
                for k in i:
                    if cur[i] == str(c4):
                        can = False
            if can:
                cur[index] = c4
                break
            c4 += 1
c3 = 0
while c3 < 81:
    if board[c3] == "_":
        orig = board
        solve(c3, board)
    c3 += 1

print(board)
