f = open('lektuere', "rb")
s = f.read()
f.close()

f = open('multiboot', "rb")
sm = f.read()
f.close()

f = open('challenge', "rb")
sc = f.read()
f.close()

l1 = 0
flag = True

for data in s:
    l1  = l1 +1
print('lange')
l2 = 0
for data in sm:
    l2 = l2+1

k = 79 + l1 - l2

i = 0
j = []
srt = ''
for data in s:
    if 70853 > i > 79:
        j.append(data)
        srt = srt + chr(data)
    i = i + 1

f = open('test', "wb")
f.write(bytes(j))
f.close()
#print(j)
#print(srt)
j = []
i = 0
for jj in range(20):
    j.append(sc[i])
    i = i + 1
#print(j)



f = open('test', "rb")
sm = f.read()
f.close()
j = []
for data in sm:
    j.append(data)
#print(j)
f = open('lektuere', "rb")
s = f.read()
f.close()

i = 0
j = []
srt = ''
for data in s:
    if 45300 > i > 45167:
        j.append(data)
        srt = srt + chr(data)
    i = i + 1
print(srt)
print(j)
print('11111')

lis1 = []
for i in range(10):
    lis1.append(s[45168+i*4])

lis2 = [170,67,170,205,128,35,31,17,13,193]
lis3 = []
for i in range(10):
    k = lis2[i] - 67
    if k < 0:
        k = k + 256
    lis3.append(k)
lis4 = []
for i in range(10):
    lis4.append(lis1[i] ^ lis3[i])
str = ''
for i in range(10):
    str = str + chr(lis4[i])
print(str)
print('111111')