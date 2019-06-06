import binascii
filename = 'HelloWorld.exe'
with open(filename, 'rb') as f:
    content = f.read()

data = list(str(binascii.hexlify(content)))


file = open('OUT.txt','w')
file.write('[')
i = 2
while i < len(data)-1:
    file.write('\\x'+data[i]+data[i+1]+',')
    i = i + 2
file.write(']')
file.close()


