for j in ['a','b','c']:
    print(j)
    for i in range(3):
        print(i)
        if i == 1:
            print('inner')
            break
print('outer')