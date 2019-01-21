import datetime
import time
from blockchain import Ledger

ledger = Ledger(Ledger.MerkleTree)

def main():
    
    ledger.storage.add("first block")
    ledger.storage.add("second block")

    while (getCommand() != 'exit'):
        pass

def getCommand():
    c = input('ledger.bc > ')
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
    elif pc[0] == 'change':
        changeBlockCommand(pc, c)
    elif pc[0] == 'val':
        validateSlowCommand(pc)
    elif pc[0] == 'exit' or pc[0] == 'x':
        return 'exit'

def addCommand(pc, c):
    if len(pc) <= 1:
        return
    ledger.storage.add(str(c[4:]))

def getBlockCommand(pc):
    if len(pc) <= 1:
        return
    try:
        f = int(pc[1])
    except Exception:
        if pc[1] == 'last':
            print(ledger.storage.get(-1).toStringFull())
        elif pc[1] == 'all':
            for i in range(len(ledger.storage)):
                print(ledger.storage.get(i).toStringFull())
        else:
            print('Error: not a number')
        return

    if int(pc[1]) >= len(ledger.storage):
        print('Error: index out of range')
        return
    print(ledger.storage.get(int(pc[1])).toStringFull())

def getInfo():
    print('Blockchain length:', len(ledger.storage))

def genCommand(pc):
    if len(pc) <= 1:
        return
    try:
        int(pc[1])
    except Exception:
        print('Error: not a number')
        return

    for i in range(int(pc[1])):
        ledger.storage.add('generated at ' + str(time.ctime()))

# Changes a past block's data. This is only used for verifying that the validation
# function works appropriately, since it should be impossible for obedient nodes
def changeBlockCommand(pc, c):
    if len(pc) <= 1:
        return
    try:
        int(pc[1])
    except Exception:
        print('Error: not a number')
        return
    if int(pc[1]) >= len(ledger.storage):
        print('Error: index out of range')
        return
    if ledger.storage.blocks[int(pc[1])].data != str(c[9:]):
        ledger.storage.blocks[int(pc[1])].data = str(c[9:]).encode('utf-8')
    else:
        print('Error: data matches block data')

# Validates the blockchain by computing the hash of each block and
# checking the previous hash in the next block
def validateSlowCommand(pc):
    startTime = time.time()
    noErrors = True
    for i in range(1, len(ledger.storage.blocks)):
        if ledger.storage.blocks[i].prevHash != ledger.storage.blocks[i-1].hash():
            print('Block ' + str(i-1) + ' is invalid.')
            noErrors = False

    if noErrors:
        print('Blockchain is valid.')
    print(str(round(time.time() - startTime, 3)) + ' seconds taken.')

if __name__ == "__main__":
    main()



    