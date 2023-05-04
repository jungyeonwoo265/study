import random

fin = []
for i in range(10):
    result = []
    while len(result) < 6:
        num = random.randint(1, 45)
        if num not in result:
            result.append(num)
    fin.append(result)

for i in fin:
    print(sorted(i))
