import datetime
import time
from blockchain import Blockchain

bc = Blockchain()

def main():

    bc.add("first block")
    bc.add("second block")

    while (getCommand() != 'exit'):
        pass

def getCommand():
    c = input('bc > ')
    pc = c.split()
    if len(pc) == 0:
        return
    elif pc[0] == 'add':
        addCommand(pc, c)
    elif pc[0] == 'get':
        getBlockCommand(pc)
    elif pc[0] == 'info':
        getInfo()
    elif pc[0] == 'gen':
        genCommand(pc)
    elif pc[0] == 'exit' or pc[0] == 'x':
        return 'exit'

def addCommand(pc, c):
    if len(pc) <= 1:
        return
    bc.add(str(c[4:]))

def getBlockCommand(pc):
    if len(pc) <= 1:
        return
    try:
        int(pc[1])
    except Exception:
        if pc[1] == 'last':
            print(bc.get(-1).toStringFull())
        elif pc[1] == 'all':
            for i in range(len(bc)):
                print(bc.get(i).toStringFull())
        else:
            print('Error: not a number')
        return

    if int(pc[1]) >= len(bc):
        print('Error: index out of range')
        return
    print(bc.get(int(pc[1])).toStringFull())

def getInfo():
    print('Blockchain length:', len(bc))

def genCommand(pc):
    if len(pc) <= 1:
        return
    try:
        int(pc[1])
    except Exception:
        print('Error: not a number')
        return

    for i in range(int(pc[1])):
        bc.add('generated at ' + str(time.ctime()))


if __name__ == "__main__":
    main()