program rdf
implicit none
integer, parameter :: nhis=2600
integer :: i,j,npart,ngr,ig,m,b1,b2,b3,b4
integer, dimension(:), allocatable :: b
real :: bij,bm,box,dx,dy,dz,delr,r,rmin,rmax,rmed,hint
real, dimension(:), allocatable :: x,y,z
real, dimension(nhis) :: hist,hs1,hs2,base,gr
character(32) :: a
character(2) :: ele

open(unit=10,file='shell.xyz')
read(10,*) npart
!read(10,*) a !uncomment for dump
allocate(b(npart))
allocate(x(npart))
allocate(y(npart))
allocate(z(npart))

b1 = 28 !Ni
b2 = 78 !Pt
b3 = 27 !Co
b4 = 46 !Pd
bm = 0.0

do i=1,npart
   read(10,*) ele, x(i), y(i), z(i)
   if(ele.eq.'Ni'.or.ele.eq.'1') b(i)=b1 
   if(ele.eq.'Pt'.or.ele.eq.'2') b(i)=b2 
   if(ele.eq.'Co'.or.ele.eq.'3') b(i)=b3
   if (ele.eq.'Pd') b(i) = b4
   bm = bm + b(i)
end do

print*, x(1), y(1), z(1),b(1),bm
print*, x(2), y(2), z(2),b(2),bm
print*, x(3), y(3), z(3),b(3),bm

bm = bm/npart
20 format(a2,3f12.5)
close(10)
!print*, ele, x(1), y(1), z(1),b(1),bm


delr = 0.02
box = nhis*delr
hist(:) = 0.0

m = npart*(npart-1)/2
rmin = 10.0
rmax = 0.0
rmed = 0.0
hint = 0.0

do i = 1,npart-1
   do j = i+1,npart
      bij = b(i)*b(j)/bm**2
      dx = x(i)-x(j)
      dy = y(i)-y(j)
      dz = z(i)-z(j)
      r = sqrt(dx**2 +dy**2 +dz**2)
      if (r < 0.1) print*, i,j
      if (r < box) then
         ig = int(r/delr-0.5)
         hist(ig) = hist(ig) +2.0*bij/(r*delr)
         hint = hint +1/r
         rmed = rmed +r
         if (r < rmin) rmin = r
         if (r > rmax) rmax = r
      else
         print*, 'El tamaño del sistema supera los parametros ',r,' > ',box
      end if
   end do
end do

rmed = rmed/m
hist = hist/hint

call smooth(hist,5,hs1)
!call smooth(hs1,5,hs2)
!call smooth(hs2,5,hs1)
call smooth(hist,100,hs2)
call smooth(hs2,100,base)
gr = hs1-base

print*, npart,' atomos ',m,' pares '
print*, 'Rango de distancias ',rmin,'-',rmax
print*, 'Distancias promedio ',rmed
print*, 'Factor de normalizacion ',hint
!print*, shape(h)

open(unit=11,file='rdf.txt',action='write',status='replace')
write(11,*) '#r(A)        h(r)         Base         G(r)'
!write(11,*) '#r(A)        G(r)'
do i = 1,nhis
   r = i*delr
   write(11,30) r, hist(i), base(i), gr(i)
!   write(11,30) r, gr(i)
end do
30 format(f6.2,3f13.5)
close(11)

end program


subroutine smooth(h,ns,f)
implicit none
integer, parameter :: nhis=2600
integer :: i,j,ns,k
real :: x
real,dimension(nhis) :: h,f

k = int(ns/2)
do i = 1,nhis
   x = 0.0
   do j = i-k,i+k
      if (j>=1 .and. j<=nhis)  x = x + h(j)
   end do
   f(i) = x/(2*k+1)
end do

end subroutine


