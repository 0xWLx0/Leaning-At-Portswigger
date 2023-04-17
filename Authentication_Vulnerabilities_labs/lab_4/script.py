name1 = 'carlos'
name2 = 'wiener'
l = 0

f = open('newusers.txt', 'w+')

while l <= 100:
    f.write(f'{name1}\n')
    f.write(f'{name2}\n')
    l += 1

f.close()

