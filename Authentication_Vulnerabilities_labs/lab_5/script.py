d = open('usernames.txt', 'r')
f = open('newusers.txt', 'w+')

for i in d:
    for j in range(5):
        f.write(f'{i}')

d.close()
f.close()

