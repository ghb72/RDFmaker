import os
import numpy as np

# ALL THESE FUNCTIONS WORK: coords = Shell(ns,d,...)
# struc = 'fcc' or 'bcc' or 'simple'
# coords = centerStr(atpos) or = sphericalShave(coords,r)

def cubeShell(ns,d,struc):
	if struc == 'bcc':
		d *= 2/np.sqrt(3)
	elif struc == 'fcc':
		d *= np.sqrt(2)
	a = np.array([d,0.0,0.0])
	b = np.array([0.0,d,0.0])
	c = np.array([0.0,0.0,d])
	f = -0.5*ns*d
	g = -0.5*(ns-1)*d
	u = np.array([f,f,f])
	p = []
	for k in range(ns+1):
		for j in range(ns+1):
			for i in range(ns+1):
#				if i==0 or i==ns or j==0 or j==ns or k==0 or k==ns:
				p.append(u+ i*a+ j*b+ k*c)
	if struc == 'simple':
		return p
	elif struc == 'bcc':
		v = np.array([g,g,g])
		for k in range(ns):
			for j in range(ns):
				for i in range(ns):
					p.append(v+ i*a+ j*b+ k*c)
		return p
	elif struc == 'fcc':
		v = [np.array([g,g,f]),np.array([g,f,g]),np.array([f,g,g])]
		for k in range(ns+1):
			for j in range(ns):
				for i in range(ns):
#					if i==0 or i==ns-1 or j==0 or j==ns-1 or k==0 or k==ns:
					p.append(v[0]+ i*a+ j*b+ k*c)
		for k in range(ns+1):
			for j in range(ns):
				for i in range(ns):
#					if i==0 or i==ns-1 or j==0 or j==ns-1 or k==0 or k==ns:
					p.append(v[1]+ i*a+ k*b+ j*c)
		for k in range(ns+1):
			for j in range(ns):
				for i in range(ns):
#					if i==0 or i==ns-1 or j==0 or j==ns-1 or k==0 or k==ns:
					p.append(v[2]+ k*a+ i*b+ j*c)
		return p
	
def octShell(ns,d,cut=False):

	s2 = np.sqrt(2)
	edge = float(ns*d)
	a = edge/s2

	edges = [[1,2,3,4],[2],[3],[4],[1],[1,2,3,4]]
	faces = [[0,1],[1,2],[2,3],[3,0],[8,9],[9,10],[10,11],[11,8]]
# Vertices
	v = []
	v.append(np.array([0.0,0.0,-a]))
	v.append(np.array([ a,0.0,0.0]))
	v.append(np.array([0.0, a,0.0]))
	v.append(np.array([-a,0.0,0.0]))
	v.append(np.array([0.0,-a,0.0]))
	v.append(np.array([0.0,0.0, a]))
# Edge vectors
	ev = []
	for j in range(len(edges)):
		ed = edges[j]
		for i in ed:
			ev.append((v[i]-v[j])/ns)
# Edges
	e = []
	f = []
	for k1 in range(1,ns):
		m = 0
		for j in range(len(edges)):
			ed = edges[j]
			for i in ed:
				e.append(v[j]+ k1*ev[m])
				m += 1
# Faces
		k3 = 1
		while (k1+k3) < ns:
			for i in range(4):
				fv = faces[i]
				f.append(v[0]+ k1*ev[fv[0]]+ k3*ev[fv[1]])
			for i in range(4,8):
				fv = faces[i]
				f.append(v[5]+ k1*ev[fv[0]]+ k3*ev[fv[1]])
			k3 += 1

	coords = v + e + f
	if cut:
		b = a*0.72
		n = len(coords)
		cc = []
		for x,y,z in coords:
			w1 = min([x,y,z])
			w2 = max([x,y,z])
			if w1 > -b and w2 < b:
				cc.append([x,y,z])
		coords = cc

	return coords

