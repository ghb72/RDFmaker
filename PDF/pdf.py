

import sys, os
import numpy as np

def getStr(name):
	with open(name) as infile:
		data = infile.readlines()
	n = int(data[0])
	f = 1.0
	w = []
	atpos = []
	for i in range(n):
		ele,sx,sy,sz = data[i+2].split()
		x = f*float(sx)
		y = f*float(sy)
		z = f*float(sz)
		w += [x,y,z]
		atpos.append([ele,x,y,z])
	size = 2*(max(w) -min(w))
	print('\nFile ',name)
	return atpos, size


def histogram(atpos,size):

	hfile = open('hpdf.dat','w')
	hfile.write('  #r(a)       PDF\n')
#	dx = 0.05
	l = int(size/dx)
	n = len(atpos)
	m = n*(n-1)/2
	hint = 0.0
	dmean = 0.0
	closest = 10.0
	farthest = 0.0
	h = np.zeros(l)
	for j in range(1,n):
		ele2,x2,y2,z2 = atpos[j]
		for i in range(j):
			ele1,x1,y1,z1 = atpos[i]
			d = np.sqrt((x2-x1)**2 +(y2-y1)**2 +(z2-z1)**2)
			hint += 1/d
			dmean += d/m
			if d < closest:
				closest = d
			if d > farthest:
				farthest = d
			k = int(d/dx-0.5)
			h[k] += 1/(d*dx)

	lh = int(farthest/dx-0.5) +3
	h = h[:lh]
	h *= 1/hint
	print(n,' Atoms,  ',m,' Pairs')
	print('Distance range {0:7.4f} --{1:9.4f}'.format(closest, farthest))
	print('Mean pair distance ', dmean)
	print('Normalization factor ', hint)

	for i in range(len(h)):
		ri = (i+1)*dx
		hfile.write('{0:7.3f}{1:12.5f}\n'.format(ri, h[i]))
	return h, dmean


def smooth(h,m):

	s = int(m/2)
	lh = len(h)
	hs = []
	for j in range(lh):
		x = 0.0
		for i in range(j-s,j+s+1):
			if 0 <= i and i < lh:
				x += h[i]
		hs.append(x/(2*s+1))
	return hs


def gaussConvolution(h,s):

	gfile = open('gpdf.dat','w')
	gfile.write('  #r(a)       PDF\n')
#	dx = 0.05
	lh = len(h)
	b = 1.0/(2*s*s)
	c = 1.0/(s*np.sqrt(2*(np.pi)))
	r = s
	rmax = lh*dx
	ga = []
	gsum = 0.0
	while r < rmax:
		gr = 0.0
		imin = int((r-3*s)/dx +0.5)
		imax = int((r+3*s)/dx +0.5) +1
		if imin < 0:
			imin = 0
		if imax > lh:
			imax = lh
		for i in range(imin,imax):
			ri = (i+1)*dx
			gr += c*h[i]*dx*np.exp(-b*(r-ri)**2)
		ga.append(gr)
		gsum += gr*dx
		gfile.write('{0:7.3f}{1:12.5f}\n'.format(r,gr))
		r += dx
	print('gsum =', gsum, 'rmax =', rmax, 'sigma =', s)
	g = np.array(ga)/gsum
	return g


def calcPDF(h):

	a = 2.72
#	b = 2.198
	b = 0.35
	lh = len(h)
	hs = smooth(h,10)
#	hs2 = smooth(hs1,5)
#	hs = smooth(hs2,5)
	bs1 = smooth(h,100)
	bs2 = smooth(bs1,100)
	gr = np.array(hs) -np.array(bs2)
	k = int(a /dx) -1
	y = h[k] -bs2[k]
#	c = b /y
	c = b /gr[k] 
	gr *= c
	print('Scaling factor ', c)

	pdffile = open(name[:-4] +'-pdf.dat','w')
	pdffile.write('  #r(A)    Histogram   Baseline       PDF\n')
	for i in range(lh):
		ri = (i+1)*dx
		pdffile.write('{0:7.3f}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(ri, hs[i], bs2[i], gr[i]))
	pdffile.close()




if __name__ == '__main__':
    name =  sys.argv[1]
#    s = float(sys.argv[2])


atpos, size = getStr(name)
dx = 0.02
hist, dmean = histogram(atpos,size)
calcPDF(hist)
#os.system('mv pdf.dat '+ name[:-4] +'-pdf.dat')
