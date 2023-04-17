passwd  = 'peter'
f = open('passwords.txt', 'r')
d = open('newpass.txt', 'w+')

for i in f: 
    d.write(f"{i}")
    d.write(f"{passwd}\n")

f.close()
d.close()

