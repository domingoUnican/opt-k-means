#!/usr/bin/python


def enumerate_list(l,n):
	"""
	Select n elements without repetitions, from {x|0<=x<l} (if l is an integer) or l itself (if is a list)
	"""
	if isinstance(l,int):
		m=l
		selection=False
	else:
		m=len(l)
		selection=True
	d=0
	L=range(n) #with invariant L[i]<L[i+1]
	while L[n-1]<m:
		if selection:
			#selecting elements from l
			yield [l[k] for k in L]
		else:
			yield L[:]
		#advance to the next
		d=0
		L[d]+=1
		while L[d]>=L[d+1]:
			if d==0:
				L[d]=0
			else:
				L[d]=L[d-1]+1 #The first element keeping the invariant
			d+=1
			L[d]+=1
			if d==n-1: break

def alternate(g,period=2,phase=0):
	"""
	Given a generator g, returns a generator along [g(phase+period*k), k in nat]
	Works for unlimited generators
	"""
	for i in xrange(phase):
		g.next()
	for x in g:
		yield x
		for i in xrange(period-1):
			g.next()

if __name__=="__main__":
	for L in enumerate_list(7,3):
		print L
	print "----"
	for L in enumerate_list(["A","B","C","D","E","F"],4):
		print L
	print "----"
	for x in alternate((y for y in xrange(10)),period=2,phase=0): print x
	for x in alternate((y for y in xrange(10)),period=2,phase=1): print x
	print "----"
	for l in alternate(enumerate_list(7,2),period=3,phase=0):
		print l
	print "----"
	for l in alternate(enumerate_list(7,2),period=3,phase=1):
		print l
	print "----"
	for l in alternate(enumerate_list(7,2),period=3,phase=2):
		print l
	print "----"
	count=0
	for L in enumerate_list(87,4):
		count+=1
	print count

