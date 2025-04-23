'\npymmh3 was written by Fredrik Kihlander and enhanced by Swapnil Gusani, and is placed in the public\ndomain. The authors hereby disclaim copyright to this source code.\n\npure python implementation of the murmur3 hash algorithm\n\nhttps://code.google.com/p/smhasher/wiki/MurmurHash3\n\nThis was written for the times when you do not want to compile c-code and install modules,\nand you only want a drop-in murmur3 implementation.\n\nAs this is purely python it is FAR from performant and if performance is anything that is needed\na proper c-module is suggested!\n\nThis module is written to have the same format as mmh3 python package found here for simple conversions:\n\nhttps://pypi.python.org/pypi/mmh3/2.3.1\n'
import sys as _sys
if _sys.version_info>(3,0):
	def xrange(a,b,c):return range(a,b,c)
	def xencode(x):
		if isinstance(x,bytes)or isinstance(x,bytearray):return x
		else:return x.encode()
else:
	def xencode(x):return x
del _sys
def hash(key,seed=0):
	' Implements 32bit murmur3 hash. ';B=key;B=bytearray(xencode(B))
	def L(h):h^=h>>16;h=h*2246822507&4294967295;h^=h>>13;h=h*3266489909&4294967295;h^=h>>16;return h
	F=len(B);I=int(F/4);C=seed;J=3432918353;K=461845907
	for D in xrange(0,I*4,4):A=B[D+3]<<24|B[D+2]<<16|B[D+1]<<8|B[D+0];A=J*A&4294967295;A=(A<<15|A>>17)&4294967295;A=K*A&4294967295;C^=A;C=(C<<13|C>>19)&4294967295;C=C*5+3864292196&4294967295
	G=I*4;A=0;E=F&3
	if E>=3:A^=B[G+2]<<16
	if E>=2:A^=B[G+1]<<8
	if E>=1:A^=B[G+0]
	if E>0:A=A*J&4294967295;A=(A<<15|A>>17)&4294967295;A=A*K&4294967295;C^=A
	H=L(C^F)
	if H&2147483648==0:return H
	else:return-((H^4294967295)+1)
