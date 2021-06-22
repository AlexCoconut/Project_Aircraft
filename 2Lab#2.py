import matplotlib.pyplot as plt 
import math
import pandas as pd

                           # Constants
X = 0
Y0 = 15
Y = Y0
g = 1.62                                                                                                      # модуль ускорения свободного падения на Луне
a_max = 29.43                                                                                                 # лимит по ускорению
M = 2150                                                                                                      # масса корпуса
u = 3660                                                                                                      # скорость выхлопа газа
m_t = 1000                                                                                                     # начальная масса топлива
V_maxx = 1                                                                                                     # лимит по вертикальной скорости посадки
V_maxy = 3                                                                                                     # лимит по горизонтельной скорости посадки                                                                                             # общая масса ракеты

dt = 0.1                                                                                                  # малый промежуток времени (определяет дискретность процессов и точность вычислений)
V = 0                                                                                                        # текущая скорость
a = g                                                                                                         # текущее ускорение
m = M + m_t                                                                                                   # текущая масса ракеты
t = 0                                                                                                         # длительность маневра (счетчик времени)
dm = 0                                                                                                        # расход топлива (кг/с)
Vx = 0
Vy = 0
T = 0

###############################################################################
                           # 0-Angle search
L = 250010              
d = 0.0000001
alpha = 3.1416/3
ky = 0
km = 0
while ((ky == 0) and (km == 0)) and (alpha > 1):
    
    a = a_max
    ax = a*math.cos(alpha)
    ay = a*math.sin(alpha)
    
    while ((ay-g)*ay/g**2-(math.cos(alpha))**2 < 0):
        alpha -= 0.1
    while (L/( ax*math.sqrt( (ay-g)*ay/g**2-(math.cos(alpha))**2 ) + ax*(ay/g - 0.5) + 0.5*ax*math.cos(alpha) ) < 0):
        alpha -= 0.1
    t1 = math.sqrt ( L/( ax*math.sqrt( (ay-g)*ay/g**2-(math.cos(alpha))**2 ) + ax*(ay/g - 0.5) + 0.5*ax*math.cos(alpha) ) )


###

    t = 0
    while (t < t1):
        if (Y < 0): 
            ky = 1
            break
        if (m_t < 0): 
            km = 1
            break
        dm = m*a/((u+a*dt))
        m = M + m_t
        Y += Vy*dt + ay*dt**2/2 - g*dt**2/2
        X += Vx*dt + ax*dt**2/2
        Vy += ay*dt - g*dt
        Vx += ax*dt
        m_t -= dm*dt
        t += dt
    
    dm = 0    
    a = a_max
    t = 0
    t4 = (Vx-V_maxx)/a_max
    while (Vy > V_maxy) or (Y-Y0 > - Vy*t4 + g*t4**2/2):
        if (Y < 0): 
            ky = 1
            break
        if (m_t < 0): 
            km = 1
            break
        t4 = Vx/a
        Y += Vy*dt - g*dt**2/2
        X += Vx*dt
        Vy -= g*dt
        t += dt
    
    ax = Vx**2/(2*(L-X))
    tx = Vx/ax
    ay = 2*(- Vy*tx + g*tx**2/2 - (Y-Y0))/tx**2
    a = math.sqrt (ax**2 + ay**2)
    t = 0
    while (Vx > 0):
        if (Y < 0): 
            ky = 1
            break
        if (m_t < 0): 
            km = 1
            break
        if (Vy + ay*dt - g*dt > 0):
            ay = g
            a = math.sqrt (ax**2 + ay**2)
        
        dm = m*a/((u+a*dt))
        m = M + m_t
        Y += Vy*dt + ay*dt**2/2 - g*dt**2/2
        X += Vx*dt - ax*dt**2/2
        Vy += ay*dt - g*dt
        Vx -= ax*dt
        m_t -= dm*dt
        t += dt

    a = (V_maxy**2 - Vy**2)/(2*(Y - V_maxy*dt)) + g
    t = 0
    while (- Vy > V_maxy):
        if (Y < 0):
            ky = 1
            break
        if (m_t < 0):
            km = 1
            break
        dm = m*a/((u+a*dt))
        m = M + m_t
        Y += Vy*dt + a*dt**2/2 - g*dt**2/2
        X += Vx*dt
        Vy += a*dt - g*dt
        m_t -= dm*dt
        t += dt    

    t = 0
    a = g
    while (Y+Vy*dt > 0):
        if (Y < 0):
            ky = 1
            break
        if (m_t < 0):
            km = 1
            break
        dm = m*a/((u+a*dt))
        m = M + m_t
        Y += Vy*dt
        X += Vx*dt
        m_t -= dm*dt
        t += dt  

    if (ky == 0) and (km == 0):
        ky = 2
        km = 2  
    if ((ky == 1) and (km == 1)) or ((ky == 1) and (km == 0)) or ((ky == 0) and (km == 1)):
        ky = 0
        km = 0   
    
    alpha -= d
    Y = Y0
    m_t = 1000
    X = 0
    Vx = 0
    Vy = 0
    
