import random
for i in range(500):
    alistA = random.sample(range(1,36),5)
    alistB = random.sample(range(1,13),2)

    print("所有数为",str(alistA) +"/" + str(alistB))