def cbocShell(ns,d,cut=False):

	s2 = np.sqrt(2)
	s3 = np.sqrt(3)
	edge = float(ns*d)

	vertices = [[1,0,0],[0,1,0],[-1,1,0],[-1,0,0],[0,-1,0],[1,-1,0],
		[1,-1,1],[0,0,1],[0,-1,1],[0,0,-1],[0,1,-1],[-1,1,-1]]
	edges = [[1,6,10],[2,7,10],[3,7,11],[4,8,11],[5,8,9],
		[0,6,9],[7,8],[8],[],[10,11],[11]]
	faces3 = [[0,2],[3,4],[6,8],[9,10],[12,14],
		[15,16],[18,19],[],[],[21,22]]
	faces4 = [[0,1],[3,5],[6,7],[9,11],[12,13],[15,17]] 
# Vertices
	a = np.array([edge,0.0,0.0])
	b = np.array([edge/2,s3*edge/2,0.0])
	c = np.array([0.0,edge/s3,s2*edge/s3])
	v = []
	for vec in vertices:
		i,j,k = vec
		v.append(i*a +j*b +k*c)
# Edge vectors
	ev = []
	for j in range(len(edges)):
		ed = edges[j]
		for i in ed:
			ev.append((v[i]-v[j])/ns)
# Edges
	e = []
	f = []
	for k1 in range(1,ns):
		m = 0
		for j in range(len(edges)):
			ed = edges[j]
			for i in ed:
				e.append(v[j]+ k1*ev[m])
				m += 1
# Triangular Faces
		k3 = 1
		while (k1+k3) < ns:
			for i in range(7):
				fv = faces3[i]
				f.append(v[i]+ k1*ev[fv[0]]+ k3*ev[fv[1]])
			f.append(v[9]+ k1*ev[21] +k3*ev[22])
			k3 += 1
# Square Faces
		for k4 in range(1,ns):
			for i in range(6):
				fv = faces4[i]
				f.append(v[i]+ k1*ev[fv[0]]+ k4*ev[fv[1]])

	coords = v + e + f
	if cut:
		n = len(coords)
		cc = []
		for x,y,z in coords:
			if x < -0.001*d:
				cc.append([x+d/2,y,z])
			elif x > -0.501*d:
				cc.append([x-d/2,y,z])
		del(cc[9])
		del(cc[7])
		coords = cc

	return coords

def acboShell(ns,d,cut=False):

	s2 = np.sqrt(2)
	s3 = np.sqrt(3)
	edge = float(ns*d)

	vertices = [[1,0,0],[0,1,0],[-1,1,0],[-1,0,0],[0,-1,0],[1,-1,0],
		[1,-1,1],[0,0,1],[0,-1,1],[1.0/3,1.0/3,-1],
		[-2.0/3,4.0/3,-1],[-2.0/3,1.0/3,-1]]
	edges = [[1,6,9],[2,7,10],[3,7,10],[4,8,11],[5,8,11],
		[0,6,9],[7,8],[8],[],[10,11],[11]]
	faces3 = [[1,3,4],[1,3,5],[3,9,10],[3,9,11],[5,15,16],
		[5,15,17],[6,18,19],[9,21,22]]
	faces4 = [[0,0,1],[0,0,2],[2,6,7],[2,6,8],[4,12,13],[4,12,14]] 
# Vertices
	a = np.array([edge,0.0,0.0])
	b = np.array([edge/2,s3*edge/2,0.0])
	c = np.array([0.0,edge/s3,s2*edge/s3])
	v = []
	for vec in vertices:
		i,j,k = vec
		v.append(i*a +j*b +k*c)
# Edge vectors
	ev = []
	for j in range(len(edges)):
		ed = edges[j]
		for i in ed:
			ev.append((v[i]-v[j])/ns)
# Edges
	e = []
	f = []
	for k1 in range(1,ns):
		m = 0
		for j in range(len(edges)):
			ed = edges[j]
			for i in ed:
				e.append(v[j]+ k1*ev[m])
				m += 1
# Triangular Faces
		k3 = 1
		while (k1+k3) < ns:
			for fv in faces3:
				f.append(v[fv[0]]+ k1*ev[fv[1]]+ k3*ev[fv[2]])
			k3 += 1