###############################################################################
                           # Main part

a = a_max
alpha += d
L = 250000
m_t = 1000

#####################################
axe_t = []
axe_t1 = []
axe_t3 = []
axe_x = []
axe_x1 = []
axe_x3 = []
axe_y = []
axe_y1 = []
axe_y3 = []
axe_v = []
axe_a = []
axe_a2 = []
axe_dm = []
axe_alp = []

axe_t.append(T)
axe_x.append(X)
axe_y.append(Y)
axe_v.append(math.sqrt(Vx**2+Vy**2))
axe_a.append(a)
axe_dm.append(dm)
axe_alp.append(90-alpha/2/math.pi*180)
#####################################

ax = a*math.cos(alpha)
ay = a*math.sin(alpha)
t = 0
t1 = math.sqrt ( L/( ax*math.sqrt( (ay-g)*ay/g**2-(math.cos(alpha))**2 ) + ax*(ay/g - 0.5) + 0.5*ax*math.cos(alpha) ) )
while (t < t1):
    dm = m*a/((u+a*dt))
    m = M + m_t
    Y += Vy*dt + ay*dt**2/2 - g*dt**2/2
    X += Vx*dt + ax*dt**2/2
    Vy += ay*dt - g*dt
    Vx += ax*dt
    m_t -= dm*dt
    t += dt
    T += dt
    #print ('Y', Y, 'X', X, 'Vy', Vy, 'Vx', Vx, 'dm', dm, 'm_t', m_t, 'a', a)
    
    axe_t.append(T)
    axe_t1.append(T)
    axe_x.append(X)
    axe_x1.append(X)
    axe_y.append(Y)
    axe_y1.append(Y)
    axe_v.append(math.sqrt(Vx**2+Vy**2))
    axe_a.append(a)
    axe_dm.append(dm)
    axe_alp.append(90-alpha/2/math.pi*180)
    
L1 = X
print ('end of the first part')

dm = 0    
a = g
t4 = (Vx-V_maxx)/a_max
while (Vy > V_maxy) or (Y-Y0 > - Vy*t4 + g*t4**2/2):
    t4 = Vx/a_max
    Y += Vy*dt - g*dt**2/2
    X += Vx*dt
    Vy -= g*dt
    T += dt
    #print ('Y', Y, 'X', X, 'Vy', Vy, 'Vx', Vx, 'a', a)  
    
    axe_t.append(T)
    axe_x.append(X)
    axe_y.append(Y)
    axe_v.append(math.sqrt(Vx**2+Vy**2))
    axe_a.append(a)
    axe_dm.append(dm)
    axe_alp.append(90-math.atan(Vy/Vx))
    
print ('end of the second part')
L3 = X
H3 = Y  
T3 = T
ax = Vx**2/(2*(L-X))
tx = Vx/ax
ay = 2*(- Vy*tx + g*tx**2/2 - (Y-Y0))/tx**2
a = math.sqrt (ax**2 + ay**2)
while (Vx > 0):
    if (Vy + ay*dt - g*dt > 0):
        ay = g
        a = math.sqrt (ax**2 + ay**2)
    
    dm = m*a/((u+a*dt))
    m = M + m_t
    Y += Vy*dt + ay*dt**2/2 - g*dt**2/2
    X += Vx*dt - ax*dt**2/2
    Vy += ay*dt - g*dt
    Vx -= ax*dt
    m_t -= dm*dt
    T += dt
    #print ('Y', Y, 'X', X, 'Vy', Vy, 'Vx', Vx, 'dm', dm, 'm_t', m_t, 'a', a)
    
    axe_t.append(T)
    axe_t3.append(T)
    axe_x.append(X)
    axe_x3.append(X)
    axe_y.append(Y)
    axe_y3.append(Y)
    axe_v.append(math.sqrt(Vx**2+Vy**2))
    axe_a.append(a)
    axe_a2.append(a)
    axe_dm.append(dm)
    axe_alp.append(-(90-math.atan(Vy/Vx)))
    
print ('end of the third part')

