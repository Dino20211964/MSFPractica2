# Librerías necesarias:
# pip install control
# pip install slycot

import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

# ===================== ENTRADA =====================
u = np.array(pd.read_excel('signal.xlsx', header=None))

x0, t0, tend, dt, w, h = 0, 0, 15, 1e-3, 10, 5
N = round((tend - t0) / dt) + 1
t = np.linspace(t0, tend, N)

u = np.reshape(signal.resample(u, len(t)), -1)

# ===================== MODELO =====================
def cardio(Z, C, R, L):
    num = [L*R, R*Z]
    den = [C*L*R*Z, L*R + L*Z, R*Z]
    sys = ctrl.tf(num, den)
    return sys

# Normotenso
Z, C, R, L = 0.033, 1.5, 0.95, 0.01
sysnormo = cardio(Z, C, R, L)
print(f'Funcion de transferencia del normotenso: {sysnormo}')

# Hipotenso
Z, C, R, L = 0.02, 0.25, 0.6, 0.005
syshipo = cardio(Z, C, R, L)
print(f'Funcion de transferencia del hipotenso: {syshipo}')

# Hipertenso
Z, C, R, L = 0.05, 2.5, 1.4, 0.02
syshiper = cardio(Z, C, R, L)
print(f'Funcion de transferencia del hipertenso: {syshiper}')

# ===================== RESPUESTAS LAZO ABIERTO =====================
_, Pp0 = ctrl.forced_response(sysnormo, t, u, x0)
_, Pp1 = ctrl.forced_response(syshipo, t, u, x0)
_, Pp2 = ctrl.forced_response(syshiper, t, u, x0)

# ===================== FIGURA 1 =====================
fg1 = plt.figure()

plt.plot(t, Pp0, '-', linewidth=1, color='tab:blue', label='Pp(t): Normotenso')
plt.plot(t, Pp1, '-', linewidth=1, color='tab:orange', label='Pp(t): Hipotenso')
plt.plot(t, Pp2, '-', linewidth=1, color='tab:green', label='Pp(t): Hipertenso')

plt.grid(False)
plt.xlim(0, 15)
plt.xticks(np.arange(0, 16, 1))
plt.ylim(-0.6, 1.4)
plt.yticks(np.arange(-0.6, 1.6, 0.2))

plt.xlabel('t[s]')
plt.ylabel('Pp(t) [V]')

plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=3)

plt.show()

fg1.set_size_inches(w, h)
fg1.tight_layout()
fg1.savefig('Cardiovascular_lazo_abierto_python.pdf')

# ===================== CONTROLADOR PID =====================
def controlador(kP, kI, kD, sys):
    Cr = 1e-6
    Re = 1 / (kI * Cr)
    Rr = kP * Re
    Ce = kD / Rr

    numPID = [Re*Rr*Ce*Cr, (Re*Ce + Rr*Cr), 1]
    denPID = [Re*Cr, 0]

    PID = ctrl.tf(numPID, denPID)
    X = ctrl.series(PID, sys)
    sysPID = ctrl.feedback(X, 1, sign=-1)

    return sysPID

hipoPID = controlador(1.49397900518606, 352.000659394334, 0.00049119206492278, syshipo)
print(f'Hipotenso con PID: {hipoPID}')

hiperPID = controlador(12.7154893348189, 363.894411463659, 0.0343454696960019, syshiper)
print(f'Hipertenso con PID: {hiperPID}')

# ===================== RESPUESTAS PID =====================
_, PID1 = ctrl.forced_response(hipoPID, t, Pp0, x0)
_, PID2 = ctrl.forced_response(hiperPID, t, Pp0, x0)

# ===================== SUBPLOTS =====================
fig, ax = plt.subplots(2, 1, sharex=True)

# -------- (a) Normotenso vs Hipotenso --------
ax[0].plot(t, Pp0, '-', linewidth=1.5,
           color='tab:blue',
           label=r'$P_p(t)$: Normotenso')

ax[0].plot(t, Pp1, '-', linewidth=1.5,
           color='tab:orange',
           label=r'$P_p(t)$: Hipotenso')

ax[0].plot(t, PID1, ':', linewidth=2,
           color='tab:red',
           label=r'$PID(t)$: Hipotenso')

ax[0].set_title('Normotenso vs Hipotenso')
ax[0].set_ylabel(r'$P_p(t)$ [V]')
ax[0].set_xlim(0, 15)
ax[0].grid(False)

ax[0].legend(loc='lower center',
             bbox_to_anchor=(0.5, 1.12),
             ncol=3,
             frameon=False,
             fontsize=9)

ax[0].text(0.01, 1.05, '(a)', transform=ax[0].transAxes)

ax[0].autoscale(enable=True, axis='y')
ax[0].margins(y=0.1)

# -------- (b) Normotenso vs Hipertenso --------
ax[1].plot(t, Pp0, '-', linewidth=1.5,
           color='tab:blue',
           label=r'$P_p(t)$: Normotenso')

ax[1].plot(t, Pp2, '-', linewidth=1.5,
           color='tab:green',
           label=r'$P_p(t)$: Hipertenso')

ax[1].plot(t, PID2, ':', linewidth=2,
           color='tab:red',
           label=r'$PID(t)$: Hipertenso')

ax[1].set_title('Normotenso vs Hipertenso')
ax[1].set_xlabel(r'$t$ [s]')
ax[1].set_ylabel(r'$P_p(t)$ [V]')
ax[1].set_xlim(0, 15)
ax[1].grid(False)

ax[1].legend(loc='lower center',
             bbox_to_anchor=(0.5, 1.12),
             ncol=3,
             frameon=False,
             fontsize=9)

ax[1].text(0.01, 1.05, '(b)', transform=ax[1].transAxes)

ax[1].autoscale(enable=True, axis='y')
ax[1].margins(y=0.1)

# ===================== FORMATO FINAL =====================
fig.set_size_inches(w, 2.3*h)
fig.tight_layout(rect=[0, 0, 1, 0.95])

plt.show()

fig.savefig('Subplots_Normotenso_Hipotenso_Hipertenso_PID.pdf')