# Square Faces
		for k4 in range(1,ns):
			for fv in faces4:
				f.append(v[fv[0]]+ k1*ev[fv[1]]+ k4*ev[fv[2]])

	coords = v + e + f
	if cut:
		n = len(coords)
		cc = []
		for x,y,z in coords:
			if x < -0.001*d:
				cc.append([x+d/2,y,z])
			elif x > -0.501*d:
				cc.append([x-d/2,y,z])
		del(cc[9])
		del(cc[7])
		coords = cc

	return coords

def icoShell(ns,d,cut=False):

	edge = ns*d
	s5 = np.sqrt(5)
	t = np.arctan((s5-1)/2)
	r = edge/(2*np.sin(t))
# Vertices
	v = []
	x0 = edge/2
	y0 = r*np.cos(t)
	for j in [0,1]:
		for i in [0,1]:
			v.append(np.array([(-1)**i*x0,(-1)**j*y0,0.0]))
	for j in [0,1]:
		for i in [0,1]:
			v.append(np.array([0.0,(-1)**i*x0,(-1)**j*y0]))
	for j in [0,1]:
		for i in [0,1]:
			v.append(np.array([(-1)**i*y0,0.0,(-1)**j*x0]))
	if ns == 1:
		return v

	edges = [[1,4,6,8,10],[4,6,9,11],[3,5,7,8,10],[5,7,9,11],
		[5,8,9],[8,9],[7,10,11],[10,11],[10],[11]]
	faces = [[[0,1],[0,2],[1,3],[2,4],[3,4]],[[5,7],[6,8],[7,8]],
		[[9,10],[9,11],[10,12],[11,13],[12,13]],
		[[14,16],[15,17],[16,17]],[[18,19],[18,20]],[],
		[[23,24],[23,25]]]	
# Edge vectors
	ev = []
	for j in range(len(edges)):
		ed = edges[j]
		for i in ed:
			ev.append((v[i]-v[j])/ns)
# Edges
	e = []
	f = []
	for k1 in range(1,ns):
		m = 0
		for j in range(len(edges)):
			ed = edges[j]
			for i in ed:
				e.append(v[j]+k1*ev[m])
				m += 1
# Faces
		k2 = 1
		while (k1+k2) < ns: 
			for i in range(len(faces)):
				for fv in faces[i]:
					f.append(v[i] + k1*ev[fv[0]] + k2*ev[fv[1]])
			k2 += 1

	coords = v + e + f
	if cut:
		n = len(coords)
		cc = []
		for x,y,z in coords:
			if z < -0.810*d:
				cc.append([x,y,z+d/2])
			elif z < -0.501*d:
				cc.append([x,y,z+0.809*d])
			elif z < -0.499*d:
				cc.append([x,y,z+d/2])
			elif z > 0.810*d:
				cc.append([x,y,z-d/2])
		coords = cc

	return coords

def tdecShell(ns,d,cut=False):

	t = 2*np.pi/5
	edge = float(ns*d)
	r = edge / (2*np.sin(t/2))
	h = edge/2 + np.sqrt(edge*edge-r*r)

	edges = [[1,2,3,4,5],[2,6],[3,7],[4,8],[5,9],[1,10],
		[7],[8],[9],[10],[6],[6,7,8,9,10]]
	faces3 = [[0,1],[1,2],[2,3],[3,4],[4,0],
		 [20,21],[21,22],[22,23],[23,24],[24,20]]
	faces4 = [[5,6],[7,8],[9,10],[11,12],[13,14]]
# Vertices
	v = [np.array([0.0,0.0,-h])]
	for j in [0,1]:
		for i in range(5):
			x = r*np.cos(i*t)
			y = r*np.sin(i*t)
			z = edge*(j-0.5)
			v.append(np.array([x,y,z]))
	v.append(np.array([0.0,0.0,h]))
# Edge vectors
	ev = []
	for j in range(len(edges)):
		ed = edges[j]
		for i in ed:
			ev.append((v[i]-v[j])/ns)
