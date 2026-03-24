"""
Práctica 1: Diseño de controladores

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Victor Silvano Dino Seanez
Número de control: 20211964
Correo institucional: l20211964@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
""" 
import control as ctrl
import numpy  as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

u = np.array(pd.read_excel('signal.xlsx',header=None))
x0,t0,tend,dt,w,h = 0,0,15,1e-3,10,5
N  = round((tend-t0)/dt)+ 1
t = np.linspace(t0,tend, N)
u = np.reshape(signal.resample(u,len(t)),-1)

def cardio(Z,C,R,L):
    num=[L*R,R*Z]
    den= [C*L*R*Z,L*R+L*Z,R*Z]
    sys = ctrl.tf(num,den)
    return sys

#funcion de transferencia : normotenso
Z,C,R,L = 0.33,1.5,0.95,0.01
sysnormo =cardio(Z,C,L,R)
print (f'Funcion de transferencia del normotenso(control): {sysnormo}')

#funcion de transferencia : hipotenso
Z,C,R,L = 0.02,0.25,0.6,0.005
sysnormo =cardio(Z,C,L,R)
print(f'Funcion de transferencia del hipotenso(caso1): {syshipo}')

#funcion de transferencia : hipertenso
Z,C,R,L = 0.05,2.5,1.4,0.02
sysnormo =cardio(Z,C,L,R)
print(f'Funcion de transferencia del hipertenso(caso2): {syshiper}')

#Respuestas en lazo abierto
_,Pp0 =ctrl.forced_response(sysnormo,t,u,x0)
_,Pp1 =ctrl.forced_response(syshipo,t,u,x0)
_,Pp2 =ctrl.forced_response(syshiper,t,u,x0)
fg1 =plt.figure()
plt.plot(t,Pp0,'-',linewidth=1,color=[0.25,0.51,0.47],label='PP(t) Normotenso')
plt.plot(t,Pp1,'-',linewidth=1,color=[0.5,0.10,0.05],label='PP(t) Hipotenso')
plt.plot(t,Pp2,'-',linewidth=1,color=[0.00,0.25,0.40],label='PP(t) Hipertenso')
plt.gride(False)
plt.xlim(0,15);plt.xtick(np.arrange(0,16,1))
plt.ylim(-0.6,1.4)plt.yticks(np.arrange(-0.16,1.6,0.2))
plt.xlabel('t[s]')
pl.ylabel('Pp(t)[V]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg1.set_size_inches(w,h)
fg1.tight_layout()
fg1.savefig('Cardiovascular lazo abierto python.pdf')