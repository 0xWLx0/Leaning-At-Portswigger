f = open('passwords.txt', 'r')
d = open('newpass.txt', 'w+')

for i in f:
    for j in range(10):
        d.write(f'{i}')

f.close()
d.close()