# Edges
	e = []
	f = []
	for k1 in range(1,ns):
		m = 0
		for j in range(len(edges)):
			ed = edges[j]
			for i in ed:
				e.append(v[j]+ k1*ev[m])
				m += 1
# Triangular Faces
		k3 = 1
		while (k1+k3) < ns:
			for i in range(5):
				fv = faces3[i]
				f.append(v[0]+ k1*ev[fv[0]]+ k3*ev[fv[1]])
			for i in range(5,10):
				fv = faces3[i]
				f.append(v[11]+ k1*ev[fv[0]]+ k3*ev[fv[1]])
			k3 += 1
# Square Faces
		for k4 in range(1,ns):
			for i in range(len(faces4)):
				fv = faces4[i]
				f.append(v[i+1]+ k1*ev[fv[0]]+ k4*ev[fv[1]])

	coords = v + e + f
	if cut:
		n = len(coords)
		cc = []
		for x,y,z in coords:
			if z < -1.501*d:
				cc.append([x,y,z+d*1.50])
			elif z > 1.501*d:
				cc.append([x,y,z-d*1.50])
		coords = cc

	return coords

def decShell(ns,d,cut=False):

	t = 2*np.pi/5
	edge = float(ns*d)
	r = edge / (2*np.sin(t/2))
	h = np.sqrt(edge*edge-r*r)

	edges = [[1,2,3,4,5],[2],[3],[4],[5],[1],
		[1,2,3,4,5]]
	faces3 = [[0,1],[1,2],[2,3],[3,4],[4,0],
		 [10,11],[11,12],[12,13],[13,14],[14,10]]
# Vertices
	v = [np.array([0.0,0.0,-h])]
	for i in range(5):
		x = r*np.cos(i*t)
		y = r*np.sin(i*t)
		v.append(np.array([x,y,0.0]))
	v.append(np.array([0.0,0.0,h]))
# Edge vectors
	ev = []
	for j in range(len(edges)):
		ed = edges[j]
		for i in ed:
			ev.append((v[i]-v[j])/ns)
# Edges
	e = []
	f = []
	for k1 in range(1,ns):
		m = 0
		for j in range(len(edges)):
			ed = edges[j]
			for i in ed:
				e.append(v[j]+ k1*ev[m])
				m += 1
# Triangular Faces
		k3 = 1
		while (k1+k3) < ns:
			for i in range(5):
				fv = faces3[i]
				f.append(v[0]+ k1*ev[fv[0]]+ k3*ev[fv[1]])
			for i in range(5,10):
				fv = faces3[i]
				f.append(v[6]+ k1*ev[fv[0]]+ k3*ev[fv[1]])
			k3 += 1

	coords = v + e + f
	return coords

def rdodShell(ns,d,cut=False):

	edge = ns*d
	s2 = np.sqrt(2)
	t = np.arctan(1/s2)
	g = edge*np.cos(t)
	h = edge*np.sin(t)
	l = s2*np.cos(t)/np.sin(t)

	edges = [[1,2,3,4],[5,8],[5,6],[6,7],[7,8],[9,10],
		[10,11],[11,12],[12,9],[13],[13],[13],[13]]
	faces = [[0,1],[1,2],[2,3],[3,0],[4,5],[6,7],[8,9],[10,11],
		[12,13],[14,15],[16,17],[18,19]]
# Vertices
	a = np.array([g,0.0,0.0])
	b = np.array([0.0,g,0.0])
	c = np.array([0.0,0.0,h])
	v = [-l*c,a-c,b-c,-a-c,-b-c,a+b,-a+b,
	     -a-b,a-b,a+c,b+c,-a+c,-b+c,l*c]
# Edge vectors
	ev = []
	for j in range(len(edges)):
		ed = edges[j]
		for i in ed:
			ev.append((v[i]-v[j])/ns)
# Edges
	e = []
	f = []
	for k1 in range(1,ns):
		m = 0
		for j in range(len(edges)):
			ed = edges[j]
			for i in ed:
				e.append(v[j]+ k1*ev[m])
				m += 1