def hash128(key,seed=0,x64arch=True):
	' Implements 128bit murmur3 hash. ';A=key
	def B(key,seed):
		' Implements 128bit murmur3 hash for x64. ';A=key
		def L(k):k^=k>>33;k=k*0xff51afd7ed558ccd&0xffffffffffffffff;k^=k>>33;k=k*0xc4ceb9fe1a85ec53&0xffffffffffffffff;k^=k>>33;return k
		I=len(A);M=int(I/16);D=seed;E=seed;J=0x87c37b91114253d5;K=0x4cf5ad432745937f
		for G in xrange(0,M*8,8):B=A[2*G+7]<<56|A[2*G+6]<<48|A[2*G+5]<<40|A[2*G+4]<<32|A[2*G+3]<<24|A[2*G+2]<<16|A[2*G+1]<<8|A[2*G+0];C=A[2*G+15]<<56|A[2*G+14]<<48|A[2*G+13]<<40|A[2*G+12]<<32|A[2*G+11]<<24|A[2*G+10]<<16|A[2*G+9]<<8|A[2*G+8];B=J*B&0xffffffffffffffff;B=(B<<31|B>>33)&0xffffffffffffffff;B=K*B&0xffffffffffffffff;D^=B;D=(D<<27|D>>37)&0xffffffffffffffff;D=D+E&0xffffffffffffffff;D=D*5+1390208809&0xffffffffffffffff;C=K*C&0xffffffffffffffff;C=(C<<33|C>>31)&0xffffffffffffffff;C=J*C&0xffffffffffffffff;E^=C;E=(E<<31|E>>33)&0xffffffffffffffff;E=D+E&0xffffffffffffffff;E=E*5+944331445&0xffffffffffffffff
		H=M*16;B=0;C=0;F=I&15
		if F>=15:C^=A[H+14]<<48
		if F>=14:C^=A[H+13]<<40
		if F>=13:C^=A[H+12]<<32
		if F>=12:C^=A[H+11]<<24
		if F>=11:C^=A[H+10]<<16
		if F>=10:C^=A[H+9]<<8
		if F>=9:C^=A[H+8]
		if F>8:C=C*K&0xffffffffffffffff;C=(C<<33|C>>31)&0xffffffffffffffff;C=C*J&0xffffffffffffffff;E^=C
		if F>=8:B^=A[H+7]<<56
		if F>=7:B^=A[H+6]<<48
		if F>=6:B^=A[H+5]<<40
		if F>=5:B^=A[H+4]<<32
		if F>=4:B^=A[H+3]<<24
		if F>=3:B^=A[H+2]<<16
		if F>=2:B^=A[H+1]<<8
		if F>=1:B^=A[H+0]
		if F>0:B=B*J&0xffffffffffffffff;B=(B<<31|B>>33)&0xffffffffffffffff;B=B*K&0xffffffffffffffff;D^=B
		D^=I;E^=I;D=D+E&0xffffffffffffffff;E=D+E&0xffffffffffffffff;D=L(D);E=L(E);D=D+E&0xffffffffffffffff;E=D+E&0xffffffffffffffff;return E<<64|D
	def C(key,seed):
		' Implements 128bit murmur3 hash for x86. ';N=seed;A=key
		def O(h):h^=h>>16;h=h*2246822507&4294967295;h^=h>>13;h=h*3266489909&4294967295;h^=h>>16;return h
		M=len(A);T=int(M/16);B=N;F=N;G=N;H=N;P=597399067;Q=2869860233;R=951274213;S=2716044179
		for K in xrange(0,T*16,16):C=A[K+3]<<24|A[K+2]<<16|A[K+1]<<8|A[K+0];D=A[K+7]<<24|A[K+6]<<16|A[K+5]<<8|A[K+4];E=A[K+11]<<24|A[K+10]<<16|A[K+9]<<8|A[K+8];I=A[K+15]<<24|A[K+14]<<16|A[K+13]<<8|A[K+12];C=P*C&4294967295;C=(C<<15|C>>17)&4294967295;C=Q*C&4294967295;B^=C;B=(B<<19|B>>13)&4294967295;B=B+F&4294967295;B=B*5+1444728091&4294967295;D=Q*D&4294967295;D=(D<<16|D>>16)&4294967295;D=R*D&4294967295;F^=D;F=(F<<17|F>>15)&4294967295;F=F+G&4294967295;F=F*5+197830471&4294967295;E=R*E&4294967295;E=(E<<17|E>>15)&4294967295;E=S*E&4294967295;G^=E;G=(G<<15|G>>17)&4294967295;G=G+H&4294967295;G=G*5+2530024501&4294967295;I=S*I&4294967295;I=(I<<18|I>>14)&4294967295;I=P*I&4294967295;H^=I;H=(H<<13|H>>19)&4294967295;H=B+H&4294967295;H=H*5+850148119&4294967295
		L=T*16;C=0;D=0;E=0;I=0;J=M&15
		if J>=15:I^=A[L+14]<<16
		if J>=14:I^=A[L+13]<<8
		if J>=13:I^=A[L+12]
		if J>12:I=I*S&4294967295;I=(I<<18|I>>14)&4294967295;I=I*P&4294967295;H^=I
		if J>=12:E^=A[L+11]<<24
		if J>=11:E^=A[L+10]<<16
		if J>=10:E^=A[L+9]<<8
		if J>=9:E^=A[L+8]
		if J>8:E=E*R&4294967295;E=(E<<17|E>>15)&4294967295;E=E*S&4294967295;G^=E
		if J>=8:D^=A[L+7]<<24
		if J>=7:D^=A[L+6]<<16
		if J>=6:D^=A[L+5]<<8
		if J>=5:D^=A[L+4]
		if J>4:D=D*Q&4294967295;D=(D<<16|D>>16)&4294967295;D=D*R&4294967295;F^=D
		if J>=4:C^=A[L+3]<<24
		if J>=3:C^=A[L+2]<<16
		if J>=2:C^=A[L+1]<<8
		if J>=1:C^=A[L+0]
		if J>0:C=C*P&4294967295;C=(C<<15|C>>17)&4294967295;C=C*Q&4294967295;B^=C
		B^=M;F^=M;G^=M;H^=M;B=B+F&4294967295;B=B+G&4294967295;B=B+H&4294967295;F=B+F&4294967295;G=B+G&4294967295;H=B+H&4294967295;B=O(B);F=O(F);G=O(G);H=O(H);B=B+F&4294967295;B=B+G&4294967295;B=B+H&4294967295;F=B+F&4294967295;G=B+G&4294967295;H=B+H&4294967295;return H<<96|G<<64|F<<32|B
	A=bytearray(xencode(A))
	if x64arch:return B(A,seed)
	else:return C(A,seed)
def hash64(key,seed=0,x64arch=True):
	' Implements 64bit murmur3 hash. Returns a tuple. ';C=hash128(key,seed,x64arch);A=C&0xffffffffffffffff
	if A&0x8000000000000000==0:D=A
	else:D=-((A^0xffffffffffffffff)+1)
	B=C>>64&0xffffffffffffffff
	if B&0x8000000000000000==0:E=B
	else:E=-((B^0xffffffffffffffff)+1)
	return int(D),int(E)
def hash_bytes(key,seed=0,x64arch=True):
	' Implements 128bit murmur3 hash. Returns a byte string. ';A=hash128(key,seed,x64arch);B=''
	for D in xrange(0,16,1):C=A&255;B=B+str(chr(C));A=A>>8
	return B
if __name__=='__main__':
	import argparse;parser=argparse.ArgumentParser('pymurmur3','pymurmur [options] "string to hash"');parser.add_argument('--seed',type=int,default=0);parser.add_argument('strings',default=[],nargs='+');opts=parser.parse_args()
	for str_to_hash in opts.strings:sys.stdout.write('"%s" = 0x%08X\n'%(str_to_hash,hash(str_to_hash)))