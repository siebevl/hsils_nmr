# Siebe Vanlommel
import numpy as np, glob
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt

#ref = 560.0 #estimate
ref = (571.329 - 7.3) # 23Na in NaNO3 (PBE+pcSseg-3) is -7.3 ppm

Na_freq = 132.49 # MHz, of spectrometer
def get_spectrum(mainpath, sigma=0):
    sum_spec = None
    freq = None
    files = sorted(glob.glob(mainpath))
    #print(files)
    for f in files:
        d = np.loadtxt(f)
        freq = d[:,0]
        spec = d[:,1] #real part of signal
        if sum_spec is None:
            sum_spec = np.zeros_like(spec)
        sum_spec += spec
    sum_spec /= np.trapz(sum_spec)
    final_filter = gaussian_filter1d(sum_spec, sigma=sigma)
    freq = -1*freq/132.49 + ref
    return freq, final_filter, sum_spec

fig, ax = plt.subplots(1,2)

freq0,spec0_f,spec0 = get_spectrum("isotropic/high-xNa/*/output.txt", sigma=10)
freq1,spec1_f,spec1 = get_spectrum("isotropic/low-xNa/*/output.txt", sigma=10)
ax[0].plot(freq0, spec0, c='gold', label='iso (a0b0, CS), $x_{Na} = 0.267$', linestyle='--')
ax[0].plot(freq1, spec1, c='tab:blue', label='iso (a0b0, CS), $x_{Na} = 0.004$', linestyle='--')

freq2,spec2_f,spec2 = get_spectrum("anisotropic/high-xNa/*/output.txt", sigma=10)
freq3,spec3_f,spec3 = get_spectrum("anisotropic/low-xNa/*/output.txt", sigma=10)
ax[1].plot(freq2, spec2, c='gold', label='aniso (rep256, CS+CSA+QC), $x_{Na} = 0.267$')
ax[1].plot(freq3, spec3, c='tab:blue', label='aniso (rep256, CS+CSA+QC), $x_{Na} = 0.004$')

lim=200
ax[0].set_xlabel("23Na $\delta$ [ppm]")
ax[1].set_xlabel("23Na $\delta$ [ppm]")
#plt.ylabel("intensity")
#plt.title(f"Summed NMR spectra")
ax[0].set_xlim(lim,-1*lim)
ax[1].set_xlim(lim,-1*lim)
ax[0].legend()
ax[1].legend()
plt.tight_layout()
plt.show()