# Faces
		for k2 in range(1,ns):
			for i in range(len(faces)):
				fv = faces[i]
				if i < 4:
					u = v[0]
				else:
					u = v[i-3]
				f.append(u+ k1*ev[fv[0]]+ k2*ev[fv[1]])
	coords = v + e + f
	return coords

def hcpShell(ns,d):

	s2 = np.sqrt(2)
	s3 = np.sqrt(3)
	a = np.array([d,0.0,0.0])
	b = np.array([-d/2,s3*d/2,0.0])
	c = np.array([0.0,d/s3,0.0])
	h = np.array([0.0,0.0,s2*d/s3])
	evec = [-a-b, -a, b, a+b, a, -b]
	base = [np.array([0.0,0.0,0.0])]
	for k in range(1,ns+1):
		ring = [k*a]
		for e in evec:
			for j in range(k):
				ring.append(ring[-1] +e)
		base += ring[1:]

	m = 3*ns*ns -3*ns +1
	coords = base[m:]
	for k in range(ns):
		x = ns -(k+1)/2
		q = divmod(k,2)[1]
		m1 = 3*(x-1)*(x-1) +q*(3*x-2)
		m2 = 3*x*x +q*(3*x+1)
		#print(m2, floor(m2), m1, floor(m1))
		layer = []
		for vec in base[:int(m2)]: #he modificado m2->int(m2)
			layer += [vec +(1-q)*c +(k+1)*h]
			layer += [vec +(1-q)*c -(k+1)*h]
		if k < ns-1:
			coords += layer[2*int(m1):] # tambien modificado m1->int(m1)
		else:
			coords += layer
	return coords

def centerStr(atpos):
	n = len(atpos)
	cx = cy = cz = 0.0
	for i in range(n):
		ele,x,y,z = atpos[i]
		cx += x/n
		cy += y/n
		cz += z/n
	for i in range(n):
		atpos[i][1] -= cx
		atpos[i][2] -= cy
		atpos[i][3] -= cz
	return atpos

def tomakeshell_wxyz(coords,element,name):
	center = True
	previous = False
	m1 = 0
	prev = []
	if os.path.exists(name):
		previous = True
		prefile = open(name,'r')
		prev = prefile.readlines()
		m1 = int(prev[0])
		del prev[0:2]
		atpos = []
		for i in range(m1):
			ele2,sx,sy,sz = prev[i].split()
			x = float(sx)
			y = float(sy)
			z = float(sz)
			atpos.append([ele2,x,y,z])
		if center:
			centerStr(atpos)
			
	xyzfile = open(name,'w')
	m2 = len(coords)
	n = m1 + m2
	xyzfile.write(str(n) + '\n\n')

	if previous:
		for atom in atpos:
			ele2,x,y,z = atom
			xyzfile.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(ele2,x,y,z))
	for i in range(m2):
		x,y,z = coords[i]
		xyzfile.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(element,x,y,z))

def sphericalShave(coords,r):
	cc=[]
	for p in coords:
		d = np.sqrt(p[0]*p[0]+ p[1]*p[1]+ p[2]*p[2])
		if d<r:
			cc.append(p)
	return cc

def atpos_eleList_maker(coords:list,element:str):
	atpos = []
	eleList = []
	for coord in coords:
		#print(coord)
		atpos.append([element,coord[0],coord[1],coord[2]])
		if element not in eleList:
			eleList.append(element)
	return atpos, eleList

def help():
	print('Functions work like this: coords = Shell(ns,d,...)')
	print('ns = number of Layer: 0,1,2,... if ns == 0, its necessary code capas=[np.array([0.0,0.0,0.0])]')
	print('all functions make only one layer of shell, except "cubeShell" that makes all a structure of ns layers')
	print('if cubeShell is on, structure = "fcc" or "bcc" or "simple"')
	print('tomakeshell_wxyz(coords,element,name) makes a name.xyz file, name="xxxx.xyz"')
	print('certerSrt(atpos) center the atpos, and sphericalShave(coords,r) cut the atpos radialy for radius r')

def interatomic_distances():
	distances = ['Pd:2.75 A', 'Pt:2.775 A', 'Ni:2.49 A', 'Co: None']
	print(distances)