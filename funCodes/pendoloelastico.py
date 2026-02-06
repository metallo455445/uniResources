import numpy as np
import math
import matplotlib.pyplot as plt
# Pendolo elastico

def traiettoria():
  dt = 0.001 # s integration step
  nstep = 1000 # how many forward steps
  ninner = 20 # internal steps
  l0 = 1.
  k = 1.e2
# condizioni iniziali
  r0 = 1.1
  th0 = 0.3
  dotr0 = 0.
  dotth0 = 0.2
  g = 10.
  m = 1.
  peso = g*m

  tf = dt*nstep*ninner # s final time

  t = 0
  ts = np.empty(nstep+1)
  rhot = np.empty(nstep+1)
  thet = np.empty(nstep+1)
  enet = np.empty(nstep+1)
  xt = np.empty(nstep+1)
  yt = np.empty(nstep+1)
  i = -10
  r = r0
  th = th0
  dotr = dotr0
  dotth = dotth0
  t = 0
  while i<=nstep:
     j=0
     while j<ninner:
        fr = - k*(r-l0)+peso*math.cos(th)
        fth = -peso*math.sin(th)
        th1  = th + dt*dotth
        r1 = r + dt*dotr
        dotth1 = dotth + dt*(fth/m-2*dotth*dotr)/r
        dotr1 = dotr + dt*(fr/m+r*dotth**2)
        fr = - k*(r1-l0)+peso*math.cos(th1)
        fth = -peso*math.sin(th1)
        th2  = th + dt*dotth1
        r2 = r + dt*dotr1
        dotth2 = dotth + dt*(fth/m-2*dotth1*dotr1)/r1
        dotr2 = dotr+dt*(fr/m+r1*dotth1**2)
        r = 0.5*(r1+r2)
        th = 0.5*(th1+th2)
        dotth = 0.5*(dotth1+dotth2)
        dotr = 0.5*(dotr1+dotr2)
#
        t = t + dt
        j = j + 1
     if i >=0 : 
       ts[i] = t
       rhot[i] = r
       thet[i] = th
       xt[i] = r*math.sin(th)
       yt[i] = -r*math.cos(th)
       enet[i] = 0.5*m*(dotr**2+(r*dotth)**2)+k*0.5*(r-l0)**2-m*g*r*math.cos(th)
     i = i + 1

  # plot data

  plt.figure(1)
  plt.plot(ts,rhot)
  plt.xlabel("t")
  plt.ylabel("r(t)")
  plt.figure(2)
  plt.plot(ts,thet)
  plt.xlabel("t")
  plt.ylabel('$\\theta(t)$')
  plt.figure(3)
  plt.plot(xt,yt)
  plt.xlabel("x")
  plt.ylabel("y")
#  plt.figure(4)
#  plt.plot(ts,enet)
#  plt.xlabel("time")
#  plt.ylabel("energy")
  plt.show()

# call function
traiettoria()