print ('start of the fourth part')    
a = (V_maxy**2 - Vy**2)/(2*(Y - V_maxy*dt)) + g
while (- Vy > V_maxy):
    dm = m*a/((u+a*dt))
    m = M + m_t
    Y += Vy*dt + a*dt**2/2 - g*dt**2/2
    X += Vx*dt
    Vy += a*dt - g*dt
    m_t -= dm*dt
    T += dt
    #print ('Y', Y, 'X', X, 'Vy', Vy, 'Vx', Vx, 'dm', dm, 'm_t', m_t, 'a', a)
    
    axe_t.append(T)
    axe_t3.append(T)
    axe_x.append(X)
    axe_x3.append(X)
    axe_y.append(Y)
    axe_y3.append(Y)
    axe_v.append(math.sqrt(Vx**2+Vy**2))
    axe_a.append(a)
    axe_a2.append(a)
    axe_dm.append(dm)
    axe_alp.append(0)

print ('end of the fourth part')    
    
print ('start of the fifth part')    
a = g
dt = 0.00001
while (Y+Vy*dt > 0):
    dm = m*a/((u+a*dt))
    m = M + m_t
    Y += Vy*dt
    X += Vx*dt
    m_t -= dm*dt
    T += dt 
    #print ('Y', Y, 'X', X, 'Vy', Vy, 'Vx', Vx, 'dm', dm, 'm_t', m_t, 'a', a)    
    
    axe_t.append(T)
    axe_t3.append(T)
    axe_x.append(X)
    axe_x3.append(X)
    axe_y.append(Y)
    axe_y3.append(Y)
    axe_v.append(math.sqrt(Vx**2+Vy**2))
    axe_a.append(a)
    axe_a2.append(a)
    axe_dm.append(dm)
    axe_alp.append(0)

print ('end of the fifth part')
print ('Y', Y, 'X', X, 'Vy', Vy, 'Vx', Vx, 'dm', dm, 'm_t', m_t)  
print ('rocket landed')
if (m_t >= 0):
    print ('cool guy!')
else:
    print ('all fuel burned out couple of minutes ago ...')
    
df = pd.DataFrame ({'Time, s': axe_t,
                    'X, m': axe_x,
                    'Y, m': axe_y,
                    'V, m/s': axe_v,
                    'a, m/s^2': axe_a,
                    'dm, kg/s': axe_dm,
                    'alpha': axe_alp})
df.to_excel ('./rocket.xlsx')

    
fig = plt.figure()
#fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots (nrows=3, ncols=2, figsize=(25,40))

fig, ax1 = plt.subplots (nrows=1, ncols=1, figsize=(10,10))
ax1.plot(axe_t,axe_v)
ax1.set_xlim([0, T+1])
ax1.set_ylim([0, 700])
ax1.set_title(r'V(t)')
ax1.set_xlabel('Time, s')
ax1.set_ylabel('Velocity, $m/s$')

fig, ax2 = plt.subplots (nrows=1, ncols=1, figsize=(10,10))
ax2.plot(axe_x,axe_y)
ax2.set_xlim([0, L])
ax2.set_ylim([0, 110000])
ax2.set_title(r'Y(X) - all flight')
ax2.set_xlabel('X, m')
ax2.set_ylabel('Y, m')

fig, ax3 = plt.subplots (nrows=1, ncols=1, figsize=(10,10))
ax3.plot(axe_x1,axe_y1)
ax3.set_xlim([0, L1])
ax3.set_ylim([0, 10000])
ax3.set_title(r'Y(X) - first flight part')
ax3.set_xlabel('X, m')
ax3.set_ylabel('Y, m')

fig, ax4 = plt.subplots (nrows=1, ncols=1, figsize=(10,10))
ax4.plot(axe_x3,axe_y3)
ax4.set_xlim([L3, L])
ax4.set_ylim([0, H3])
ax4.set_title(r'Y(X) - 3d-5th parts')
ax4.set_xlabel('X, m')
ax4.set_ylabel('Y, m')

fig, ax5 = plt.subplots (nrows=1, ncols=1, figsize=(10,10))
ax5.plot(axe_t,axe_a)
ax5.set_xlim([0, T+1])
ax5.set_ylim([0, a_max+3])
ax5.set_title(r'a(t) - all flight')
ax5.set_xlabel('Time, s')
ax5.set_ylabel('Rocket acceleration, $m/s^2$')

fig, ax6 = plt.subplots (nrows=1, ncols=1, figsize=(10,10))
ax6.plot(axe_t3,axe_a2)
ax6.set_xlim([T3, T+1])
ax6.set_ylim([0, a_max+3])
ax6.set_title(r'a(t) - 3d-5th parts')
ax6.set_xlabel('Time, s')
ax6.set_ylabel('Rocket acceleration, $m/s^2$')