for i in range(1, 4):
    exec(f'var_{i} = list(range(i))')

for i in range(1, 4):
    print(f'var_{i}:', eval(f'var_{i}'))
